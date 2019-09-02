.. _getlino.changes:

=======================
Changes in `getlino`
=======================

2019-09-02
==========

Also write logrotate config file for supervisor.

.. program:: getlino configure

Changed some default values
in :cmd:`getlino configure`:
The default value for :option:`--contrib` was wrong : when
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
