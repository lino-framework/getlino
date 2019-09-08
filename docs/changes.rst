.. _getlino.changes:

=======================
Changes in `getlino`
=======================

2019-09-08
==========

.. program:: getlino configure

Renamed the ``--contrib`` option  to :option:`--clone` because it is also used
when configuring a :term:`demo server`. It means "clone all known repositories
to the --repos-base and install them to the shared env using :cmd:`pip -e`."
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
