"""
@brief      test log(time=2s)
"""
import os
import unittest
from pyquickhelper.pycode import ExtTestCase, skipif_appveyor, skipif_travis
from pyrsslocal.rss.rss_stream import StreamRSS


class TestRSSBug(ExtTestCase):

    @skipif_appveyor("issue")
    @skipif_travis("issue")
    def test_rss_parse(self):
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "xdbrss.xml")
        self.assertExists(file)

        rss = StreamRSS(titleb="yy", type="rss",
                        xmlUrl="https://freakonometrics.hypotheses.org/feed",
                        htmlUrl="https://freakonometrics.hypotheses.org/",
                        keywordsb=["python"], id=5)

        res = rss.enumerate_post()
        nb = 0
        for _ in res:
            nb += 1
            self.assertNotEmpty(_.title)
        self.assertGreater(nb, 1)


if __name__ == "__main__":
    unittest.main()
