"""
@brief      test log(time=2s)
"""
import os
import unittest
from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from pyrsslocal.rss.rss_helper import enumerate_rss_merge, to_rss, to_html


class TestRSSMerge(ExtTestCase):

    def test_merge_rss(self):
        this = os.path.abspath(os.path.dirname(__file__))
        name = os.path.join(this, "data")
        rsss = [os.path.join(name, "rss.xml"), os.path.join(name, "rss2.xml")]
        blogs = list(enumerate_rss_merge(rsss))
        nb = len(blogs)
        self.assertEqual(nb, 16)
        text = to_rss(blogs, link="http://mymy", description="zoo")
        self.assertIn("<item>", text)
        self.assertIn("</item>", text)
        text = to_html(blogs)
        temp = get_temp_folder(__file__, "temp_merge_rss")
        dest = os.path.join(temp, "blog.html")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(text)
        self.assertIn('<h1>', text)
        self.assertIn('2019', text)


if __name__ == "__main__":
    unittest.main()
