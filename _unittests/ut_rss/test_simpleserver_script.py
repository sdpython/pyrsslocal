# coding: latin-1
"""
@brief      test log(time=1s)

"""


import sys, os, unittest, time
from io import StringIO

try :
    import src
    import pyquickhelper
except ImportError :
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..")))
    if path not in sys.path : sys.path.append (path)
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..", "..", "pyquickhelper", "src")))
    if path not in sys.path : sys.path.append (path)
    import src
    import pyquickhelper

from pandas import DataFrame

from pyquickhelper                                      import fLOG
from src.pyrsslocal.simple_server.html_script_parser    import HTMLScriptParser
from src.pyrsslocal.simple_server.html_string           import html_debug_string
from src.pyrsslocal.helper.externs                      import df_to_html


class TestSimpleServerScript (unittest.TestCase):

    def test_html_string(self):
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        params = { "url":"http://..." }
        pars = [ { "key":k, "value":v } for k,v in params.items() ]
        tbl = DataFrame (pars)
        html = df_to_html(tbl, class_table="myclasstable")
        assert "<table class" in html
        assert params["url"] in html

    def test_python_processing(self):
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        st = StringIO()
        parser = HTMLScriptParser( outStream = st)
        parser.feed(html_debug_string)
        res = st.getvalue()
        assert len(res) > 0
        assert """<script type="text/python">""" in html_debug_string
        assert """<script type="text/python">""" not in res
        assert '<table class="myclasstable">' in res


if __name__ == "__main__"  :
    unittest.main ()