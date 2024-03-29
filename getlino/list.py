# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import shutil
import secrets
import click

from os.path import join
from importlib import import_module

import rstgen

from .utils import KNOWN_REPOS, JINJA_ENV

KNOWN_APPS = [r for r in KNOWN_REPOS if r.settings_module and r.package_name]


@click.command()
@click.option('--rst/--no-rst', default=False, help="Output as reStructuredText")
@click.pass_context
def list(ctx, rst):
    """
    List the Lino applications known by getlino.

    """

    if rst:
        click.echo(".. Generated by `getlino list --rst`")
        click.echo(".. _getlino.apps:\n")
        click.echo(rstgen.header(1, "List of the known Lino applications"))
        click.echo("\nThe following applications are supported by :cmd:`getlino startsite`.\n")
    rows = []
    headings = ["Name", "Short description", "Nickname"]
    for r in KNOWN_APPS:
        m = import_module(r.settings_module)
        s = m.Site
        # r: nickname package_name git_repo settings_module front_end
        # print(r.settings_module)
        if rst:
            cells = [
                ":ref:`{s.verbose_name}<{r.nickname}>`".format(**locals()),
                s.description or '',
                r.nickname]
            rows.append(cells)
        else:
            click.echo("{r.nickname} : {s.verbose_name} : {s.description}".format(**locals()))
            # if s.description:
            #     click.echo("\n" + s.description.strip() + "\n")
            # if r.git_repo:
            #     print("(`Source repository <{r.git_repo}>`__)".format(**locals()))
    if rst:
        click.echo(rstgen.table(headings, rows))
        tpl = JINJA_ENV.get_template("apps_section.rst")
        for r in KNOWN_APPS:
            m = import_module(r.settings_module)
            s = m.Site
            p = import_module(r.package_name.replace("-", "_"))
            public_url = None
            if hasattr(p, 'intersphinx_urls'):
                public_url = p.intersphinx_urls.get('docs', None)
            context = dict(repo=r, package=p, m=m, site=s, rstgen=rstgen,
                public_url=public_url)
            click.echo(tpl.render(**context))
