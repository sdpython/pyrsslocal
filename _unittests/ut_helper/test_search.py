"""
@brief      test log(time=0s)
"""

import sys
import os
import unittest
import warnings


try:
    import src
    import pyquickhelper as skip_
    import pyensae as skip__
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
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
    import src
    import pyquickhelper as skip_
    import pyensae as skip__

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import is_travis_or_appveyor
from src.pyrsslocal.helper.search_engine import query_bing


class TestSearch(unittest.TestCase):

    def test_search(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        cont = query_bing("bing")
        assert isinstance(cont, list)
        assert len(cont) > 0
        if is_travis_or_appveyor():
            warnings.warn("unstable search result, skip on ci")
        else:
            if "bing" not in cont[0]:
                raise Exception(str(cont[0]))


if __name__ == "__main__":
    unittest.main()
