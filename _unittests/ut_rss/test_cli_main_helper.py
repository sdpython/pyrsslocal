"""
@brief      test tree node (time=7s)
"""
import unittest
from pyquickhelper.loghelper import BufferedPrint
from pyquickhelper.pycode import ExtTestCase
from pyrsslocal.__main__ import main


class TestCliMainHelper(ExtTestCase):

    def test_main(self):
        st = BufferedPrint()
        main(args=[], fLOG=st.fprint)
        res = str(st)
        self.assertIn("python -m pyrsslocal <command>", res)
        self.assertIn("compile_rss_blogs", res)

    def test_compile_rss_blogs(self):
        st = BufferedPrint()
        main(args=["compile_rss_blogs", '--help'], fLOG=st.fprint)
        res = str(st)
        self.assertIn("usage: compile_rss_blogs", res)


if __name__ == "__main__":
    unittest.main()
