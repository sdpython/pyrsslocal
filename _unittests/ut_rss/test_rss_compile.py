# coding: utf-8
"""
@brief      test log(time=2s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from pyrsslocal.cli import compile_rss_blogs


class TestRSSCompile(ExtTestCase):

    def test_rss_compile(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        temp = get_temp_folder(__file__, "temp_rss_compile")
        out_html = os.path.join(temp, 'index.html')
        out_rss = os.path.join(temp, 'rssfile.xml')

        links = ['http://www.xavierdupre.fr/blog/xdbrss.xml',
                 'http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/_downloads/rss.xml']
        compile_rss_blogs(links, "http://www.xavierdupre.fr/blogagg.html",
                          'Aggregation of blog posts published on <a href='
                          '"http://www.xavierdupre.fr.">xavierdupre.fr</a>',
                          title="Recent posts",
                          author="Xavier Dupré",
                          out_html=out_html, out_rss=out_rss,
                          fLOG=fLOG)
        self.assertExists(out_html)
        self.assertExists(out_rss)


if __name__ == "__main__":
    unittest.main()
