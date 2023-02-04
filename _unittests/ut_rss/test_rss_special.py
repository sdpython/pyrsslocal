"""
@brief      test log(time=5s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyensae.sql.database_main import Database
from pyrsslocal.rss.rss_stream import StreamRSS


class TestRSSSpecial (unittest.TestCase):

    def test_rss_from_google_arxiv(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "subscriptions_arxiv.xml")
        assert os.path.exists(file)
        res = list(StreamRSS.enumerate_stream_from_google_list(file))
        if len(res) != 1:
            for r in res:
                print(r)
            raise AssertionError("number of expected feed %d != 1" % (len(res)))
        fLOG("nb:", len(res))

        dbfile = os.path.join(path, "temp_rss_arxiv.db3")
        if os.path.exists(dbfile):
            os.remove(dbfile)

        db = Database(dbfile, LOG=fLOG)
        db.connect()
        StreamRSS.fill_table(db, "blogs", res)
        db.close()


if __name__ == "__main__":
    unittest.main()
