"""
@brief      test log(time=0s)
"""

import sys
import os
import unittest
import warnings
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8
from pyquickhelper.pycode.utils_tests_helper import _extended_refactoring


class TestCodeStyle(unittest.TestCase):

    def test_code_style_src(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2:
            warnings.warn(
                "skipping test_code_style because of Python 2 or " + sys.executable)
            return

        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG, extended=[("fLOG", _extended_refactoring)],
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'W0231', 'W0212', 'C0111', 'W0122', 'W0223',
                                  'R1703', 'C0412', 'W0105', 'W0703', 'W0201',
                                  'W0107', 'C0415'),
                   skip=["Unable to import 'pyrsslocal'",
                         ],
                   )

    def test_code_style_test(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2:
            warnings.warn(
                "skipping test_code_style because of Python 2 or " + sys.executable)
            return

        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0111', 'C0103', 'W0622', 'C1801', 'C0412',
                                  'R0201', 'W0122', 'W0123', 'E1101', 'R1705',
                                  'E0401', 'W0621', 'W0212', 'C0411', 'W0107',
                                  'C0415'),
                   skip=[],
                   extended=[("fLOG", _extended_refactoring)])


if __name__ == "__main__":
    unittest.main()
