.. _getlino.install:

==================
Installing getlino
==================


**On a production server** you must install getlino into the system-wide Python
3 environment.

Either the officially stable version::

   $ sudo pip3 install getlino

Or the development version::

   $ sudo pip3 install -e git+https://github.com/lino-framework/getlino.git#egg=getlino


**On a development machine** you can use getlino to simply configure a
development environment. In that case you don't need root privileges.

Make sure your default working environment is activated.

We recommend to install your own local clone::

   $ cd ~/repositories
   $ git clone git@github.com:lino-framework/getlino.git
   $ pip install -e getlino

Or the officially stable version::

   $ pip install getlino

Or a snapshot the development version::

   $ pip install -e git+https://github.com/lino-framework/getlino.git#egg=getlino


.. _ss:

The ``startsite`` template
==========================

The `cookiecutter-startsite
<https://github.com/lino-framework/cookiecutter-startsite>`__ project contains
a cookiecutter template used by :cmd:`getlino startsite`.


Notes
=====

When you maintain a Lino server, then you don't want to decide for each new
site which database engine to use. You decide this once for all during
:cmd:`getlino configure`. In general, `apt-get install` is called only during
:cmd:`getlino configure`, never during :cmd:`getlino startsite`. If you have a
server with some mysql sites and exceptionally want to install a site with
postgres, you simply call :cmd:`getlino configure` before calling
:cmd:`getlino startsite`.
