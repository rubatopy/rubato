# pylint: disable=missing-module-docstring
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

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "rubato"
copyright = "2022, Martin Chaperot, Tomer Sedan, Yamm Elnekave"  # pylint: disable=redefined-builtin
author = "Martin Chaperot, Tomer Sedan, Yamm Elnekave"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinxext.opengraph",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",  # This need to be after napoleon
    "sphinx.ext.todo",
    "sphinx_sitemap",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

html_sidebars = {
    "**":
        [
            "sidebar/scroll-start.html",
            "brand.html",
            "sidebar/search.html",
            "sidebar/navigation.html",
            "versioning.html",
            "sidebar/scroll-end.html",
        ],
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

add_module_names = False

# Auto Class Config
autodoc_class_signature = "mixed"
autodoc_member_order = "bysource"
autodoc_mock_imports = ["sdl2"]
autodoc_typehints_format = "short"
autodoc_typehints = "signature"
autodoc_preserve_defaults = True

autodoc_default_options = {
    "show-inheritance": True,
}

rst_epilog = """
.. |default| replace:: :ref:`default config <defaults>`
"""

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = ["custom.css"]

add_module_names = False

html_favicon = "https://raw.githubusercontent.com/rubatopy/rubato/main/docs/source/_static/logo_filled.png"

theme_color = "#ff9484"

html_theme_options = {
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
    "light_css_variables":
        {
            "color-brand-primary": theme_color,
            "color-brand-content": theme_color,
            "color-api-name": theme_color,
            "font-stack": "Fredoka, sans-serif"
        },
    "dark_css_variables":
        {
            "color-brand-primary": theme_color,
            "color-brand-content": theme_color,
            "color-api-name": theme_color,
        },
    "globaltoc_maxdepth": -1,
    "globaltoc_includehidden": True,
}

html_use_index = False

html_title = f"{project} docs"

html_short_title = f"{project} docs"

html_show_sphinx = False
html_show_sourcelink = False

html_baseurl = "https://rubato.app"

# Open Graph
ogp_site_url = "https://rubato.app"
ogp_description_length = 300
ogp_image = "https://raw.githubusercontent.com/rubatopy/rubato/main/docs/source/_static/full.png"
ogp_site_name = "rubato docs"
ogp_custom_meta_tags = [
    '<meta property="og:title" content="rubato docs">',
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True
