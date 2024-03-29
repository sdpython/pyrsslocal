"""
@brief      test log(time=6s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyrsslocal.helper.download_helper import get_url_content_timeout
from pyrsslocal.rss.rss_simple_server import RSSServer


class TestSimpleServerRSS (unittest.TestCase):

    def test_server_start_run(self):
        """
        if this test fails, the unit test is stuck, you need to stop the program yourself
        """
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        dbfile = os.path.join(path, "data", "database_rss.db3")

        server = RSSServer(('localhost', 8093), dbfile, fLOG=fLOG)
        thread = RSSServer.run_server(server, dbfile, thread=True, fLOG=fLOG)

        fLOG("fetching first url")
        url = "http://localhost:8093/"
        cont = get_url_content_timeout(url)
        if "Traceback" in cont:
            fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont) > 0
        assert "RSS" in cont
        assert "XD blog" in cont

        url = "http://localhost:8093/rss_status.html"
        cont = get_url_content_timeout(url)
        if "Traceback" in cont:
            fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont) > 0
        assert "RSS" in cont
        if "interesting" not in cont:
            raise AssertionError(cont)

        url = "http://localhost:8093/rss_search.html?searchterm=pypi&usetag=usetag"
        cont = get_url_content_timeout(url)
        if "Traceback" in cont:
            fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont) > 0
        assert "RSS" in cont
        if "PyPI" not in cont:
            fLOG(cont)
            assert False
        # if "added" not in cont:
        #    fLOG(cont)
        #    assert False
        assert "Mozilla Continues" not in cont

        fLOG("fetching first url")
        url = "http://localhost:8093/rss_search.html?searchterm=military"
        cont = get_url_content_timeout(url)
        if "Traceback" in cont:
            fLOG(cont)
        assert "Traceback" not in cont
        assert len(cont) > 0
        assert "RSS" in cont
        assert "interesting" not in cont
        assert "Military" in cont
        assert "Mozilla Continues" not in cont

        thread.shutdown()
        assert not thread.is_alive()


if __name__ == "__main__":
    unittest.main()
