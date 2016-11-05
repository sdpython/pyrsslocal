"""
@file
@brief run all unit tests
"""
import os
import sys


def main():
    try:
        import pyquickhelper as skip_
    except ImportError:
        sys.path.append(
            os.path.normpath(
                os.path.abspath(
                    os.path.join(
                        os.path.split(__file__)[0],
                        "..",
                        "..",
                        "pyquickhelper",
                        "src"))))
        import pyquickhelper as skip_

    try:
        import pyensae as skip__
    except ImportError:
        sys.path.append(
            os.path.normpath(
                os.path.abspath(
                    os.path.join(
                        os.path.split(__file__)[0],
                        "..",
                        "..",
                        "pyensae",
                        "src"))))
        import pyensae as skip__

    from pyquickhelper.loghelper import fLOG
    from pyqcuikhelper.pycode import main_wrapper_tests
    fLOG(OutputPrint=True)
    main_wrapper_tests(__file__)


if __name__ == "__main__":
    main()
