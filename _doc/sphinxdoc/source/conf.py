#-*- coding: utf-8 -*-
import sys
import os
import datetime
import re
import hachibee_sphinx_theme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "..",
            "..",
            "..",
            "pyquickhelper",
            "src")))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "..",
            "..",
            "..",
            "pyensae",
            "src")))

from pyquickhelper.helpgen.default_conf import set_sphinx_variables

set_sphinx_variables(__file__, "pyrsslocal", "Xavier Dupré", 2017,
                     "hachibee", hachibee_sphinx_theme.get_html_themes_path(),
                     locals(), add_extensions=['hachibee_sphinx_theme'], custom_style='custom_style.css',
                     extlinks=dict(issue=('https://github.com/sdpython/pyrsslocal/issues/%s', 'issue')))

# do not put it back otherwise sphinx import matplotlib before setting up its backend
# for the sphinx command .. plot::
# import pyensae
blog_root = "http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/"
