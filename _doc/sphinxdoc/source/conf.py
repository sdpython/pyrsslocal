# -*- coding: utf-8 -*-
import sys
import os
import hachibee_sphinx_theme
from pyquickhelper.helpgen.default_conf import set_sphinx_variables

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "pyrsslocal", "Xavier Dupré", 2018,
                     "hachibee", hachibee_sphinx_theme.get_html_themes_path(),
                     locals(), add_extensions=['hachibee_sphinx_theme'], custom_style='custom_style.css',
                     extlinks=dict(issue=('https://github.com/sdpython/pyrsslocal/issues/%s', 'issue')))

# do not put it back otherwise sphinx import matplotlib before setting up its backend
# for the sphinx command .. plot::
# import pyensae
blog_root = "http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/"

epkg_dictionary['XML'] = 'https://en.wikipedia.org/wiki/XML'
