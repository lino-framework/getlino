.. _getlino.install:

==================
Installing getlino
==================

Install
=======

The easiest way to install getlino is via pip::

  $ pip install getlino

To update your getlino to the newest version simply run::

  $ pip install -U getlino`


More options
============

You can optionally use the development version::

  $ pip uninstall getlino
  $ pip install -e git+https://github.com/lino-framework/getlino.git#egg=getlino

You may install your own local clone of getlino::

   $ cd ~/lino/env/repositories
   $ git clone git@github.com:lino-framework/getlino.git
   $ pip install -e getlino

In that last use case don't forget to manually add getlino to your
:xfile:`./atelier/config.py` file.
