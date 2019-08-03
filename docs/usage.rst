.. _getlino.usage:

=====
Usage
=====


The :cmd:`getlino configure` command
====================================

.. program:: getlino configure

The :cmd:`getlino configure` command configures your machine as a :term:`Lino
server`.  This is required before you can run :cmd:`startsite`.

If you run this command as root (using :cmd:`sudo`), it will also install system
packages and system-wide configuration files, turning the machine into a
**production server**.  Otherwise it will install Lino into a  **virtual
environment**. If you want Lino to install into an existing enviroment, you
should activate it before running :cmd:`getlino configure` in order to use it as
the default value for :option:`--shared-env`.

:cmd:`getlino configure` asks a lot of questions, one question for each server
configuration option. Read the docs below for more explanations. You can answer
ENTER to each question if your don't care.

:cmd:`getlino configure` creates or reads and updates a configuration file where
it stores  your answers.  Depending on whether you are root, the configuration
file will be either :xfile:`/etc/getlino/getlino.conf` or
:xfile:`~/.getlino.conf`.

If you specify :option:`--batch`, every option gets its default value, which you
may override by specifying command-line arguments. Use this option only when you
really know that you want it (e.g. in a Dockerfile).


.. command:: getlino configure

    Install the Lino framework on this machine.

    Run-time options:

    .. option:: --batch

        Run in batch mode, i.e. without asking any questions.
        Assume yes to all questions.
        

    .. rubric:: Server configuration options

    .. option:: --contrib

        Configure a contributor environment. Install a clone of all repositories
        to your ``--repos-base`` and use these for new sites.

    .. option:: --shared-env

        Full path to your default virtualenv.

    .. option:: --repos-base

        Base directory for your shared repositories.  This is where getlino
        should clone repositories of packages to be used in editable mode
        ("development version") specified by :option:`getlino startsite --dev-repos`.

        If this is empty and a site requests a development version, this will
        be stored in a directory named :option:`--repos-link` below the virtualenv dir.

    .. option:: --sites-base

        The root directory for sites on this server.

        This will be added to the :envvar:`PYTHONPATH` of every Lino process
        (namely in :xfile:`manage.py` and :xfile:`wsgi.py`).

        The :envvar:`PYTHONPATH` is needed because the :xfile:`settings.py` of
        a site says ``from lino_local.settings import *``, and the
        :xfile:`manage.py` sets :setting:`DJANGO_SETTINGS_MODULE` to
        ``'lino_local.mysite1.settings'``.

    .. option:: --env-link

        Relative directory or symbolic link to the virtualenv.

    .. option:: --local-prefix

        Prefix for local server-wide importable packages.

    .. option:: --backups-base

        Base directory for backups

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

    .. option:: --db-user

        A database username to use for all sites on this server.

        If this is set, you should also set :option:`--db-password`.

        Used during development and testing when you prefer to have a single
        database user for all databases. For security reasons these options
        should not be used on a production server.

    .. option:: --db-password

        The password for the :option:`--db-user`.



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
        <https://wiki.debian.org/FreedomBox/Manual/DynamicDNS>`__or `dynu.com
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

    .. option:: --asroot

        Whether you have root permissions and want to install system packages.

    .. option:: --dev-repos

        A space-separated list of repositories for which this site uses the
        development version (i.e. not the PyPI release).

        Usage example::

            $ getlino startsite avanti mysite --dev-repos "lino xl"


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


Notes
=====
