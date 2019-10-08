.. _getlino.usage:

=====
Usage
=====


The :cmd:`getlino configure` command
====================================

.. program:: getlino configure

The :cmd:`getlino configure` command configures your machine as a :term:`Lino
server`.  This is required before you can run :cmd:`startsite`.

If you run this command as root (using :cmd:`sudo`), it will turn the machine
into a :term:`production server` or a :term:`demo server` by also installing
system packages and system-wide configuration files.  Otherwise it will install
Lino into a **virtual environment**. If you want Lino to install into an
existing virtual environment, you should activate it before running
:cmd:`getlino configure` in order to use it as the default value for
:option:`--shared-env`.

:cmd:`getlino configure` asks a lot of questions, one question for each server
configuration option. Read the docs below for more explanations. You can answer
ENTER to each question if your don't care.

:cmd:`getlino configure` creates or reads and updates a configuration file where
it stores your answers.  Depending on whether you are root, the configuration
file will be either :xfile:`/etc/getlino/getlino.conf` or
:xfile:`~/.getlino.conf`.

If you specify :option:`--batch`, every option gets its default value, which you
may override by specifying command-line arguments. Use this option only when you
know what you want (e.g. in a Dockerfile).

After running :cmd:`getlino configure` as root, you may want to run it once more
without being root, because only then it will also write a
:xfile:`.bash_aliases` file in your home directory.


.. command:: getlino configure

    Install the Lino framework on this machine.

    Run-time options:

    .. option:: --batch

        Run in batch mode, i.e. without asking any questions.
        Assume yes to all questions.


    .. rubric:: Server configuration options

    .. option:: --shared-env

        Full path to your default virtualenv.
        Default value is taken from :envvar:`VIRTUAL_ENV` environment value.
        If this is empty, every new site  will get its own virgin environment.

    .. option:: --repos-base

        Base directory for your shared repositories.  This is where getlino
        should clone repositories of packages to be used in editable mode
        ("development version") specified by :option:`getlino startsite --dev-repos`.

        If this is empty and a site requests a development version, this will
        be stored in a directory named :option:`--repos-link` below the virtualenv dir.

    .. option:: --clone

        Clone all known repositories to your ``--repos-base`` and install them
        into your ``--shared-env``. Used when configuring a :term:`contributor
        environment` or a :term:`demo server`.

    .. option:: --branch

        The git branch to use for :option:`--clone`.

    .. option:: --devtools

        Whether to install development tools (used to build docs and run tests).

    .. option:: --log-base

        The root directory for Lino's log files on this server.  Each new site
        will get its entry below that directory.

    .. option:: --backups-base

        The root directory for backups on this server.  Each new site will get
        its entry below that directory.  Used e.g. by :xfile:`make_snapshot.sh`.

    .. option:: --sites-base

        The root directory for sites on this server.

        New sites will get created below that directory (with another level
        named by :option:`--local-prefix`).

        This will be added to the :envvar:`PYTHONPATH` of every Lino process
        (namely in :xfile:`manage.py` and :xfile:`wsgi.py`).

        The :envvar:`PYTHONPATH` is needed because the :xfile:`settings.py` of
        a site says ``from lino_local.settings import *``, and the
        :xfile:`manage.py` sets :setting:`DJANGO_SETTINGS_MODULE` to
        ``'lino_local.mysite1.settings'``.

    .. option:: --local-prefix

        Prefix for local server-wide importable packages.

    .. option:: --env-link

        Relative directory or symbolic link to the virtualenv.

    .. option:: --repos-link

        Relative directory or symbolic link to repositories.

    .. option:: --server-domain

        Fully qualified domain name of this server.  Default is 'localhost'.

    .. rubric:: Default settings for new sites

    .. option:: --front-end

        Which front end (:attr:`default_ui <lino.core.Site.default_ui>`) to use
        on new sites.

    .. option:: --languages

        Default value for :attr:`languages <lino.core.site.Site.languages>` of
        new sites.

    .. option:: --linod

        Whether new sites should have a :xfile:`linod.sh` script which runs the
        :manage:`linod` command.

        When running as root, this will also add a :mod:`supervisor`
        configuration file which runs the :manage:`linod` command automatically.

    .. option:: --db-engine

        Default value is 'mysql' when running as root or 'sqlite3' otherwise.

    .. option:: --db-user

        A database username to use for all sites on this server.

        If this is set, you should also set :option:`--db-password`.

        Used during development and testing when you prefer to have a single
        database user for all databases. For security reasons these options
        should not be used on a production server.

    .. option:: --db-password

        The password for the :option:`--db-user`.

    .. option:: --db-port

        The port to use for connecting to the database server when
        :option:`--db-engine` is ``mysql`` or ``postgresql``.

    .. rubric:: Server features

    .. option:: --appy

        Whether this server provides LibreOffice service needed by sites which
        use :mod:`lino_xl.lib.appypod`.

    .. option:: --webdav

        Whether new sites should have webdav.

    .. option:: --https

        Whether this server provides secure http.

        This option will cause getlino to install certbot.

        When you use this option, you must have your domain name
        (:option:`--server-domain`) registered so that it points to the server.
        If your server has a dynamic IP address, you may use some dynamic DNS
        service like `FreedomBox
        <https://wiki.debian.org/FreedomBox/Manual/DynamicDNS>`__ or `dynu.com
        <https://www.dynu.com/DynamicDNS/IPUpdateClient/Linux>`__.


