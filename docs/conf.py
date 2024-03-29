# -*- coding: utf-8 -*-
import sys,os

sys.path.insert(0, os.path.abspath(".."))
import getlino

extensions = []
intersphinx_mapping = {}

from atelier.sphinxconf import configure
configure(globals())

extensions += ['sphinx.ext.autosummary']
extensions += ['sphinx.ext.intersphinx']

# intersphinx_mapping = {}
from atelier.sphinxconf import interproject
interproject.configure(globals(), 'atelier')
intersphinx_mapping['cg'] = ('https://community.lino-framework.org/', None)
intersphinx_mapping['book'] = ('https://www.lino-framework.org/', None)

# General information about the project.
project = "getlino"
copyright = '2019-2021 Rumma & Ko Ltd'
from getlino import SETUP_INFO
release = SETUP_INFO['version']
version = '.'.join(release.split('.')[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = [
  'include',
  ]

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
# html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = SETUP_INFO['name'] # u"DjangoSite"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#~ html_logo = 'logo.jpg'
#~ html_logo = 'lino-logo-2.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#~ html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['.static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'
#~ last_updated = True

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#~ html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
   '**': ['globaltoc.html', 'searchbox.html', 'links.html'],
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#~ html_additional_pages = {
    #~ '*': 'links.html',
#~ }


# If false, no module index is generated.
html_use_modindex = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''
html_use_opensearch = 'http://getlino.lino-framework.org'

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'getlino'

extlinks.update(
  srcref=(getlino.srcref_url, ''),
  djangoticket=('http://code.djangoproject.com/ticket/%s', 'Django ticket #'),
)

autosummary_generate = True

todo_include_todos = True

gettext_compact = True

# extlinks.update(ticket=('https://jane.mylino.net/#/api/tickets/AllTickets/%s', '#'))

suppress_warnings = ['image.nonlocal_uri']
