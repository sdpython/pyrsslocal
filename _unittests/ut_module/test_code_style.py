"""
@brief      test log(time=0s)
"""

import sys
import os
import unittest
import warnings


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
                "src",)))
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
                "src",)))
    if path not in sys.path:
        sys.path.append(path)
    import pyensae as skip__

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8
from pyquickhelper.pycode.utils_tests_helper import _extended_refactoring


class TestCodeStyle(unittest.TestCase):

    def test_code_style_src(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2 or "Anaconda" in sys.executable \
                or "condavir" in sys.executable:
            warnings.warn(
                "skipping test_code_style because of Python 2 or " + sys.executable)
            return

        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG, extended=[("fLOG", _extended_refactoring)],
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'W0231', 'W0212', 'C0111', 'W0122', 'W0223',
                                  'R1703', 'C0412', 'W0105', 'W0703', 'W0201'),
                   skip=["aserver.py:314",
                         "Unable to import 'pyrsslocal'",
                         "Redefining built-in 'filter'",
                         "Redefining built-in 'all'",
                         "Redefining built-in 'sorted'",
                         "edefining name 'fLOG' from outer scope",
                         "Redefining built-in 'type'",
                         "Redefining built-in 'id'",
                         "simple_server_custom.py",
                         'xmlfilewalk.py:183',
                         "xml_tree.py:176",
                         "rss_simple_server.py:236",
                         "html_script_parser.py:230",
                         "html_parser_json.py:8",
                         "html_parser_json.py:102",
                         "xml_tree.py:168",
                         "Instance of 'XMLHandlerDictNode' has no '",
                         "xml_tree.py:170",
                         ],
                   )

    def test_code_style_test(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2 or "Anaconda" in sys.executable \
                or "condavir" in sys.executable:
            warnings.warn(
                "skipping test_code_style because of Python 2 or " + sys.executable)
            return

        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0111', 'C0103', 'W0622', 'C1801', 'C0412',
                                  'R0201', 'W0122', 'W0123', 'E1101', 'R1705',
                                  'E0401', 'W0621', 'W0212', 'C0411'),
                   skip=["src' imported but unused",
                         "skip_' imported but unused",
                         "skip__' imported but unused",
                         "skip___' imported but unused",
                         "Unused variable 'skip_'",
                         "Unused import src",
                         "Unused variable 'skip_",
                         "imported as skip_",
                         "Redefining name 'path' from outer scope",
                         ],
                   extended=[("fLOG", _extended_refactoring)])


if __name__ == "__main__":
    unittest.main()
