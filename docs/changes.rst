.. _getlino.changes:

=======================
Changes in `getlino`
=======================

2019-09-02
==========

Also write logrotate config file for supervisor.

The default value for :option:`getlino configure --no-contrib` was wrong : when
running as root, it is not a contributor environment

.. command:: getlino configure

Changed some default values
in :cmd:`getlino configure`:
:option:`--shared-env`
and :option:`--repos-base` are now empty when
:envvar:`VIRTUAL_ENV` is not set.
:option:`--db-engine` is now mysql when running as root.


Released getlino 19.9.0 to PyPI.


2019-08-27
==========

Released getlino 19.8.1 on PyPI.

2019-08-01
==========

Released getlino 19.8.0 on PyPI.

2019-07-30
==========

Added a first meaningful unit test (:mod:`test_docker_prod`).
