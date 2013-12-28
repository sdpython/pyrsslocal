# coding: latin-1
"""
@brief      test log(time=2s)

"""


import sys, os, unittest, re, datetime, time, copy, shutil
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

class TestRSSDatabase (unittest.TestCase):
    
    def test_rss_database_html (self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "database_rss.db3")
        assert os.path.exists (file)
        
        db = DatabaseRSS(file, LOG = fLOG)
        blogs = list( db.enumerate_blogs())
        fLOG("nb",len(blogs))
        assert len(blogs) == 71
        s = str(blogs[0])
        fLOG(s, blogs[0].id)
        assert len(s) > 0
        s = blogs[0].html()
        fLOG(s)
        assert len(s) > 0
        assert "href" in s
        
        posts = list( db.enumerate_posts ( blog_selection = [1,2,3] ))
        fLOG("nb",len(posts))
        assert len(posts) > 0
        ht = posts[0].html()
        assert len(ht)>0
        
        posts = list( db.enumerate_posts ( blog_selection = [] ))
        fLOG("nb",len(posts))
        assert len(posts) > 0
        ht = posts[0].html()
        assert len(ht)>0
        ht = posts[0].html(addcontent = True)
        assert len(ht)>0

    def test_rss_database2 (self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "database_rss.db3")
        assert os.path.exists (file)
        file2 = os.path.join(path, "temp_data_copy2.db3")
        shutil.copy (file, file2)
        file = file2
        
        db = DatabaseRSS(file, LOG = fLOG)
        
        db.connect()
        sel = db.execute_view ("SELECT * FROM posts_stat")
        db.close()
        assert len(sel) > 0
        
        keys = list(sorted(DatabaseRSS.specific_search.keys()))
        keys.reverse()
        fLOG(keys)
        now = datetime.datetime(2013,7,17)
        
        nb = { }
        for specific in keys :
            bl = list(db.enumerate_blogs(specific = specific, now = now))
            nb [specific] = len(bl)
            fLOG("**specific", specific, ":", len(bl))
        assert len(nb) > 0
        assert nb["today"] <= nb["week"]
        assert nb["frequent"] <= nb["notfrequent"]
        
    def test_rss_database_stat (self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "database_rss.db3")
        assert os.path.exists (file)
        file2 = os.path.join(path, "temp_data_copy_stat.db3")
        shutil.copy (file, file2)
        file = file2
        
        keys = list(sorted(DatabaseRSS.specific_search.keys()))
        keys.reverse()
        fLOG(keys)
        now = datetime.datetime(2013,7,17)        
        
        db = DatabaseRSS(file, LOG = fLOG)
                
        for specific in keys :
            bl = list(db.enumerate_blogs(specific = specific, now = now, addstat = True))
            if len(bl) > 0 :
                html = bl[0].html("default_stat")
                assert '<tr class="blogtitle">' in html
                fLOG("**specific", specific, ":", len(bl))
                #fLOG(html)
        
    def test_rss_database_status_latest(self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "database_rss.db3")
        assert os.path.exists (file)
        
        db = DatabaseRSS(file, LOG = fLOG)
        
        posts = list( db.enumerate_posts_status ( blog_selection = [1,2,3] ))
        fLOG("nb",len(posts))
        assert len(posts)>0
        nb = 0
        for p in posts:
            s = p.html("status")
            fLOG(s)
            if "interesting" in s : nb += 1
        assert nb>0
        
if __name__ == "__main__"  :
    unittest.main ()    
