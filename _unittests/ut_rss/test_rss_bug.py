"""
@brief      test log(time=2s)
"""


import sys
import os
import unittest


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
from src.pyrsslocal.rss.rss_stream import StreamRSS


class TestRSSBug (unittest.TestCase):

    def test_rss_parse(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "xdbrss.xml")
        assert os.path.exists(file)

        rss = StreamRSS(titleb="yy",
                        type="rss",
                        xmlUrl="http://blog.yhathq.com/rss.xml",
                        htmlUrl="http://blog.yhathq.com/",
                        keywordsb=["python"],
                        id=5)

        res = rss.enumerate_post(fLOG=fLOG)
        nb = 0
        for _ in res:
            nb += 1
            assert len(_.title) > 0
        assert nb > 0


if __name__ == "__main__":
    unittest.main()
