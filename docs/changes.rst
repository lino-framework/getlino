.. _getlino.changes:

=======================
Changes in `getlino`
=======================

2021-04-12
==========

Updated the KNOWN_REPOS in :mod:`getlino.utils`: the following repositories have
moved to GitLab: lino, xl, noi, cosi, voga, avanti, welfare, weleup, welcht

2021-03-16
==========

You can now run :cmd:`getlino configure` as root with ``--clone`` and without
``--shared-env``, provided that you activated a virtualenv before calling
getlino.  In that case getlino will install clones into the current virtualenv
and store the current virtualenv in the system-wide config file. Miscellaneous
optimizations and bugfixes when setting up a demo server.

Release to PYPI.

More minor bugfixes: healthcheck.sh wasn't set to executable. configure failed
when --https was given but no --web-server


2021-03-14
==========

getlino forgot to run :command:`sudo ln -s /snap/bin/certbot /usr/bin/certbot`
when installing certbot.

2021-03-11
==========

When `--https` is specified but certbot is not installed, getlino now installs
it using snapd (no longer using wget and apt-get)

2021-03-08
==========

Release 21.3.0 to PyPI.

2021-03-05
==========

Optimization: When getlino asks to change file permissions, it now formats them
as "rwx" style strings instead of decimal integers.

2021-03-02
==========

Fixed #3998 (getlino says Invalid value for '--web-server': invalid choice: .
(choose from nginx, apache)). Reactivated UbuntuDockerTest in test suite.
getlino now upgrades the system not only when you are root but also when you are
member of sudo.  It no longer asks "Upgrade the system?" as a separate question,
only when it actually wants to install packages (and when you are either root or
sudoer).


2021-02-13
==========

Fixed a bug in the generated :xfile:`make_snapshot.sh` file: it was testing `if
[-f media/uploads]` instead of `if [-d media/uploads]`, as a result the uploads
were never included in the snapshot.

2021-02-12
==========

Fixed a problem when using apache config: certbot made a copy of the 80 conf
file, but failed to copy the WSGI* directives. Now getlino creates a 443 site
with snakeoil certificate already from the beginning. Added `uploads` to
:xfile:`make_snapshots.py`.

Released version 21.2.1 to PyPI.


2021-02-10
==========

Changed the number of nginx worker processes in the uwsgi.ini script from 2 to 1
as every worker process immobilizes about 5 to 6% of 2GB of RAM even when nobody
is using the site.

Added support for apache web server.  Until now, getlino always installed nginx
(when running as root). Now :cmd:`getlino configure` has a new option
`--web-server`, which can be "nginx", "apache" or empty. Changed behaviour: When
not given, getlino will not setup any web server configuration, even when
running as root.

The test suite now also tests for "ERROR" (not just "Error") in the output of
:xfile:`healthcheck.sh`. Increased the wait time for supervisor to restart from
10 to 20 seconds because with only 10 seconds it failed once.

Released version 21.2.0 to PyPI.

2021-02-08
==========

Fixed several minor bugs in `getlino startsite`: Fixed a typo bug that caused
``--https`` to fail at the last step (when calling certbot for the new
subdomain). Some config files were generated with a leading newline, and the
make_snapshot cron job even with leading blanks on every line. The
:xfile:`nginx.conf` file was still pointing ``/static/``  to a directory static,
but the new default name for this is :xfile:`static_root`.

2020-09-23
==========

getlino configure now again installs (or instructs to install) apt packages
libldap2-dev and libsasl2-dev, which are --as it seems-- required for
django_auth_ldap.

2020-09-21
==========

When invoking getlino configure without sudo, it no longer asks for
`--usergroup`.

Released getlino 20.9.0 to PyPI.

2020-09-02
==========

getlino can now install certbot either using the Debian packager or using
certbot-auto. getlino now supports calling :meth:`Installer.run_apt_install`
more than once during an installation session.

