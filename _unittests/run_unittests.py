"""
@file
@brief run all unit tests
"""

import unittest
import os
import sys
import io


def main():
    try:
        import pyquickhelper
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
        import pyquickhelper

    try:
        import pyensae
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
        import pyensae

    from pyquickhelper import fLOG, run_cmd, main_wrapper_tests
    fLOG(OutputPrint=True)
    main_wrapper_tests(__file__)

if __name__ == "__main__":
    main()
