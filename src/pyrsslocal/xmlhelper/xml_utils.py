# -*- coding: utf-8 -*-
"""
@file
@brief  parsing XML
"""

import re
import xml.sax.saxutils as saxutils
import xml.sax.saxutils as htmlentitydefs


def escape(s):
    """
    @param      s       string to escape
    @return             escaped string
    """
    if isinstance(s, list):
        return [escape(_) for _ in s]
    else:
        s = saxutils.escape(s)
        s = s.replace("&", "&amp;")
        return s


def html_unescape(text):
    """Removes HTML or XML character references
      and entities from a text string.
      keep ``&amp;``, ``&gt;``, ``&lt;`` in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                if text[1:-1] == "amp":
                    text = "&amp;amp;"
                elif text[1:-1] == "gt":
                    text = "&amp;gt;"
                elif text[1:-1] == "lt":
                    text = "&amp;lt;"
                else:
                    text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\\w+;", fixup, text)


character_to_escape = {
    "é": "&eacute;",
    " ": "&nbsp;",
    "è": "&egrave;",
    "à": "&agrave;",
    "â": "&acirc;",
    "ê": "&ecirc;",
    "ë": "&euml;",
    "î": "&icirc;",
    "ù": "&ugrave;",
    "ü": "&uuml;",
    "ô": "&ocirc;",
    "œ": "&oelig;",
}


def html_escape(text):
    """escape any French character with an accent
    """
    def fixup(m):
        text = m.group(0)
        return character_to_escape.get(text, text)
    return re.sub("[àâäéèêëîïôöùüü]", fixup, text)
