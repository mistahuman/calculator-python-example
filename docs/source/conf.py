#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sphinx configuration file for Calculator Example documentation.

This file configures Sphinx to generate documentation for the calculator project.
It sets up autodoc, type hints, and theme settings.
"""

import os
import sys
from datetime import datetime

# Add project to path for autodoc
sys.path.insert(0, os.path.abspath('../../src'))

# Project information
project = 'Calculator Example'
copyright = f'{datetime.now().year}, Marco Lanconelli'
author = 'Marco Lanconelli'
release = '0.1.0'
version = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
    'myst_parser',
]

# Add support for markdown files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Master document
master_doc = 'index'

# Templates path
templates_path = ['_templates']

# Patterns to exclude
exclude_patterns = []

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings (for Google/NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
