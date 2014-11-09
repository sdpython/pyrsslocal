"""
@brief      test log(time=0s)
"""

import sys, os, unittest, re


try :
    import src
    import pyquickhelper
    import pyensae
except ImportError :
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..")))
    if path not in sys.path : sys.path.append (path)
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..", "..", "pyquickhelper", "src")))
    if path not in sys.path : sys.path.append (path)
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..", "..", "pyensae", "src")))
    if path not in sys.path : sys.path.append (path)
    import src
    import pyquickhelper
    import pyensae

from pyquickhelper import fLOG
from src.pyrsslocal import get_subscriptions_example


class TestContent (unittest.TestCase):
    
    def test_sample(self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        cont = get_subscriptions_example()
        assert len(cont)>0


if __name__ == "__main__"  :
    unittest.main ()    
