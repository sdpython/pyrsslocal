# coding: latin-1
"""
@brief      test log(time=4s)

"""


import sys, os, unittest
from http.server import HTTPServer

try :
    import src
    import pyquickhelper
    import pyensae
except ImportError :
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
from src.pyrsslocal.rss.rss_database    import DatabaseRSS
from src.pyrsslocal.simple_server.simple_server_custom import SimpleHandler, run_server
from src.pyrsslocal.helper.download_helper import get_url_content


class TestSimpleServer (unittest.TestCase):
    
    def test_server_start_run (self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        
        server = HTTPServer(('localhost', 8094), SimpleHandler)
        thread = run_server(server, True)
        
        url = "http://localhost:8094/localfile/__file__"
        cont = get_url_content(url)
        assert len(cont)> 0
        assert "class SimpleHandler(BaseHTTPRequestHandler):" in cont
        
        url = "http://localhost:8094/localfile/test_simpleserver.py?execute=False&path=%s" % path
        fLOG(url)
        cont = get_url_content(url)
        assert "class TestSimpleServer (unittest.TestCase):" in cont
        
        cloud = os.path.join(path, "data")
        url = "http://localhost:8094/localfile/tag-cloud.html?path=%s" % cloud
        fLOG(url)
        cont = get_url_content(url)
        assert 'd3.json("data.json"' in cont
        
        url = "http://localhost:8094/localfile/tag-cloud.html?path=%s&keep=True" % cloud
        fLOG(url)
        cont = get_url_content(url)
        assert 'd3.json("data.json"' in cont
        assert len(SimpleHandler.queue_pathes) > 0
        
        thread.shutdown()    
        assert not thread.is_alive()
        
        
if __name__ == "__main__"  :
    
    if False :
        from srcpyhome.internet.rss.rss_helper import rss_run_server
        path = os.path.abspath(os.path.split(__file__)[0])
        dbfile = os.path.join( path, "data", "database_rss.db3")
        
        
        sql = """SELECT id_rss, SUM(nb)*1.0/ (MAX(day) - MIN(day)+1) AS avg_nb FROM (
                    SELECT id_rss, day, COUNT(*) AS nb FROM (
                        SELECT id_rss, getdayn(pubDate) AS day FROM posts
                    ) GROUP BY id_rss, day
                ) GROUP BY id_rss
                """
        db = DatabaseRSS(dbfile)
        db.connect()
        db.add_function ("getdayn", 1, DatabaseRSS.getdayn)        
        for row in db.execute(sql) :
            print ("ut",row)
            break
        db.close()

        
        rss_run_server (dbfile, port = 8093)
    
    unittest.main ()    

    