..
  --log-root TEXT                 Base directory for log files
  --usergroup TEXT                User group for files to be shared with the
                                  web server
  --supervisor-dir TEXT           Directory for supervisor config files
  --db-engine [postgresql|mysql|sqlite3]
                                  Default database engine for new sites.
  --db-port TEXT                  Default database port for new sites.
  --db-host TEXT                  Default database host name for new sites.
  --env-link TEXT                 link to virtualenv (relative to project dir)
  --repos-link TEXT               link to code repositories (relative to
                                  virtualenv)
  --appy / --no-appy              Whether this server provides appypod and
                                  LibreOffice
  --redis / --no-redis            Whether this server provides redis
  --devtools / --no-devtools      Whether this server provides developer tools
                                  (build docs and run tests)
  --server-domain TEXT            Domain name of this server
  --https / --no-https            Whether this server uses secure http
  --monit / --no-monit            Whether this server uses monit
  --admin-name TEXT               The full name of the server administrator
  --admin-email TEXT              The email address of the server
                                  administrator
  --time-zone TEXT                The TIME_ZONE to set on new sites
  --help                          Show this message and exit.





The :cmd:`getlino startsite` command
====================================

.. program:: getlino startsite

Usage::

   $ sudo -H getlino startsite appname prjname [options]

The ``-H`` option instructs :cmd:`sudo` to use your home directory for caching
its downloads.  You will appreciate this when you run the command a second
time.

The script will ask you some questions:

- appname is the Lino application to run

- prjname is the internal name, it must be unique for this Lino server. We
  recommend lower-case only and no "-" or "_", maybe a number.  Examples:  foo,
  foo2, mysite, first,


.. command:: getlino startsite

    Create a new Lino site.

    Usage: getlino startsite [OPTIONS] APPNAME PRJNAME

    Arguments:

    APPNAME : The application to run on the new site.

    SITENAME : The name for the new site.

    .. option:: --batch

        Don't ask anything. Assume yes to all questions.

    .. option:: --dev-repos

        A space-separated list of repositories for which this site uses the
        development version (i.e. not the PyPI release).

        Usage example::

            $ getlino startsite avanti mysite --dev-repos "lino xl"

        Not that the sort order is important. The following would not work::

            $ getlino startsite avanti mysite --dev-repos "xl lino"

    .. option:: --shared-env

        Full path to the shared virtualenv to use for this site.
        Default value is the value specified during :option:`getlino configure --shared-env`
        If this is empty, the new site will get its own virgin environment.


Configuration files
===================

.. xfile:: ~/.getlino.conf
.. xfile:: /etc/getlino/getlino.conf



Multiple database engines on a same server
==========================================

Note that :cmd:`getlino startsite` does not install any db engine because this
is done by :cmd:`getlino configure`.

When you maintain a Lino server, you don't want to decide for each new site
which database engine to use. You decide this once during :cmd:`getlino
configure`. In general, `apt-get install` is called only during :cmd:`getlino
configure`, never during :cmd:`getlino startsite`. If you have a server with
some mysql sites and exceptionally want to install a site with postgres, you
simply call :cmd:`getlino configure` before calling :cmd:`getlino startsite`.

You may use multiple database engines on a same server by running configure
between startsite invocations.

.. _ss:

The ``startsite`` template
==========================

The `cookiecutter-startsite
<https://github.com/lino-framework/cookiecutter-startsite>`__ project contains
a cookiecutter template used by :cmd:`getlino startsite`.


Shared virtual environments
===========================

You can run multiple sites on a same virtualenv.  That virtualenv is then called
a shared environment.

Note that if you update a shared virtualenv (by activating it and running some
pip command), the change will affect all sites and you must take special care
for migrating their data if needed.

In a :term:`developer environment` and a :term:`contributor environment` you
usually have a single shared env used by all your sites.  On a :term:`production
server` you usually have no shared-env at all (each production site has its own
env). On a :term:`demo server` you usually hav several shared envs:

- /usr/local/lino/sharedenvs/master
- /usr/local/lino/sharedenvs/stable

You can specify a *default* shared environment with
:option:`getlino configure --shared-env`
:option:`getlino startsite --shared-env`.

Note that :option:`getlino configure --clone`) will install all known framework
repositories into the default shared env.

:cmd:`getlino startsite` does not install any Python packages when a shared env
is used.
