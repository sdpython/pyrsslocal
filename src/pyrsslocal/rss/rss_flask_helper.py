"""
@file
@brief Helpers for ``rss_flask.py``.
"""

import os


def root_dir():
    """
    Returns this directory.
    @return     this path
    """
    return os.path.abspath(os.path.dirname(__file__))


def load_page(filename):
    """
    Loads the content of a file.
    """
    fold = root_dir()
    full = os.path.abspath(os.path.join(fold, filename))
    with open(full, "r", encoding="utf8") as f:
        content = f.read()
        return content


def get_text_file(filename):
    """
    Returns the content of a text filename.

    @param      filename        relative filename
    @return                     content
    """
    src = os.path.join(root_dir(), filename)
    with open(src, "r", encoding="utf8") as f:
        return f.read()


def get_binary_file(filename):
    """
    Returns the content of a binary filename.

    @param      filename        relative filename
    @return                     content
    """
    src = os.path.join(root_dir(), filename)
    with open(src, "rb") as f:
        return f.read()

# -- HELP BEGIN EXCLUDE --


main_page_content = load_page("rss_reader.html")


# -- HELP END EXCLUDE --
