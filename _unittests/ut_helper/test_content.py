"""
@brief      test log(time=0s)
"""
import unittest
from pyquickhelper.loghelper import fLOG
from pyrsslocal import write_subscriptions_example


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
