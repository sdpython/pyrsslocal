"""
generates the documentation using Sphinx
"""
import sys, os

try:
    import pyquickhelper, pyensae, pyrsslocal
except ImportError:
    sys.path.append ( os.path.normpath (os.path.join( os.path.abspath("."), "..", "pyquickhelper", "src")))
    sys.path.append ( os.path.normpath (os.path.join( os.path.abspath("."), "..", "pyensae", "src")))
    sys.path.append ( os.path.normpath (os.path.join( os.path.abspath("."), "src")))
    import pyquickhelper
    import pyensae
    import pyrsslocal

from pyquickhelper  import fLOG
from pyrsslocal     import rss_update_run_server

if __name__ == "__main__" :
    fLOG (OutputPrint = True)
    xml_blogs = "_unittests/ut_rss/data/subscriptions_small.xml"
    dbfile    = "rss_posts.db3"
    rss_update_run_server(dbfile, xml_blogs)