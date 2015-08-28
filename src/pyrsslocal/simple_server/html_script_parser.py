"""
@file
@brief  This modules contains a class which implements a simple server.
"""

import sys
from html.parser import HTMLParser
from html import escape
from io import StringIO
from ..helper.python_run import run_python_script


class HTMLScriptParser(HTMLParser):

    """
    defines a HTML parser.
    the purpose is to intercept section such as the following and to run it.

    @code
    <script type="text/python">
    from pandas import DataFrame
    from pyquickhelper.pandashelper.tblformat import df2html
    pars = [ { "key":k, "value":v } for k,v in params ]
    tbl = DataFrame (pars)
    print ( df2html(tbl,class_table="myclasstable") )
    </script>
    @endcode
    """

    def __init__(self, outStream=sys.stdout,
                 context={},
                 catch_exception=False):
        """
        constructor

        @param      outStream           instance of a class which should have a method ``write``
        @param      context             context for the script execution (dictionary with local variables)
        @param      catch_exception     if True, the parser prints out the exception instead of raising when it happens.

        The context is not modified unless it contains container. In that case, it could be.
        """
        HTMLParser.__init__(self, convert_charrefs=True)
        self.outStream = outStream
        self.script_stack = None
        self.context = context
        self.catch_exception = catch_exception
        self.in_script = False

        # for some reason it is missing
        self.outStream.write('<?xml version="1.0" encoding="utf-8"?>\n')

    def str_attr(self, attrs):
        """
        returns a string including the parameters values

        @param      attr        attributes
        @return                 string
        """
        if len(attrs) > 0:
            #at = [ "%s=\"%s\"" % (a,escape(b)) for a,b in attrs ]
            at = ["%s=\"%s\"" % (a, b) for a, b in attrs]
            return " " + " ".join(at)
        else:
            return ""

    def handle_starttag(self, tag, attrs):
        """
        intercepts the beginning of a tag

        @param      tag     tag
        @param      attrs   attributes
        """
        if tag.lower() == "script" and \
                len(attrs) == 1 and \
                attrs[0][0].lower() == "type" and \
                attrs[0][1].lower() == "text/python":
            self.script_stack = StringIO()
        else:
            if tag.lower() == "script":
                self.in_script = True
            self.script_stack = None
            row = "<%s%s>" % (tag, self.str_attr(attrs))
            self.outStream.write(row)

    def handle_endtag(self, tag):
        """
        intercepts the end of a tag

        @param      tag     tag
        """
        if tag.lower() == "script" and self.script_stack is not None:
            script = self.script_stack.getvalue()
            fpr = lambda v: self.outStream.write(str(v) + "\n")
            pars = {"print": fpr}
            pars.update(self.context)

            if self.catch_exception:
                try:
                    run_python_script(script, pars)
                except Exception:
                    import traceback
                    ht = '<pre class="prettyprint linenums:4">\n%s\n</pre>\nException:<pre class="prettyprint">\n' % script
                    self.outStream.write(ht)
                    traceback.print_exc(file=self.outStream)
                    self.outStream.write("\n</pre>")
            else:
                run_python_script(script, pars)

            self.script_stack = None
        else:
            if tag.lower() == "script":
                self.in_script = False
            row = "</%s>" % tag
            self.outStream.write(row)

    def handle_data(self, data):
        """
        intercepts the data between two tags

        @param      data     data
        """
        if self.script_stack is not None:
            self.script_stack.write(data)
        elif self.in_script:
            self.outStream.write(data)
        else:
            self.outStream.write(escape(data))


class HTMLScriptParserRemove(HTMLScriptParser):

    """
    defines a HTML parser.
    the purpose is to remove the HTML code and the header
    """

    def __init__(self, strict=False,
                 outStream=sys.stdout,
                 catch_exception=False):
        """
        constructor

        @param      strict              @see cl HTMLParser
        @param      outStream           instance of a class which should have a method ``write``
        @param      catch_exception     if True, the parser prints out the exception instead of raising when it happens.

        The context is not modified unless it contains container. In that case, it could be.
        """
        HTMLScriptParser.__init__(self,
                                  outStream=outStream,
                                  catch_exception=catch_exception,
                                  context={})
        self.in_ = {"head": False,
                    "meta": False,
                    "link": False,
                    "style": False,
                    "title": False
                    }

    def str_attr(self, attrs):
        """
        returns a string including the parameters values

        @param      attr        attributes
        @return                 string
        """
        if len(attrs) > 0:
            #at = [ "%s=\"%s\"" % (a,escape(b)) for a,b in attrs ]
            at = ["%s=\"%s\"" % (a, b) for a, b in attrs]
            return " " + " ".join(at)
        else:
            return ""

    def handle_starttag(self, tag, attrs):
        """
        intercepts the beginning of a tag

        @param      tag     tag
        @param      attrs   attributes
        """
        ltag = tag.lower()

        for t in ["link", "meta", "title"]:
            if self.in_[t]:
                self.in_[t] = False

        if ltag == "script":
            self.script_stack = StringIO()
        elif ltag in self.in_:
            self.in_[ltag] = True
        elif ltag == "meta":
            self.in_meta = True
        else:
            self.script_stack = None
            row = "<%s%s>" % (tag, self.str_attr(attrs))
            self.outStream.write(row)

    def handle_endtag(self, tag):
        """
        intercepts the end of a tag

        @param      tag     tag
        """
        if tag == "script" and self.script_stack is not None:
            self.script_stack = None
        elif tag in self.in_:
            self.in_[tag.lower()] = False
        else:
            row = "</%s>" % tag
            self.outStream.write(row)

    def handle_data(self, data):
        """
        intercepts the data between two tags

        @param      data     data
        """
        if True not in self.in_.values():
            if self.script_stack is not None:
                self.script_stack.write(data)
            else:
                self.outStream.write(escape(data))


if __name__ == "__main__":
    from html_string import HTMLScriptParser, html_debug_string
    st = StringIO()
    parser = HTMLScriptParser(outStream=st)
    parser.feed(html_debug_string)
    print(st.getvalue())
