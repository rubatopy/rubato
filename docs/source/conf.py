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
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'Rubato'
copyright = '2022, Martin Chaperot, Tomer Sedan, Yamm Elnekave'
author = 'Martin Chaperot, Tomer Sedan, Yamm Elnekave'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.githubpages', 'sphinx.ext.autosummary', 'sphinx.ext.viewcode', 'sphinx_copybutton', 'sphinx_inline_tabs', 'sphinxext.opengraph'
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
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_extra_path = ["../robots.txt"]

add_module_names = False

html_logo = "_static/logo_img_small.png"

html_favicon = "_static/logo_img.png"

html_theme_options = {
    'navigation_with_keys': True,
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#e61e43", # Default: 2962ff (41, 98, 255)
        "color-brand-content": "#e61e43", # Default: 2a5adf (42, 90, 223)
    },
    "dark_css_variables": {
        "color-brand-primary": "var(--color-problematic)", # Default: 2962ff (41, 98, 255)
        "color-brand-content": "var(--color-problematic)", # Default: 2a5adf (42, 90, 223)
    }
}

html_use_index = False

html_title = f"{project} {release} Documentation"

html_short_title = f"{project} Docs"

html_show_sphinx = False
html_show_sourcelink = False

ogp_description_length = 300
ogp_image = "_static/logo_long.png"
