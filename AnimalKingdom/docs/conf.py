# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # add root project folder to path

# -- Project information -----------------------------------------------------

project = 'Animal Kingdom'
author = 'Steve Shillitoe'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',    # Automatically include docstrings
    'sphinx.ext.napoleon',   # Support Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode',   # Add links to source code
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
