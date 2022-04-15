# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'lebai-ros-sdk-doc'
copyright = '2022, liufang'
author = 'liufang'

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_copybutton',
    'sphinx.ext.githubpages',
    'sphinx_tabs.tabs',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'
project = 'lebai-ros-sdk'
copyright = '2022, liufang@Lebai.ltd'
author = 'liufang'
version = '0.1'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = True

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    html_logo = 'logo.png'
    html_title = 'lebai-ros-sdk'
    html_favicon = 'logo.png'

html_theme_options = {
    'collapse_navigation': False,
    'prev_next_buttons_location': 'both'
}

html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}

# html_extra_path = ['_extra']
htmlhelp_basename = 'lebai-ros-sdk-doc'
html_show_sourcelink = False

# latex_elements = {    
#     'preamble': '\\usepackage[UTF8]{ctex}\n'
# }
# latex_documents = [
#     (master_doc, 'lebai-ros-sdk.tex', 'Lebai Ros SDK Documentation',
#      'liufang', 'manual'),
# ]
# latex_engine = 'xelatex'
# latex_use_xindy = False

man_pages = [
    (master_doc, 'lebai-ros-sdk', 'Lebai Ros SDK Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'lebai-ros-sdk', 'Lebai ROS SDK Documentation',
     author, 'lebai-ros-sdk', 'One line description of project.',
     'Miscellaneous'),
]
intersphinx_mapping = {'https://docs.python.org/3/': None}
primary_domain = 'cpp'
highlight_language = 'cpp'