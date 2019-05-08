"""
@brief      test log(time=2s)
"""
import os
import unittest
from pyquickhelper.pycode import ExtTestCase
from pyrsslocal.rss.rss_helper import enumerate_rss_merge, to_rss


class TestRSSMerge(ExtTestCase):

    def test_merge_rss(self):
        this = os.path.dirname(__file__)
        name = os.path.join(this, "data")
        rsss = [os.path.join(name, "rss.xml"), os.path.join(name, "rss1.xml")]
        blogs = list(enumerate_rss_merge(rsss))
        nb = len(blogs)
        self.assertEqual(nb, 6)
        text = to_rss(blogs, link="http://mymy", description="zoo")
        self.assertIn("<item>", text)
        self.assertIn("</item>", text)


if __name__ == "__main__":
    unittest.main()
