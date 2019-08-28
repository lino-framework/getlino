.. _getlino.install:

===============
Installing Lino
===============

This page gives an overview on how to install Lino on your computer.

There are several flavours of Lino, choose the one which matches your profile:

- `Configure a Lino developer environment`_ if you just want to write your own
  Lino application.

- `Configure a Lino contributor environment`_
  if you want to write you own Lino application and maybe contribute to the project.

- `Configure a Lino production server`_ if you want to set up a Lino server and
  host Lino production sites for yourself or others.

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

If you ran configure as root and also installed a production server, you may add
sites and test them under nginx::

  $ getlino startsite noi first --dev-repos "lino xl noi book"
  $ cd first

Point your browser to http://localhost:8000

Continue here:  http://www.lino-framework.org/team/index.html

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


Contributing to getlino development
===================================

If you have a contributor environment, you may install your own local clone of
getlino::

   $ cd path/to/your/repos-base
   $ git clone git@github.com:lino-framework/getlino.git
   $ pip install -e getlino

Dont forget to manually add getlino to your atelier config.