2020-08-27
==========

:cmd:`getlino startsite` has now the database options (db-engine, db-user etc)
so that you can override them per site without needing to run getlino configure.
Added a new choice :mod:`lino.projects.std` for the `APPNAME` argument of
:cmd:`getlino startsite`. Fixed a warning :message:`bash: warning: setlocale:
LC_ALL: cannot change locale (en_US.UTF-8)` during test run.


2020-07-29
==========

Released getlino 20.7.5 to PyPI. With a few bugfixes.

2020-07-20
==========

Released getlino 20.7.3 to PyPI. After some subtle changes.

Released getlino 20.7.4 to PyPI. After some more subtle changes.

2020-07-19
==========

Released getlino 20.7.2 to PyPI.


2020-07-17
==========

getlino failed on Python 3.8 because it was using the deprecated
:attr:`platform.dist`. Now it uses :mod:`distro`.

getlino now shows its version.

Released getlino 20.7.1 to PyPI.

local-prefix was root_only, which caused configure to fail when not run as root.

2020-07-16
==========

getlino failed on Windows because the grp module is not available there. Now we
simply skip the group ownership check when running on Windows.

Reorganized the Docker files.

Released getlino 20.7.0 to PyPI.

2020-06-23
==========

:cmd:`getlino startsite` now creates a daily cron job that runs
:xfile:`make_snapshot.sh`.


2020-05-14
==========

Remove useless command to copy "mysql_config" file for MariaDB.

2020-05-14
==========

.. program:: getlino configure

Bugfix : :cmd:`getlino configure` without `--clone`, the `--shared-env` now
defaults to an empty string.


2020-05-04
==========
:cmd:`getlino configure` now defaults :option:`--shared-env` to the current
:envvar:`VIRTUAL_ENV` only when :option:`--clone` was given, not always.
And it creates the ``repos_base`` only then.

2020-04-07
==========
Fix typo with apt_packages of DbEngine.
Release 20.4.5 version to PyPI.

2020-04-03
==========
Remove certbot for www domain
Release 20.4.3 version to PyPI.

2020-04-03
==========
Update the virualenv usage.
Fix issue with installing mariadb for debian distribution instead of mysql


2020-01-03
==========
Add the ciao projet to KNOWN_REPOS.
Add 'sudo' to the certbot command.

Fix some issues with creating user and database with the :cmd:`getlino startsite` .

Released version 20.1 to PyPI
Released version 20.1.1 to PyPI

No need for 'sudo' for certbot command

Released version 20.1.2 to PyPI


2019-11-23
==========
When the user is not root , the :cmd:`getlino startsite` command doesn't create
the :xfile:`make_snapshot.sh` and the directory `nginx`.


2019-11-09
==========

The :xfile:`pull.sh` script generated by :cmd:`getlino configure` into the
shared virtualenv was still using the project_dir.


2019-11-07
==========

.. program:: getlino configure

The :option:`--https` option was appending directly to the
main :file:`/etc/crontab` file. Fixed.

Fixed some minor bugs.  For example the :option:`--redis` option
was ignored when not running as root.

Released 19.11.0 to PyPI.

2019-11-06
==========

:cmd:`getlino configure --db-user` option now creates the shared database user.
The items of :data:`getlino.utils.DB_ENGINES` are no longer named tuples but
real objects with methods.


2019-10-25
==========

getlino no longer depends on cookiecutter. The separate cookiecutter-startsite
repository is no longer used because all templates are now below
:file:`getlino/templates`.

