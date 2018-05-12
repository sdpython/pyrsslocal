"""
@brief      test log(time=0s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG


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

from src.pyrsslocal import write_subscriptions_example


class TestContent (unittest.TestCase):

    def test_sample(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        cont = write_subscriptions_example()
        assert len(cont) > 0


if __name__ == "__main__":
    unittest.main()
