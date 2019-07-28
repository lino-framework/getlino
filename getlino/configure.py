# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import os
import sys
import stat
import shutil
import grp
import configparser
import subprocess
import virtualenv
import click
import collections
from contextlib import contextmanager

from os.path import join

from .utils import CONFIG, CONF_FILES, FOUND_CONFIG_FILES, DEFAULTSECTION
from .utils import DB_ENGINES, BATCH_HELP, ASROOT_HELP
from .utils import Installer


CERTBOT_AUTO_RENEW = """
echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && /usr/local/bin/certbot-auto renew" | tee -a /etc/crontab > /dev/null
"""
HEALTHCHECK_SH = """
#!/bin/bash
# generated by getlino
set -e  # exit on error
echo -n "Checking supervisor status: "
supervisorctl status | awk '{if ( $2 != "RUNNING" ) { print "ERROR: " $1 " is not running"; exit 1}}'
echo "... OK"
"""

MONIT_CONF = """
# generated by getlino
check program status with path /usr/local/bin/healthcheck.sh
    if status != 0 then alert
"""

LIBREOFFICE_SUPERVISOR_CONF = """
# generated by getlino
[program:libreoffice]
command = libreoffice --accept="socket,host=127.0.0.1,port=8100;urp;" --nologo --headless --nofirststartwizard
umask = 0002
"""

LOCAL_SETTINGS = """
# generated by getlino
ADMINS = [ 
  ["{admin_name}", "{admin_email}"] 
]
EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'noreply@{server_domain}'
DEFAULT_FROM_EMAIL = 'noreply@{server_domain}'
STATIC_ROOT = 'env/static'
TIME_ZONE = "{time_zone}"
"""



# The configure command will be decorated below. We cannot use decorators
# because we define the list of options in CONFIGURE_OPTIONS because we need
# that list also for asking questions using the help text.

CONFIGURE_OPTIONS = []


def add(spec, default, help, type=None):
    kwargs = dict()
    kwargs.update(help=help)
    if type is not None:
        kwargs.update(type=type)
    o = click.Option([spec], **kwargs)
    o.default = DEFAULTSECTION.get(o.name, default)
    CONFIGURE_OPTIONS.append(o)

def default_projects_root():
    if os.access('/usr/local', os.W_OK):
        return '/usr/local/lino'
    return os.path.expanduser('~/lino')

def default_shared_env():
    return os.environ.get('VIRTUAL_ENV', '/usr/local/lino/shared/env')

# must be same order as in signature of configure command below
# add('--prod/--no-prod', True, "Whether this is a production server")
add('--projects-root', default_projects_root, 'Base directory for Lino sites')
add('--local-prefix', 'lino_local', "Prefix for for local server-wide importable packages")
add('--shared-env', default_shared_env, "Directory with shared virtualenv")
add('--repositories-root', '', "Base directory for shared code repositories")
add('--webdav/--no-webdav', True, "Whether to enable webdav on new sites.")
add('--backups-root', '/var/backups/lino', 'Base directory for backups')
add('--log-root', '/var/log/lino', 'Base directory for log files')
add('--usergroup', 'www-data', "User group for files to be shared with the web server")
add('--supervisor-dir', '/etc/supervisor/conf.d',
    "Directory for supervisor config files")
add('--db-engine', 'sqlite3', "Default database engine for new sites.",
    click.Choice([e.name for e in DB_ENGINES]))
add('--db-port', 3306, "Default database port for new sites.")
add('--db-host', 'localhost', "Default database host name for new sites.")
add('--env-link', 'env', "link to virtualenv (relative to project dir)")
add('--repos-link', 'repositories', "link to code repositories (relative to virtualenv)")
add('--appy/--no-appy', True, "Whether this server provides appypod and LibreOffice")
add('--redis/--no-redis', True, "Whether this server provides redis")
add('--devtools/--no-devtools', False,
    "Whether this server provides developer tools (build docs and run tests)")
add('--server-domain', 'localhost', "Domain name of this server")
add('--https/--no-https', False, "Whether this server uses secure http")
add('--monit/--no-monit', True, "Whether this server uses monit")
add('--admin-name', 'Joe Dow', "The full name of the server administrator")
add('--admin-email', 'joe@example.com',
    "The email address of the server administrator")
add('--time-zone', 'Europe/Brussels', "The TIME_ZONE to set on new sites")


