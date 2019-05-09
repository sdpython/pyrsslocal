# -*- coding: utf-8 -*-
"""
@file
@brief Implements command line ``python -m pyrsslocal <command> <args>``.

.. versionadded:: 0.9
"""
import sys


def main(args, fLOG=print):
    """
    Implements ``python -m pyrsslocal <command> <args>``.

    @param      args        command line arguments
    @param      fLOG        logging function
    """
    from pyquickhelper.cli import cli_main_helper
    try:
        from .cli.merge_rss import compile_rss_blogs
    except ImportError:
        from pyrsslocal.cli.merge_rss import compile_rss_blogs

    fcts = dict(compile_rss_blogs=compile_rss_blogs)
    return cli_main_helper(fcts, args=args, fLOG=fLOG)


if __name__ == "__main__":
    main(sys.argv[1:])
