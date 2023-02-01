# -*- coding: utf-8 -*-
import sys
import os
import alabaster
from pyquickhelper.helpgen.default_conf import set_sphinx_variables

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "pyrsslocal", "Xavier Dupré", 2023,
                     "alabaster", alabaster.get_path(), locals(), add_extensions=['alabaster'],
                     extlinks=dict(issue=(
                         'https://github.com/sdpython/pyrsslocal/issues/%s',
                         'issue %s')))

# do not put it back otherwise sphinx import matplotlib before setting up its backend
# for the sphinx command .. plot::
# import pyensae
blog_root = "http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/"

epkg_dictionary.update({
    'HTML': 'https://en.wikipedia.org/wiki/HTML',
    'RSS': 'https://en.wikipedia.org/wiki/RSS',
    'rss': 'https://en.wikipedia.org/wiki/RSS',
    'XML': 'https://en.wikipedia.org/wiki/XML',
})
