"""
@brief      test log(time=2s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyensae.sql.database_main import Database
from pyrsslocal.rss.rss_stream import StreamRSS, BlogPost
from pyrsslocal.rss.rss_helper import rss_from_xml_to_database, rss_download_post_to_database
from pyrsslocal.rss.rss_database import DatabaseRSS


class TestRSS (unittest.TestCase):

    nb_rss_blog = 64

    def test_rss_from_google(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "subscriptions.xml")
        assert os.path.exists(file)
        res = list(StreamRSS.enumerate_stream_from_google_list(file))
        if len(res) != TestRSS.nb_rss_blog:
            dic = {}
            for i, r in enumerate(sorted(res)):
                dic[str(r)] = dic.get(str(r), 0) + 1
                fLOG(i, r)
            for k in dic:
                if dic[k] > 1:
                    fLOG("--double", k)
            raise Exception(
                "number of expected feed %d != %d" %
                (len(res), TestRSS.nb_rss_blog))
        li = sorted(res)
        for i, r in enumerate(li):
            if i > 0 and li[i] < li[i - 1]:
                raise Exception("bad order {0} < {1}".format(li[i - 1], li[i]))
        fLOG("nb:", len(res))

        dbfile = os.path.join(path, "temp_rss.db3")
        if os.path.exists(dbfile):
            os.remove(dbfile)

        db = Database(dbfile, LOG=fLOG)
        db.connect()
        StreamRSS.fill_table(db, "blogs", res)
        db.close()

        db = Database(dbfile, LOG=fLOG)
        db.connect()
        assert db.has_table("blogs")
        assert db.get_table_nb_lines("blogs") == TestRSS.nb_rss_blog
        sql = "SELECT * FROM blogs"
        cur = db.execute(sql)
        val = {}
        for row in cur:
            val[row[-1]] = 0
        assert len(val) == TestRSS.nb_rss_blog
        key = val.popitem()[0]
        assert key is not None

        # iterator on StreamRSS
        obj = list(db.enumerate_objects("blogs", StreamRSS))
        assert len(obj) == TestRSS.nb_rss_blog

        db.close()

    def test_rss_from_google_shortcut(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "subscriptions_small.xml")
        dbfile = os.path.join(path, "temp_rss22.db3")
        if os.path.exists(dbfile):
            os.remove(dbfile)
        nb = rss_from_xml_to_database(file, dbfile, fLOG=fLOG)
        assert nb == 1
        nb = rss_download_post_to_database(dbfile, fLOG=fLOG)
        if nb == 0:
            raise Exception(
                "issue with database '{0}', function rss_download_post_to_database".format(dbfile))
        fLOG("***")
        db = DatabaseRSS(dbfile, LOG=fLOG)
        blogs = list(db.enumerate_blogs())
        assert len(blogs) > 0

    def test_rss_parse(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        file = os.path.join(path, "data", "xdbrss.xml")
        assert os.path.exists(file)

        rss = StreamRSS(titleb="XD", type="rss",
                        xmlUrl="http://www.xavierdupre.fr/blog/xdbrss.xml",
                        htmlUrl="http://www.xavierdupre.fr/blog/xd_blog_nojs.html",
                        keywordsb=["python"], id=5)

        res = rss.enumerate_post(fLOG=fLOG)
        nb = 0
        for _ in res:
            nb += 1
            assert len(_.title) > 0
        self.assertTrue(nb > 0)

        res = rss.enumerate_post(file, fLOG=fLOG)
        nb = 0
        lres = list(res)

        nb = 0
        for _ in lres:
            nb += 1
            self.assertTrue(len(_.title) > 0)
        self.assertTrue(nb > 0)
        fLOG("nb post=", nb)

        dbfile = os.path.join(path, "temp_rssp.db3")
        if os.path.exists(dbfile):
            os.remove(dbfile)

        db = Database(dbfile, LOG=fLOG)
        db.connect()
        BlogPost.fill_table(db, "posts", lres)
        db.close()

        db = Database(dbfile, LOG=fLOG)
        db.connect()
        self.assertTrue(db.has_table("posts"))
        self.assertEqual(db.get_table_nb_lines("posts"), nb)

        sql = "SELECT * FROM posts"
        cur = db.execute(sql)
        val = {}
        for row in cur:
            val[row[-1]] = 0
        self.assertEqual(len(val), 6)
        key, _ = val.popitem()
        self.assertTrue(key is not None)

        # we insert the blog a second time
        BlogPost.fill_table(db, "posts", lres)
        sql = "SELECT * FROM posts"
        cur = db.execute(sql)
        val = {}
        for row in cur:
            val[row[-1]] = 0
        self.assertEqual(len(val), 6)

        # we insert the blog a third time
        BlogPost.fill_table(db, "posts", lres)
        sql = "SELECT * FROM posts"
        cur = db.execute(sql)
        val = {}
        for row in cur:
            val[row[-1]] = 0
        self.assertEqual(len(val), 6)

        db.close()


if __name__ == "__main__":
    unittest.main()
