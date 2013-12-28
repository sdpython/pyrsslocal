# coding: latin-1
"""
@brief      test log(time=6s)

"""


import sys, os, unittest, re, datetime, time
from http.server import BaseHTTPRequestHandler, HTTPServer

try :
    import src
    import pyquickhelper
    import pyensae
except ImportError :
    import os, sys
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..")))
    if path not in sys.path : sys.path.append (path)
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..", "..", "pyquickhelper", "src")))
    if path not in sys.path : sys.path.append (path)
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..", "..", "pyensae", "src")))
    if path not in sys.path : sys.path.append (path)
    import src
    import pyquickhelper
    import pyensae

from pyquickhelper                      import fLOG
from src.pyrsslocal.rss.rss_stream      import StreamRSS, BlogPost
from src.pyrsslocal.rss.rss_database    import DatabaseRSS
from src.pyrsslocal.simple_server.simple_server_custom import SimpleHandler, run_server
from src.pyrsslocal.helper.search_engine import get_url_content
from src.pyrsslocal.rss.rss_simple_server import RSSSimpleHandler, RSSServer



class TestSimpleServerRSS (unittest.TestCase):
    
    def test_server_start_run (self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        dbfile = os.path.join( path, "data", "database_rss.db3")
        
        server = RSSServer(('localhost', 8093), dbfile)
        thread = RSSServer.run_server(server, dbfile, thread = True)
        
        fLOG("fetching first url")
        url = "http://localhost:8093/"
        cont = get_url_content(url)
        if "Traceback" in cont : fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont)> 0
        assert "RSS" in cont
        assert "XD blog" in cont
        
        url = "http://localhost:8093/rss_status.html"
        cont = get_url_content(url)
        if "Traceback" in cont : fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont)> 0
        assert "RSS" in cont
        assert "interesting" in cont

        url = "http://localhost:8093/rss_search.html?searchterm=military&usetag=usetag"
        cont = get_url_content(url)
        if "Traceback" in cont :fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont)> 0
        assert "RSS" in cont
        assert "interesting" in cont
        assert "Military" in cont
        assert "Mozilla Continues" not in cont
        
        fLOG("fetching first url")
        url = "http://localhost:8093/rss_search.html?searchterm=military"
        cont = get_url_content(url)
        if "Traceback" in cont : fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont)> 0
        assert "RSS" in cont
        assert "interesting" not in cont
        assert "Military" in cont
        assert "Mozilla Continues" not in cont        

        thread.shutdown()
        assert not thread.is_alive()
        
if __name__ == "__main__"  :
    unittest.main ()  


