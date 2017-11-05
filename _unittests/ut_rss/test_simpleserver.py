# coding: latin-1
"""
@brief      test log(time=4s)

"""


import sys
import os
import unittest
from http.server import HTTPServer

try:
    import src
    import pyquickhelper as skip_
    import pyensae as skip__
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyensae",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import src
    import pyquickhelper as skip_
    import pyensae as skip__

from pyquickhelper.loghelper import fLOG
from src.pyrsslocal.simple_server.simple_server_custom import SimpleHandler, run_server
from src.pyrsslocal.helper.download_helper import get_url_content_timeout


class TestSimpleServer (unittest.TestCase):

    def test_server_start_run(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])

        server = HTTPServer(('localhost', 8094), SimpleHandler)
        thread = run_server(server, True)

        url = "http://localhost:8094/localfile/__file__"
        cont = get_url_content_timeout(url)
        self.assertTrue(len(cont) > 0)
        if sys.platform.startswith("win"):
            self.assertIn("class SimpleHandler(BaseHTTPRequestHandler):", cont)

        url = "http://localhost:8094/localfile/test_simpleserver.py?execute=False&path=%s" % path
        fLOG(url)
        cont = get_url_content_timeout(url)
        if "class TestSimpleServer (unittest.TestCase):" not in cont:
            raise Exception(
                "expects to find 'class TestSimpleServer (unittest.TestCase):' in \n{0}".format(cont))

        cloud = os.path.join(path, "data")
        url = "http://localhost:8094/localfile/tag-cloud.html?path=%s" % cloud
        fLOG(url)
        cont = get_url_content_timeout(url)
        self.assertIn('d3.json("data.json"', cont)

        url = "http://localhost:8094/localfile/tag-cloud.html?path=%s&keep=True" % cloud
        fLOG(url)
        cont = get_url_content_timeout(url)
        self.assertIn('d3.json("data.json"', cont)
        self.assertTrue(len(SimpleHandler.queue_pathes) > 0)

        thread.shutdown()
        self.assertTrue(not thread.is_alive())


if __name__ == "__main__":
    unittest.main()
