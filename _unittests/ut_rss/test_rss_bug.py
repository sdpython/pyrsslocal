"""
@brief      test log(time=2s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import ExtTestCase
from pyrsslocal.rss.rss_stream import StreamRSS


class TestRSSBug(ExtTestCase):

    def test_rss_parse(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "xdbrss.xml")
        self.assertExists(file)

        rss = StreamRSS(titleb="yy", type_="rss",
                        xmlUrl="https://freakonometrics.hypotheses.org/feed",
                        htmlUrl="https://freakonometrics.hypotheses.org/",
                        keywordsb=["python"], idrss=5)

        res = rss.enumerate_post(fLOG=fLOG)
        nb = 0
        for _ in res:
            nb += 1
            self.assertNotEmpty(_.title)
        self.assertGreater(nb, 1)


if __name__ == "__main__":
    unittest.main()
