"""
@brief      test log(time=0s)
"""
import unittest
import warnings
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import is_travis_or_appveyor
from pyrsslocal.helper.search_engine import query_bing


class TestSearch(unittest.TestCase):

    def test_search(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        cont = query_bing("bing")
        if cont is None:
            warnings.warn("unstable search result, skip on ci, check locally")
            return
        if not isinstance(cont, list):
            raise TypeError(type(cont))
        self.assertTrue(len(cont) > 0)
        if is_travis_or_appveyor():
            warnings.warn("unstable search result, skip on ci")
        else:
            sel = [c for c in cont if "bing" in c]
            if len(sel) == 0:
                raise Exception("\n".join(cont))


if __name__ == "__main__":
    unittest.main()
