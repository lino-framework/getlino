.. _getlino.install:

===============
Installing Lino
===============

This page gives an overview on how to install Lino on your computer.

From the following list, choose the one which matches your profile:

- I want to write my own Lino application.
  --> `Configure a minimal Lino site`_

- I want to write my own Lino application and maybe contribute to the project.
  --> `Configure a Lino contributor environment`_

- I want to set up a Lino server and host Lino production sites for myself or
  others. --> `Configure a Lino production server`_


Configure a minimal Lino site
=============================

Create a new virtual environment, activate it, install getlino, run
:cmd:`getlino configure` followed by :cmd:`getlino startsite`, then run
:manage:`runserver`::

  $ sudo apt-get install -y python3-pip
  $ mkdir ~/lino
  $ cd ~/lino
  $ virtualenv -p python3 env
  $ . env/bin/activate
  $ pip install getlino
  $ getlino configure --sites-base .
  $ getlino startsite noi first
  $ cd first
  $ python manage.py runserver

Point your browser to http://localhost:8000

Read the http://www.lino-framework.org/dev/index.html


Configure a Lino contributor environment
========================================

Activate the virtual environment you want to use for your Lino projects::

  $ . path/to/my/virtualenv/bin/activate


  $ pip install getlino
  $ getlino configure --contrib
  $ getlino startsite noi first --dev-repos "lino xl noi book"
  $ cd first
  $ python manage.py runserver

Point your browser to http://localhost:8000

Read the http://www.lino-framework.org/team/index.html


Configure a Lino production server
==================================

You need shell access to a **Linux machine**, i.e. a virtual or physical machine
with a Linux operating system running in a network. We recommend a **stable
Debian** as operating system.   We will install a series of system packages like
Python, nginx, monit, a database server (MySQL or PostGreSQL) on your machine.

Install getlino into the system-wide Python 3 environment::

   $ sudo -H pip3 install getlino

We run :cmd:`getlino configure` as root::

   $ sudo -H getlino configure

If your customers want to access their Lino from outside of their intranet, then
you need to setup a domain name and add use the :option:`getlino configure
--https` option in above command line.

Install a first site.  You will do the following for every new site on your
server.

   $ sudo -H getlino startsite noi first

Point your browser to http://first.localhost


Three variants of getlino
=========================

Either the officially stable version::

   $ pip install getlino

Or the development version::

   $ pip install -e git+https://github.com/lino-framework/getlino.git#egg=getlino

Or install your own local clone::

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