def configure(ctx, batch, asroot,
              projects_root, local_prefix, shared_env, repositories_root,
              webdav, backups_root, log_root, usergroup,
              supervisor_dir, db_engine, db_port, db_host, env_link, repos_link,
              appy, redis, devtools, server_domain, https, monit,
              admin_name, admin_email, time_zone):
    """
    Edit and/or create a configuration file and
    set up this machine to become a Lino production server
    according to the configuration file.
    """

    if len(FOUND_CONFIG_FILES) > 1:
        # reconfigure is not yet supported
        raise click.UsageError("Found multiple config files: {}".format(
            FOUND_CONFIG_FILES))

    i = Installer(batch, asroot)

    if asroot:
        conffile = CONF_FILES[0]
    else:
        conffile = CONF_FILES[1]

    # # write config file. if there is no system-wide file but a user file, write
    # # the user file. Otherwise write the system-wide file.
    # if len(FOUND_CONFIG_FILES) == 1:
    #     conffile = FOUND_CONFIG_FILES[0]
    #     msg = "This will update configuration file {}"
    # else:
    #     msg = "This will create configuration file {}"

    # before asking questions check whether we will be able to store them
    click.echo("This will write configuration file {}".format(conffile))
    pth = os.path.dirname(conffile)
    if not os.path.exists(pth):
        os.makedirs(pth, exist_ok=True)

    pth = os.path.dirname(conffile)
    if not os.access(pth, os.W_OK):
        raise click.ClickException(
            "No write permission for directory {}".format(pth))

    if os.path.exists(conffile) and not os.access(conffile, os.W_OK):
        raise click.ClickException(
            "No write permission for file {}".format(conffile))

    for p in CONFIGURE_OPTIONS:
        k = p.name
        v = locals()[k]
        if batch:
            CONFIG.set(CONFIG.default_section, k, str(v))
        else:
            msg = "- {} ({})".format(k, p.help)
            kwargs = dict(default=v)
            if p.type is not None:
                kwargs.update(type=p.type)
            answer = click.prompt(msg, **kwargs)
            # conf_values[k] = answer
            CONFIG.set(CONFIG.default_section, k, str(answer))

    if not i.yes_or_no("Okay to configure your system using above options? [y or n]"):
        raise click.Abort()

    with open(conffile, 'w') as fd:
        CONFIG.write(fd)
    click.echo("Wrote config file " + conffile)

    if DEFAULTSECTION.getboolean('monit'):
        i.write_file('/usr/local/bin/healthcheck.sh', HEALTHCHECK_SH, executable=True)
        i.write_file('/etc/monit/conf.d/lino.conf', MONIT_CONF)

    # pth = "/etc/default/nginx"
    # content = open(pth, "r").read()
    # if not "umask" in content:
    #     content += """\n# added by getlino\numask 0002\n"""
    #     if i.write_file(pth, content):
    #         i.must_restart("nginx")

    pth = DEFAULTSECTION.get('projects_root')
    if os.path.exists(pth):
        i.check_permissions(pth)
    elif batch or click.confirm("Create projects root directory {}".format(pth), default=True):
        os.makedirs(pth, exist_ok=True)
        i.check_permissions(pth)

    local_prefix = DEFAULTSECTION.get('local_prefix')
    pth = join(DEFAULTSECTION.get('projects_root'), local_prefix)
    if os.path.exists(pth):
        i.check_permissions(pth)
    elif batch or click.confirm("Create shared settings package {}".format(pth), default=True):
        os.makedirs(pth, exist_ok=True)
    with i.override_batch(True):
        i.check_permissions(pth)
        i.write_file(join(pth, '__init__.py'), '')
    i.write_file(join(pth, 'settings.py'),
                 LOCAL_SETTINGS.format(**DEFAULTSECTION))

    if asroot:
        if batch or click.confirm("Upgrade the system", default=True):
            with i.override_batch(True):
                i.runcmd("apt-get update")
                i.runcmd("apt-get upgrade")

    i.apt_install(
        "git subversion python3 python3-dev python3-setuptools python3-pip supervisor")

    if asroot:
        i.apt_install("nginx uwsgi-plugin-python3")
        i.apt_install("logrotate")

    if DEFAULTSECTION.getboolean('devtools'):
        i.apt_install("tidy swig graphviz sqlite3")

    if DEFAULTSECTION.getboolean('monit'):
        i.apt_install("monit")

    if DEFAULTSECTION.getboolean('redis'):
        i.apt_install("redis-server")

    for e in DB_ENGINES:
        if DEFAULTSECTION.get('db_engine') == e.name:
            i.apt_install(e.apt_packages)

    if DEFAULTSECTION.getboolean('appy'):
        i.apt_install("libreoffice python3-uno")

    i.finish()

    if DEFAULTSECTION.get('db_engine') == 'mysql':
        i.runcmd("mysql_secure_installation")

    if DEFAULTSECTION.getboolean('appy'):
        i.write_supervisor_conf(
            'libreoffice.conf',
            LIBREOFFICE_SUPERVISOR_CONF.format(**DEFAULTSECTION))

    if DEFAULTSECTION.getboolean('https'):
        if shutil.which("certbot-auto"):
            click.echo("certbot-auto already installed")
        elif batch or click.confirm("Install certbot-auto ?", default=True):
            with i.override_batch(True):
                i.runcmd("wget https://dl.eff.org/certbot-auto")
                i.runcmd("mv certbot-auto /usr/local/bin/certbot-auto")
                i.runcmd("chown root /usr/local/bin/certbot-auto")
                i.runcmd("chmod 0755 /usr/local/bin/certbot-auto")
                i.runcmd("certbot-auto -n")
                i.runcmd("certbot-auto register --agree-tos -m {} -n".format(DEFAULTSECTION.get('admin_email')))
        if batch or click.confirm("Set up automatic certificate renewal ", default=True):
            i.runcmd(CERTBOT_AUTO_RENEW)

    click.echo("Lino server setup completed.")

params = [
    click.Option(['--batch/--no-batch'], default=False, help=BATCH_HELP),
    click.Option(['--asroot/--no-asroot'], default=False, help=ASROOT_HELP)
] + CONFIGURE_OPTIONS
configure = click.pass_context(configure)
configure = click.Command('configure', callback=configure,
                          params=params, help=configure.__doc__)



