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
import sys

#sys.path.insert(0, os.path.abspath('../..'))
#print(os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../tiledb'))
print(os.path.abspath('../../tiledb'))

# -- ReadTheDocs configuration ---------------------------------------------

# Special handling on ReadTheDocs builds.
# Some of this code is from https://github.com/robotpy/robotpy-docs/blob/master/conf.py
readthedocs = os.environ.get('READTHEDOCS', None) == 'True'
rtd_version = os.environ.get('READTHEDOCS_VERSION', 'latest')
rtd_version = rtd_version if rtd_version in ['stable', 'latest'] else 'stable'

# -- Project information -----------------------------------------------------

project = 'TileDB-Cloud-Py'
copyright = '2020, TileDB, Inc.'
author = 'TileDB, Inc.'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # 'sphinx.ext.autodoc',
    #'sphinxcontrib.apidoc',
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    'sphinx.ext.autosummary',  # Create neat summary tables
]
autosummary_generate = True

source_suffix = ['.rst', '.md']

#apidoc_module_dir = '../..'
#apidoc_excluded_paths = ['tests', 'tiledb/cloud/rest_api', 'setup.py', '**/test/**']
#apidoc_separate_modules = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_autosummary/tiledb.test*", "_autosummary/tiledb.cloud.rest_api.test*", "_autosummary/tiledb.version.rst", "_autosummary/tiledb.array*", "_autosummary/tiledb.core*", "_autosummary/tiledb.dataframe*", "_autosummary/tiledb.highlevel", "_autosummary/tiledb.libtiledb*", "_autosummary/tiledb.metadata*", "_autosummary/tiledb.multirange*", "_autosummary/tiledb.version.rst"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
if readthedocs:
    html_theme = 'default'
else:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_sidebars = { '**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'] }
