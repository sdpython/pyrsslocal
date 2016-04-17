#-*- coding: utf-8 -*-
"""
@brief      test log(time=20s)
"""

import sys
import os
import unittest


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

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_

try:
    import pyensae as skip__
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyensae",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyensae as skip__

try:
    import pymyinstall as skip___
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pymyinstall",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pymyinstall as skip___


from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from src.pyrsslocal.xmlhelper import xml_filter_iterator


class TestXmlIterator(unittest.TestCase):

    def test_enumerate_xml_row(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, "temp_enumerate_wolf_xml_row")
        data = os.path.join(temp, "..", "data", "sample.wolf.xml")
        rows = xml_filter_iterator(data, fLOG=fLOG, xmlformat=False, log=True)
        n = 0
        node = None
        for i, row in enumerate(rows):
            if node is None:
                node = row
            #fLOG(type(row), row)
            s = str(row)
            assert s
            for obj in row.iterfields():
                s = str(obj)
                assert s
            if i % 2 == 0:
                row._convert_into_list()
            xout = row.get_xml_output()
            assert xout
            row.find_node_value("SYNET")
            n += 1
        assert n > 0

        # node += node


if __name__ == "__main__":
    unittest.main()
