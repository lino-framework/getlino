# Copyright 2019-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Some utilities for getlino.
"""

import os
from os.path import expanduser
from pathlib import Path
import stat
import shutil
try:
    import grp
except ImportError:
    grp = None  # e.g. on Windows
import configparser
import subprocess
import click
# import platform
import distro
import collections
import getpass
from contextlib import contextmanager
import virtualenv
from jinja2 import Environment, PackageLoader
from .setup_info import SETUP_INFO

JINJA_ENV = Environment(loader=PackageLoader('getlino', 'templates'))

# currently getlino supports only nginx, maybe we might add other web servers
# USE_NGINX = True

BATCH_HELP = "Whether to run in batch mode, i.e. without asking any questions.  "\
             "Don't use this on a machine that is already being used."

# note that we double curly braces because we will run format() on this string:
LOGROTATE_CONF = """\
# generated by getlino
{logfile} {{
    weekly
    missingok
    rotate 156
    compress
    delaycompress
    notifempty
    create 660 root {usergroup}
    su root {usergroup}
    sharedscripts
}}
"""

def perm2text(value):
    """

    Convert a permission value given as integer returned by os.stat() to an "rwx"
    like text as used by :command:`ls -l`.

    Inspired from comment by hack-tramp (Jul 6, 2020) on
    https://gist.github.com/beugley/47b4812df0837fc90e783347faee2432
    """
    octal = "{:04o}".format(value)
    result =  ''
    first = 0
    # if there are 4 digits, deal with first (setuid, setgid, and sticky flags) separately
    if len(octal) > 4:
        raise Exception("value must be less than 0o7777")
    if octal[0] != '0':
        first = int(octal [:1])
    octal = octal [-3:]
    value_letters = [(4, 'r'), (2, 'w'), (1, 'x')]
    # Iterate over each of the digits in octal
    for permission in [int(n) for n in octal]:
        # Check for each of the permissions values
        for value, letter in value_letters:
            if permission >= value:
                result += letter
                permission -= value
            else:
                result += '-'
    if first != 0:
        for value in [4, 2, 1]:
           if first >= value:
              if value == 4:
                 if result[2] == 'x':
                    result = result[:2] + 's' + result[3:]
                 elif result[2] == '-':
                    result = result[:2] + 'S' + result[3:]
              if value == 2:
                 if result[5] == 'x':
                    result = result[:5] + 's' + result[6:]
                 elif result[5] == '-':
                    result = result[:5] + 'S' + result[6:]
              if value == 1:
                 if result[8] == 'x':
                    result = result[:8] + 't' + result[9:]
                 elif result[8] == '-':
                    result = result[:8] + 'T' + result[9:]
              first -= value

    return result


class WebServer(object):
    apt_packages = ''
    service = None
    name = None  # name must match certbot convention (nginx, apache)

class Nginx(WebServer):
    name = 'nginx'
    service = 'nginx'
    apt_packages = "nginx uwsgi-plugin-python3"

class Apache(WebServer):
    name = 'apache'
    service = 'apache2'
    apt_packages = "apache2 libapache2-mod-wsgi"

WEB_SERVERS = [Nginx(), Apache()]

# def default_web_server():
#     return ifroot("nginx", '')

def resolve_web_server(web_server):
    if not web_server:
        return None
    for e in WEB_SERVERS:
        if e.name == web_server:
            return e
    raise click.ClickException("Invalid --web-server '{}'.".format(web_server))

class DbEngine(object):
    name = None  # Note that the DbEngine.name field must match the Django engine name
    service = None
    apt_packages = ''
    python_packages = ''
    needs_root = False
    "Whether you need to be root in order to create users and databases."

    def runcmd(self, i, sqlcmd):
        pass

    def setup_database(self, i, database, user, db_host):
        click.echo("No setup needed for " + self.name)

    def setup_user(self, i, context):
        click.echo("No need to setup user for " + self.name)

    def after_prep(self, i, context):
        pass

class SQLite(DbEngine):
    name = 'sqlite3'
    default_port = ""

    def after_prep(self, i, context):
        project_dir = context['project_dir']
        prjname = context['prjname']
        pth = Path(project_dir) / prjname
        if os.path.exists(pth):
            with i.override_batch(True):
                i.check_permissions(pth)



class MySQL(DbEngine):
    name = 'mysql'
    service = 'mysql'
    default_port = "3306"
    apt_packages = "mysql-server libmysqlclient-dev"
    python_packages = "mysqlclient"
    needs_root = True

    def __init__(self):
        super(MySQL, self).__init__()
        # apt_packages = "mysql-server libmysqlclient-dev"
        # TODO: support different platforms (Debian, Ubuntu, Elementary, ...)
        # apt_packages += " python-dev libffi-dev libssl-dev python-mysqldb"
        if distro.id() == "debian":
            # package name is mariadb but service name remains mysql
            # self.service = 'mariadb'
            self.apt_packages = "mariadb-server libmariadb-dev-compat libmariadb-dev "\
                "python-dev libffi-dev libssl-dev"
                # "python-dev libffi-dev libssl-dev python-mysqldb"

    def run(self, i, sqlcmd):
        options = "" if i.batch else "-p"
        return i.runcmd('mysql -u root {} -e "{};"'.format(options, sqlcmd))

    def setup_user(self, i, context):
        self.run(i, "create user '{db_user}'@'{db_host}' identified by '{db_password}'".format(**context))

    def setup_database(self, i, database, user, db_host):
        self.run(i, "create database {database} charset 'utf8'".format(**locals()))
        self.run(i, "grant all PRIVILEGES on {database}.* to '{user}'@'{db_host}'".format(**locals()))

class PostgreSQL(DbEngine):
    name = 'postgresql'
    service = 'postgresql'
    apt_packages = "postgresql postgresql-contrib libpq-dev python-dev"
    # python_packages = "psycopg2"
    python_packages = "psycopg2-binary"
    default_port = "5432"
    needs_root = True

    def run(self, i, cmd):
        assert '"' not in cmd
        # self.runcmd('sudo -u postgres bash -c "psql -c \\\"{}\\\""'.format(cmd))
        i.runcmd('sudo -u postgres psql -c "{}"'.format(cmd))

    def setup_user(self, i, context):
        self.run(i, "CREATE USER {db_user} WITH PASSWORD '{db_password}';".format(**context))

    def setup_database(self, i, database, user, db_host):
        self.run(i, "CREATE DATABASE {database};".format(**locals()))
        self.run(i, "GRANT ALL PRIVILEGES ON DATABASE {database} TO {user};".format(**locals()))


DB_ENGINES = [MySQL(), PostgreSQL(), SQLite()]

def default_db_engine():
    return ifroot("mysql", 'sqlite3')

def resolve_db_engine(db_engine):
    for e in DB_ENGINES:
        if e.name == db_engine:
            return e
    raise click.ClickException("Invalid --db-engine '{}'.".format(db_engine))



Repo = collections.namedtuple(
    'Repo', 'nickname package_name git_repo settings_module front_end')
REPOS_DICT = {}
KNOWN_REPOS = []

def add(nickname, package_name, git_repo='', settings_module='', front_end=''):
    t = Repo(nickname, package_name, git_repo, settings_module, front_end)
    KNOWN_REPOS.append(t)
    REPOS_DICT[t.nickname] = t
    if t.front_end:
        # add an alias because front ends are identified using their full package name
        REPOS_DICT[t.front_end] = t

# some tools to be installed with --clone because they are required for a complete contributor environment:
add("cd", "commondata", "https://github.com/lsaffre/commondata")
add("be", "commondata.be", "https://github.com/lsaffre/commondata-be")
add("ee", "commondata.ee", "https://github.com/lsaffre/commondata-ee")
add("eg", "commondata.eg", "https://github.com/lsaffre/commondata-eg")
add("atelier", "atelier", "https://github.com/lino-framework/atelier")
add("rstgen", "rstgen", "https://github.com/lino-framework/rstgen")
add("etgen", "etgen", "https://github.com/lino-framework/etgen")
add("eid", "eidreader", "https://github.com/lino-framework/eidreader")

add("lino", "lino", "https://github.com/lino-framework/lino", "", "lino.modlib.extjs")
add("xl", "lino-xl", "https://github.com/lino-framework/xl")
add("welfare", "lino-welfare", "https://github.com/lino-framework/welfare")
add("amici", "lino-amici", "https://github.com/lino-framework/amici", "lino_amici.lib.amici.settings")
add("avanti", "lino-avanti", "https://github.com/lino-framework/avanti", "lino_avanti.lib.avanti.settings")
add("care", "lino-care", "https://github.com/lino-framework/care", "lino_care.lib.care.settings")
add("cosi", "lino-cosi", "https://github.com/lino-framework/cosi", "lino_cosi.lib.cosi.settings")
add("noi", "lino-noi", "https://github.com/lino-framework/noi", "lino_noi.lib.noi.settings")
add("presto", "lino-presto", "https://github.com/lino-framework/presto", "lino_presto.lib.presto.settings")
add("pronto", "lino-pronto", "https://github.com/lino-framework/pronto", "lino_pronto.lib.pronto.settings")
add("tera", "lino-tera", "https://github.com/lino-framework/tera", "lino_tera.lib.tera.settings")
add("vilma", "lino-vilma", "https://github.com/lino-framework/vilma", "lino_vilma.lib.vilma.settings")
add("voga", "lino-voga", "https://github.com/lino-framework/voga", "lino_voga.lib.voga.settings")
add("weleup", "lino-weleup", "https://github.com/lino-framework/weleup", "lino_weleup.settings")
add("welcht", "lino-welcht", "https://github.com/lino-framework/welcht", "lino_welcht.settings")
add("ciao", "lino-ciao", "https://github.com/lino-framework/ciao", "lino_ciao.lib.ciao.settings")

add("book", "lino-book", "https://gitlab.com/lino-framework/book")
add("react", "lino-react", "https://github.com/lino-framework/react", "", "lino_react.react")
add("openui5", "lino-openui5", "https://github.com/lino-framework/openui5", "", "lino_openui5.openui5")

# experimental: applications that have no repo on their own
add("min1", "", "", "lino_book.projects.min1.settings")
add("min2", "", "", "lino_book.projects.min2.settings")
add("polls", "", "", "lino_book.projects.polls.mysite.settings")
add("cosi_ee", "", "", "lino_book.projects.cosi_ee.settings.demo")
add("lydia", "", "", "lino_book.projects.lydia.settings.demo")
add("noi1e", "", "", "lino_book.projects.noi1e.settings.demo")
add("chatter", "", "", "lino_book.projects.chatter.settings")

# e.g. for installing a non-Lino site like mailman
add("std", "", "", "lino.projects.std.settings")

APPNAMES = [a.nickname for a in KNOWN_REPOS if a.settings_module]
FRONT_ENDS = [a for a in KNOWN_REPOS if a.front_end]

CONF_FILES = ['/etc/getlino/getlino.conf', expanduser('~/.getlino.conf')]
CONFIG = configparser.ConfigParser()
FOUND_CONFIG_FILES = CONFIG.read(CONF_FILES)
DEFAULTSECTION = CONFIG[CONFIG.default_section]

def ifroot(true=True, false=False):
    if not hasattr(os, 'geteuid'):
        return false
    if os.geteuid() == 0:
        return true
    return false

def has_usergroup(usergroup):
    for gid in os.getgroups():
        if grp.getgrgid(gid).gr_name == usergroup:
            return True
    return False

def which_certbot():
    for x in ["certbot",  "certbot-auto"]:
        if shutil.which(x):
            return x

class Installer(object):
    """Volatile object used by :mod:`getlino.configure` and :mod:`getlino.startsite`.
    """
    def __init__(self, batch=False):
        self.batch = batch
        # self.asroot = ifroot()
        self._services = set()
        self._system_packages = set()
        if ifroot():
            click.echo("Running as root.")
        click.echo("This is getlino version {} running on {} ({} {}).".format(
            SETUP_INFO['version'], distro.name(pretty=True),
            distro.id(), distro.codename()))

    def check_overwrite(self, pth):
        """If `pth` (directory or file) exists, remove it after asking for confirmation.
        Return False if it exists and user doesn't confirm.
        """
        if not os.path.exists(pth):
            return True
        if os.path.isdir(pth):
            if self.yes_or_no("Overwrite existing directory {} ?".format(pth)):
                shutil.rmtree(pth)
                return True
        else:
            if self.yes_or_no("Overwrite existing file {} ?".format(pth)):
                os.remove(pth)
                return True
        return False

    def yes_or_no(self, msg, yes="yY", no="nN", default=True):
        """Ask for confirmation without accepting a mere RETURN."""
        if self.batch:
            return default
        click.echo(msg + " [y or n]", nl=False)
        while True:
            c = click.getchar()
            if c in yes:
                click.echo(" Yes")
                return True
            elif c in no:
                click.echo(" No")
                return False

    def must_restart(self, srvname):
        self._services.add(srvname)

    def runcmd(self, *cmds, **kw):
        """Run the specified command(s) in a subprocess.

        Stop when Ctrl-C. If the subprocess has non-zero return code, we simply
        stop. We don't use check=True because this would add another useless
        traceback.  The subprocess is responsible for reporting the reason of
        the error.

        """
        # kw.update(stdout=subprocess.PIPE)
        # kw.update(stderr=subprocess.STDOUT)
        kw.update(shell=True)
        kw.update(universal_newlines=True)
        # kw.update(check=True)
        # subprocess.check_output(cmd, **kw)
        if self.batch or self.yes_or_no("run {}".format(";".join(cmds)), default=True):
            for cmd in cmds:
                click.echo(cmd)
                cp = subprocess.run(cmd, **kw)
                if cp.returncode != 0:
                    # subprocess.run("sudo journalctl -xe", **kw)
                    raise click.ClickException(
                    "{} ended with return code {}".format(cmd, cp.returncode))

    def runcmd_sudo(self, *cmds, **kwargs):
        """
        Run the specified command(s) in a subprocess, prefixing each with sudo
        if needed.

        """
        if ifroot():
            pass
        elif has_usergroup('sudo'):
            cmds = ["sudo " + c for c in cmds]
        else:
            click.echo(
                "The following commands were not executed "
                "because you cannot sudo:\n{}".format("\n".join(cmds)))
            return
        self.runcmd(*cmds, **kwargs)

    def apt_install(self, packages):
        for pkg in packages.split():
            # no check for if package is already installed:
            self._system_packages.add(pkg)

    def run_in_env(self, env, cmd):
        """env is the path of the virtualenv"""
        # click.echo(cmd)
        cmd = ". {}/bin/activate && {}".format(env, cmd)
        self.runcmd(cmd)

    def check_permissions(self, pth, executable=False):
        si = os.stat(pth)

        if grp and ifroot():
            # check whether group owner is what we want
            usergroup = DEFAULTSECTION.get('usergroup')
            if grp.getgrgid(si.st_gid).gr_name != usergroup:
                if self.batch or self.yes_or_no(
                    "Set group owner for {} to '{}''".format(pth, usergroup),
                    default=True):
                    shutil.chown(pth, group=usergroup)

        # check access permissions
        mode = stat.S_IRGRP | stat.S_IWGRP
        mode |= stat.S_IRUSR | stat.S_IWUSR
        mode |= stat.S_IROTH
        if stat.S_ISDIR(si.st_mode):
            mode |= stat.S_ISGID | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        elif executable:
            mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        imode = stat.S_IMODE(si.st_mode)
        if imode ^ mode:
            msg = "Set mode for {} from {} to {}".format(
                pth, perm2text(imode), perm2text(mode))
            # pth, stat.filemode(imode), stat.filemode(mode))
            if self.batch or self.yes_or_no(msg, default=True):
                os.chmod(pth, mode)

    @contextmanager
    def override_batch(self, batch):
        old = self.batch
        try:
            self.batch = batch
            yield self
        finally:
            self.batch = old

    def write_file(self, pth, content, **kwargs):
        if self.check_overwrite(pth):
            with open(pth, 'w') as fd:
                fd.write(content)
            with self.override_batch(True):
                self.check_permissions(pth, **kwargs)
            return True

    def write_daily_cron_job(self, filename, content):
        fn = Path('/etc/cron.daily') / filename
        if fn.exists():
            return
        self.write_file(fn, content)
        self.check_permissions(fn, executable=True)

    def write_supervisor_conf(self, filename, content):
        self.write_file(
            Path(DEFAULTSECTION.get('supervisor_dir')) / filename, content)
        self.must_restart('supervisor')

    def make_file_executable(self,file_path):
        """ Make a file executable """
        st = os.stat(file_path)
        os.chmod(file_path,0o775)
        #os.chmod(file_path, st.st_mode | stat.S_IEXEC)

    def check_virtualenv(self, envdir, context):
        pull_sh_path = Path(envdir) / 'bin' / 'pull.sh'
        ok = False
        if os.path.exists(envdir):
            ok = True
            # msg = "Update virtualenv in {}"
            # return self.batch or click.confirm(msg.format(envdir), default=True)
        else:
            msg = "Create virtualenv in {}"
            if self.batch or self.yes_or_no(msg.format(envdir), default=True):
                # create an empty directory and fix permissions
                os.makedirs(envdir)
                self.check_permissions(envdir)
                virtualenv.cli_run([envdir,'--python','python3'])
                ok = True
        if ok:
            context.update(envdir=envdir)
            if not os.path.exists(pull_sh_path):
                self.jinja_write(pull_sh_path, **context)
            self.make_file_executable(pull_sh_path)
        return ok

    def clone_repo(self, repo):
        branch = DEFAULTSECTION.get('branch')
        if not os.path.exists(repo.nickname):
            self.runcmd("git clone --depth 1 -b {} {} {}".format(branch, repo.git_repo, repo.nickname))
        else:
            click.echo(
                "No need to clone {} : directory exists.".format(
                    repo.nickname))

    def install_repo(self, repo, env):
        self.run_in_env(env, "pip install -q -e {}".format(repo.nickname))

    def check_usergroup(self, usergroup):
        # not used since 20200720
        if ifroot():
            return
        if grp is None:
            return
        if has_usergroup(usergroup):
            return
        msg = """\
