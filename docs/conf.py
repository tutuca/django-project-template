# -*- coding: utf-8 -*-
#
# {{project_name}} documentation build configuration file, created by
# sphinx-quickstart on Sun May 10 19:53:54 2015.

import sys
import os
import alabaster

BASE_DIR = os.path.dirname(__file__)
PACKAGES = [
    'victims',
    'legacy'
]
[sys.path.insert(
    0, os.path.join(os.path.basename(BASE_DIR), p)) for p in PACKAGES
]


html_theme_path = [alabaster.get_path()]

html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html', 'navigation.html', 'searchbox.html', 'donate.html',
    ]
}

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'alabaster'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'{{project_name}}'
copyright = u'2015, {{project_name}}.'
version = '0.1'
release = '0.1'

exclude_patterns = ['_build']
pygments_style = 'sphinx'


html_static_path = ['_static']

htmlhelp_basename = '{{project_name}}-doc'

intersphinx_mapping = {'http://docs.python.org/': None}