Released version 19.10.6 to PyPI (versions 19.10.3 to 19.10.5 are broken
versions, don't use them).


2019-10-08
==========

Released version 19.10.0 to PyPI.

.. program:: getlino configure

Fixed some bugs: Running :command:`getlino configure` without
:option:`--db-port` caused an error :message:`Invalid value for "--db-port":
invalid choice: . (choose from 5432, 3306, 0)`. The :option:`--db-port` option
is no longer a choice (it is not limited to these values). The :option:`--clone`
option sometimes had `True` as default value when it shouldn't.

Released version 19.10.1 to PyPI.

Found another bug: with :option:`--clone`, getlino didn't clone the repositories
using their nickname, which later caused failures when trying to install them.

Released version 19.10.2 to PyPI.

.. program:: getlino configure

Fixed some more bugs: Running :command:`getlino configure` without
:option:`--db-port` caused an error :message:`Invalid value for "--db-port":
invalid choice: . (choose from 5432, 3306, 0)`. The :option:`--db-port` option
is not a choice (it must not limited to these values). The :option:`--clone`
option sometimes had `True` as default value.


2019-10-03
==========

.. program:: getlino configure

The :option:`--db-port` shows the default ports of databases.


2019-09-19
==========

.. program:: getlino configure

The :option:`--clone` option installs all contributor
repositories, i.e. those  required to build the book. Some repositories were
still missing. Fixed.  Also separated the sequence of resulting actions: first
run "git clone" for all repos, then "pip install -e".

2019-09-18
==========

.. program:: getlino configure

Optimized behaviour when running as non-root:
The default value for :option:`--devtools` is now `True` in that case.
:option:`--db-engine` had a wrong default value "sqlite" (must be "sqlite3"),
getlino tried to create the directories given by
:option:`--log-base` and :option:`--backups-base` (which failed because not
running as root).

2019-09-14
==========

.. program:: getlino configure

When running as root, :cmd:`getlino configure` now also creates empty
directories for :option:`--log-base` and :option:`--backups-base` and sets their
permissions.

2019-09-12
===========

When running as root, getlino now also installs the `build-essential` Debian
package because this is maybe needed for installing Python extensions.

getlino didn't set the group owner in some cases (e.g. the lino_local directory
and a project's virtualenv).

:cmd:`getlino configure` now also creates a :xfile:`~/.bash_aliases` file. But
only when you aren't running as root. After running :cmd:`getlino configure` as
root, you may want to run it once more without being root to create a
:xfile:`.bash_aliases` file to your home directory.

Released getlino 19.9.6 to PyPI, immediately followed by a bug-fix release
19.9.7

2019-09-09
==========

Added more demo projects to be used by the getlino configure command.
Released getlino 19.9.5.

2019-09-08
==========

.. program:: getlino configure

Renamed the ``--contrib`` option  to :option:`--clone` because it is also used
when configuring a :term:`demo server`. It means "clone all known repositories
to the --repos-base and install them to the shared-env using :cmd:`pip -e`."
This change requires that you run :cmd:`getlino configure` once after upgrade,
or manually edit your getlino config file.

The configure command now supports :option:`--clone` without specifying a
--repos-base. In that case it uses the `repositories` subdir of the shared-env.

.. program:: getlino startsite

New option :option:`--shared-env` for startsite.  When used with startsite, it
overrides the value specified during configure.

Released getlino 19.9.4 on PyPI.

2019-09-07
==========

Released getlino 19.9.2 on PyPI, followed by a bugfix release 19.9.3.

2019-09-02
==========

Also write logrotate config file for supervisor.

.. program:: getlino configure

Changed some default values
in :cmd:`getlino configure`:
The default value for :option:`--clone` was wrong : when
running as root, it is *not* a contributor environment.
:option:`--shared-env`
and :option:`--repos-base` are now empty when
:envvar:`VIRTUAL_ENV` is not set.
And :option:`--db-engine` is now mysql when running as root.

Released getlino 19.9.0 to PyPI, followed by a bugfix release 19.9.1.


2019-08-27
==========

Released getlino 19.8.1 on PyPI.

2019-08-01
==========

Released getlino 19.8.0 on PyPI.

2019-07-30
==========

Added a first meaningful unit test (:mod:`test_docker_prod`).