You {0} don't belong to the {1} user group.  Maybe you want to run:
sudo adduser `whoami` {1}"""
        raise click.ClickException(msg.format(getpass.getuser(), usergroup))

    def write_logrotate_conf(self, conffile, logfile):
        ctx = {}
        ctx.update(DEFAULTSECTION)
        ctx.update(logfile=logfile)
        self.write_file(
            '/etc/logrotate.d/' + conffile,
            LOGROTATE_CONF.format(**ctx))


    def jinja_write(self, pth, tplname=None, **context):
        """
        pth : the full path of the file to generate.
        tplname : name of the template file to render.  If tplname is not specified, use the tail of the output file.
        """
        if not self.check_overwrite(pth):
            return False
        if tplname is None:

            head, tplname = os.path.split(pth)
        tpl = JINJA_ENV.get_template(tplname)
        s = tpl.render(**context)
        with open(pth, 'w') as fh:
            fh.write(s)
        return True

    def run_apt_install(self):
        if len(self._system_packages) == 0:
            return
        cmd = "apt-get install -q "
        if self.batch:
            cmd += "-y "
        cmd +=  ' '.join(self._system_packages)
        self.runcmd_sudo("apt-get update -y", "apt-get upgrade -y", cmd)
        self._system_packages = []

    def restart_services(self):
        if len(self._services) == 0:
            return
        if not ifroot() and not has_usergroup('sudo'):
            click.echo(
                "The following system services were not "
                "restarted because you cannot sudo:\n{}".format(
                    ' '.join(list(self._services))))
            return
        msg = "Restart services {}".format(self._services)
        if self.batch or self.yes_or_no(msg, default=True):
            with self.override_batch(True):
                for srv in self._services:
                    try:
                        self.runcmd("sudo service {} restart".format(srv))
                    except Exception:
                        try:
                            self.runcmd("sudo /etc/init.d/{}  restart".format(srv))
                        except Exception:
                            continue
