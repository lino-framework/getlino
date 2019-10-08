.. _getlino.install:

===============
Installing Lino
===============

This page explains how to install Lino on your computer.

The instructions sometimes depend on what you want to do, so let's  begin with
some vocabulary.

.. glossary::

  Developer environment

    You want Lino on your computer for developing your own :term:`Lino
    application`.

  Contributor environment

    An extended :term:`developer environment` to use if you plan to potentially
    contribute to the :term:`Lino framework`.  A bit more work to install, but
    more future-proof.

  Production server

    A dedicated server designed to host one or several :term:`production sites
    <production site>`.

  Demo server

    A dedicated server designed to host a series of demo sites.


Setting up your default environment
===================================

The **default environment** is the virtualenv that contains the :cmd:`getlino`
command.

- In a :term:`developer environment` or :term:`contributor environment` we suggest
  :file:`~/lino/env` as your *default environment*.

- On a :term:`production server` we suggest :file:`/usr/local/lino/shared/env`.

- On a :term:`demo server` we suggest :file:`/usr/local/lino/shared/master` or
  :file:`/usr/local/lino/shared/stable`.

Create a new virtual environment and activate it::

  $ sudo apt-get install python3-pip
  $ mkdir ~/lino
  $ cd ~/lino
  $ virtualenv -p python3 env
  $ . env/bin/activate

You probably want to make sure that your virtual environment is automatically
activated when you open a terminal, e.g. by adding the following line to your
:file:`~/.bashrc` file::

  . ~/lino/env/bin/activate

Install getlino::

  $ pip install getlino

Optionally use the development version::

  $ pip uninstall getlino
  $ pip install -e git+https://github.com/lino-framework/getlino.git#egg=getlino

.. _getlino.install.dev:

Configure a Lino developer environment
======================================

.. program:: getlino configure

Run :cmd:`getlino configure`::

  $ getlino configure

It asks a lot of questions, but you can hit ENTER for each of them. If it asks a
[y or n] question, should read it and understand it before you hit :kbd:`y`. For
details about each question see the documentation about :cmd:`getlino
configure`.

Run :cmd:`getlino startsite` to create a first site (and for every new site)::

  $ getlino startsite noi first

Run :manage:`runserver`::

  $ cd first
  $ python manage.py runserver

Point your browser to http://localhost:8000

Continue here: http://www.lino-framework.org/dev/index.html

.. _getlino.install.contrib:

Configure a Lino contributor environment
========================================

As a contributor you will want a local clone of the Lino code repositories
because you are going to do local modifications  and submit pull requests.

Run :cmd:`getlino configure` with :option:`--clone` and :option:`--devtools`::

  $ getlino configure --clone --devtools

Try one of the demo projects::

  $ cd ~/lino/env/repositories/book/lino_book/projects/team
  $ python manage.py prep
  $ python manage.py runserver

Point your browser to http://localhost:8000

Continue here:  http://www.lino-framework.org/team/index.html

.. _getlino.install.prod:
.. _getlino.install.admin:

Configure a Lino production server
==================================

Install getlino into a shared virtual environment outside of your home::

    $ sudo mkdir /usr/local/lino/shared/env
    $ cd /usr/local/lino/shared/env
    $ sudo chown root:www-data .
    $ sudo chmod g+ws .
    $ virtualenv -p python3 master
    $ . master/bin/activate
    $ pip install getlino

Run :cmd:`getlino configure` as root::

   $ sudo env PATH=$PATH getlino configure

The ``env PATH=$PATH`` is needed to work around the controversial Debian feature
of overriding the :envvar:`PATH` for security reasons (`source
<https://stackoverflow.com/questions/257616/why-does-sudo-change-the-path>`__).

Install a first site.  You will do the following for every new site on your
server.

   $ sudo env PATH=$PATH getlino startsite noi first

Point your browser to http://first.localhost

If your customers want to access their Lino from outside of their intranet, then
you need to setup a domain name and add use the :option:`getlino configure
--https` option in above command line.

Continue here:  http://www.lino-framework.org/admin/index.html


.. _getlino.install.demo:

Configure a Lino demo server
============================

Warning : This is the deeper Python jungle. Don't try this before you have
installed a few contributor environments and production servers.

Run :cmd:`getlino configure` as root::

   $ sudo -H env PATH=$PATH getlino configure --shared-env /usr/local/lino/shared/master --clone

.. program:: getlino configure

That is, you say :option:`--clone` and create a :option:`--shared-env`.

You may create other shared envs by changing the branch and clone another set of
repositories::

   $ sudo -H env PATH=$PATH getlino configure --shared-env /usr/local/lino/shared/stable --clone --branch stable

.. program:: getlino startsite

Specify :option:`--shared-env` when creating demo sites::

   $ sudo -H env PATH=$PATH getlino startsite noi first --shared-env /usr/local/lino/shared/stable
   $ sudo -H env PATH=$PATH getlino startsite tera second --shared-env /usr/local/lino/shared/master



Updating getlino
================

Depending on how you installed getlino, run either  :cmd:`pip install -U
getlino` after activating your default virtualenv.

Or, on a :term:`demo server` you run :cmd:`sudo -H pip3 install -U getlino` in
your system-wide virtualenv.


Contributing to getlino development
===================================

If you have a contributor environment, you may install your own local clone of
getlino::

   $ cd path/to/your/repos-base
   $ git clone git@github.com:lino-framework/getlino.git
   $ pip install -e getlino

Don't forget to manually add getlino to your atelier config.


Granting access to a Linux machine
==================================

On a :term:`production server`  you need shell access to a **Linux machine**,
i.e. a virtual or physical machine with a Linux operating system running in a
network. Here are instructions for the :term:`server provider` who wants to keep
root access for themselves and create new :term:`site maintainer` accounts as
needed.

We recommend a **stable Debian** as operating system.

Ceate a user for each :term:`site maintainer` and install sudo::

  # apt-get install sudo
  # adduser joe
  # adduser joe sudo
  # adduser joe www-data

And of course grant access to that new account, e.g. by creating the user's
:file:`.ssh/authorized_keys` file with the maintainer's public ssh key.

Now the :term:`site maintainer` can continue alone.
