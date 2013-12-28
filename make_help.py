"""
generates the documentation using Sphinx
"""
import sys, os

try:
    import pyquickhelper, pyensae
except ImportError:
    sys.path.append ( os.path.normpath (os.path.join( os.path.abspath("."), "..", "pyquickhelper", "src")))
    import pyquickhelper
    sys.path.append ( os.path.normpath (os.path.join( os.path.abspath("."), "..", "pyensae", "src")))
    import pyensae
    
from pyquickhelper                      import fLOG
from pyquickhelper.helpgen.sphinx_main  import generate_help_sphinx

if __name__ == "__main__" :
    fLOG (OutputPrint = True)
    generate_help_sphinx("pyrsslocal")
    
