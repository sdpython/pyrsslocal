# -*- coding: utf-8 -*-
"""
@brief      test log(time=20s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src


from src.pyrsslocal.xmlhelper import HTMLtoJSONParser, iterate_on_json


class TestJsonIterator(unittest.TestCase):

    def test_html2json(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, "temp_enumerate_wolf_xml_row")
        data = os.path.join(temp, "..", "data", "ensae.bing.html")
        with open(data, "r", encoding="utf8") as f:
            content = f.read()
        js = HTMLtoJSONParser.to_json(content)
        self.assertTrue(js is not None)
        self.assertGreater(len(js), 0)

        key = {("/html/body/div/ol/li/h2/a/strong/strong/", "Ensae"): 0}
        for k, v in iterate_on_json(js):
            k2 = k, v
            if k2 in key:
                key[k2] += 1
        s = sum(key.values())
        self.assertGreater(s, 0)


if __name__ == "__main__":
    unittest.main()
