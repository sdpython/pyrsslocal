# coding: utf-8
"""
@brief      test log(time=1s)
"""
import unittest
from io import StringIO
from pandas import DataFrame
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pandashelper.tblformat import df2html
from pyrsslocal.simple_server.html_script_parser import HTMLScriptParser
from pyrsslocal.simple_server.html_string import html_debug_string


class TestSimpleServerScript (unittest.TestCase):

    def test_html_string(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        params = {"url": "http://..."}
        pars = [{"key": k, "value": v} for k, v in params.items()]
        tbl = DataFrame(pars)
        html = df2html(tbl, class_table="myclasstable")
        assert "<table class" in html
        assert params["url"] in html

    def test_python_processing(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        st = StringIO()
        parser = HTMLScriptParser(outStream=st)
        parser.feed(html_debug_string)
        res = st.getvalue()
        assert len(res) > 0
        assert """<script type="text/python">""" in html_debug_string
        assert """<script type="text/python">""" not in res
        assert '<table class="myclasstable">' in res


if __name__ == "__main__":
    unittest.main()
