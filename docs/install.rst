.. _getlino.install:

===============
Installing Lino
===============

This page explains how to install Lino on your computer. There are several
recipes, depending on what you want to do. Choose the one which matches your
needs:


.. glossary::

  Developer environment

    A set of utilities on your computer, to be used for developing your own
    :term:`Lino application`.

    See :ref:`getlino.install.dev`.

  Contributor environment

    An extended :term:`developer environment` for developers who plan to
    potentially contribute to the :term:`Lino framework`.  A bit more work to
    install, but more future-proof.

    See :ref:`getlino.install.dev`.

  Production server

    A server with one or several :term:`Lino sites <Lino site>` in
    :term:`production` mode for yourself or your customers.

    See :ref:`getlino.install.prod`.

  Demo server

    See :ref:`getlino.install.demo`.


.. _getlino.install.dev:

Configure a Lino developer environment
======================================

Create a new virtual environment and activate it::

  $ sudo apt-get install -y python3-pip
  $ mkdir ~/lino
  $ cd ~/lino
  $ virtualenv -p python3 env
  $ . env/bin/activate

Install getlino::

  $ pip install getlino

Optionally use the development version::

  $ pip uninstall getlino
  $ pip install -e git+https://github.com/lino-framework/getlino.git#egg=getlino

Run :cmd:`getlino configure` and :cmd:`getlino startsite`::

  $ getlino configure --sites-base .
  $ getlino startsite noi first

Run :manage:`runserver`::

  $ cd first
  $ python manage.py runserver

Point your browser to http://localhost:8000

Continue here: http://www.lino-framework.org/dev/index.html

.. _getlino.install.contrib:

Configure a Lino contributor environment
========================================

Activate the virtual environment you want to use for your Lino projects::

  $ . path/to/my/virtualenv/bin/activate

Install getlino::

  $ pip install -e git+https://github.com/lino-framework/getlino.git#egg=getlino

Run :cmd:`getlino configure` ::

  $ getlino configure --contrib

Try one of the demo projects::

  $ go team
  $ pm prep
  $ pm runserver

Point your browser to http://localhost:8000

Continue here:  http://www.lino-framework.org/team/index.html

.. _getlino.install.prod:
.. _getlino.install.admin:

Configure a Lino production server
==================================

You need shell access to a **Linux machine**, i.e. a virtual or physical machine
with a Linux operating system running in a network. We recommend a **stable
Debian** as operating system.   We will install a series of system packages like
Python, nginx, monit, a database server (MySQL or PostGreSQL) on your machine.

Install pip::

  $ sudo apt-get install -y python3-pip

Install getlino into the system-wide Python 3 environment::

   $ sudo -H pip3 install getlino

Run :cmd:`getlino configure` as root::

   $ sudo -H getlino configure

Install a first site.  You will do the following for every new site on your
server.

   $ sudo -H getlino startsite noi first

Point your browser to http://first.localhost

If your customers want to access their Lino from outside of their intranet, then
you need to setup a domain name and add use the :option:`getlino configure
--https` option in above command line.

Continue here:  http://www.lino-framework.org/admin/index.html


.. _getlino.install.demo:

Configure a Lino demo server
============================

(todo)

Contributing to getlino development
===================================

If you have a contributor environment, you may install your own local clone of
getlino::

   $ cd path/to/your/repos-base
   $ git clone git@github.com:lino-framework/getlino.git
   $ pip install -e getlino

Don't forget to manually add getlino to your atelier config.
