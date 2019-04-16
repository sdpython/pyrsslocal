"""
@file
@brief  This modules contains a class which implements a simple server.
"""

import sys
import os
import subprocess
import copy
import io
import getpass
from urllib.parse import urlparse, parse_qs
from io import StringIO
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyquickhelper.loghelper import fLOG
from pyquickhelper.filehelper import get_url_content_timeout
from .html_script_parser import HTMLScriptParser, HTMLScriptParserRemove
from .html_string import html_footer, html_header, html_debug_string


def get_path_javascript():
    """
    *pyrsslocal* contains some javascript script, it adds the paths
    to the paths where content will be looked for.

    @return         a path
    """
    filepath = os.path.split(__file__)[0]
    jspath = os.path.normpath(
        os.path.abspath(
            os.path.join(
                filepath,
                "..",
                "javascript")))
    if not os.path.exists(jspath):
        raise FileNotFoundError(jspath)
    return jspath


class SimpleHandler(BaseHTTPRequestHandler):
    """
    Defines a simple handler used by *HTTPServer*.
    Firefox works better for local files.

    This class provides the following function associated to ``/localfile``:

   * if the url is ``http://localhost:port/localfile/<filename>``, it display this file
   * you add a path parameter: ``http://localhost:port/localfile/<filename>?path=<path>``
     to tell the service to look into a different folder
   * you add a parameter ``&execute=False`` for python script if you want to display them, not to run them.
   * you can add a parameter ``&keep``, the class retains the folder and will look further files in this list

    See `Python documentation <http://docs.python.org/3/library/http.server.html>`_

    @warning Some information about pathes are stored in a unique queue but it should be done in cookie or in session data.
             An instance of SimpleHandler is created for each session and it is better to assume
             you cannot add member to this class.
    """

    # this queue will keep some pathes which should be stored in session
    # information or in cookies
    queue_pathes = list()
    javascript_path = get_path_javascript()

    def add_path(self, p):
        """
        Adds a local path to the list of path to watch.
        @param  p       local path to data

        *Python* documentation says list are proctected against multithreads (concurrent accesses).
        """
        if p not in SimpleHandler.queue_pathes:
            SimpleHandler.queue_pathes.append(p)

    def get_pathes(self):
        """
        Returns a list of local path where to look for a local file.
        @return         a list of pathes
        """
        return copy.copy(SimpleHandler.queue_pathes)

    def __init__(self, request, client_address, server):
        """
        Regular constructor, an instance is created for each request,
        do not store any data for a longer time than a request.
        """
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def log_message(self, format, *args):  # pylint: disable=W0622
        """
        Logs an arbitrary message. Overloads the original method.

        This is used by all other logging functions.  Override
        it if you have specific logging wishes.

        The first argument, FORMAT, is a format string for the
        message to be logged.  If the format string contains
        any % escapes requiring parameters, they should be
        specified as subsequent arguments (it's just like
        printf!).

        The client ip and current date/time are prefixed to
        every message.
        """
        self.private_LOG("- %s - %s\n" %
                         (self.address_string(),
                          format % args))

    def LOG(self, *args):
        """
        To log, it appends various information about the id address...
        @param      args       string to LOG or list of strings to LOG
        """
        self.private_LOG("- %s -" %
                         (self.address_string(),),
                         *args)

    def private_LOG(self, *s):
        """
        To log
        @param      s       string to LOG or list of strings to LOG
        """
        fLOG(*s)

    def do_GET(self):
        """
        What to do is case of GET request.
        """
        parsed_path = urlparse(self.path)
        self.serve_content(parsed_path, "GET")
        # self.wfile.close()

    def do_POST(self):
        """
        What to do is case of POST request.
        """
        parsed_path = urlparse(self.path)
        self.serve_content(parsed_path)
        # self.wfile.close()

    def do_redirect(self, path="/index.html"):
        """
        Redirection when url is just the website.
        @param      path        path to redirect to (a string)
        """
        self.send_response(301)
        self.send_header('Location', path)
        self.end_headers()

    def get_ftype(self, path):
        """
        Defines the header to send (type of files) based on path.
        @param      path        location (a string)
        @return                 htype, ftype (html, css, ...)
        """
        htype = ''
        ftype = ''

        if path.endswith('.js'):
            htype = 'application/javascript'
            ftype = 'r'
        elif path.endswith('.css'):
            htype = 'text/css'
            ftype = 'r'
        elif path.endswith('.html'):
            htype = 'text/html'
            ftype = 'r'
        elif path.endswith('.py'):
            htype = 'text/html'
            ftype = 'execute'
        elif path.endswith('.png'):
            htype = 'image/png'
            ftype = 'rb'
        elif path.endswith('.jpg'):
            htype = 'image/jpeg'
            ftype = 'rb'
        elif path.endswith('.jepg'):
            htype = 'image/jpeg'
            ftype = 'rb'
        elif path.endswith('.ico'):
            htype = 'image/x-icon'
            ftype = 'rb'
        elif path.endswith('.gif'):
            htype = 'image/gif'
            ftype = 'rb'

        return htype, ftype

    def send_headers(self, path):
        """
        Defines the header to send (type of files) based on path.
        @param      path        location (a string)
        @return                 type (html, css, ...)
        """
        htype, ftype = self.get_ftype(path)

        if htype != '':
            self.send_header('Content-type', htype)
            self.end_headers()
        else:
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        return ftype

    def get_file_content(self, localpath, ftype, path=None):
        """
        Returns the content of a local file. The function also looks into
        folders in ``self.__pathes`` to see if the file can be found in one of the
        folder when not found in the first one.

        @param      localpath       local filename
        @param      ftype           r or rb
        @param      path            if != None, the filename will be path/localpath
        @return                     content
        """
        if path is not None:
            tlocalpath = os.path.join(path, localpath)
        else:
            tlocalpath = localpath

        if not os.path.exists(tlocalpath):
            for p in self.get_pathes():
                self.LOG("trying ", p)
                tloc = os.path.join(p, localpath)
                if os.path.exists(tloc):
                    tlocalpath = tloc
                    break

        if not os.path.exists(tlocalpath):
            self.send_error(404)
            content = "unable to find file " + localpath
            self.LOG(content)
            return content

        if ftype in ("r", "execute"):
            self.LOG("reading file ", tlocalpath)
            with open(tlocalpath, "r", encoding="utf8") as f:
                return f.read()
        else:
            self.LOG("reading file ", tlocalpath)
            with open(tlocalpath, "rb") as f:
                return f.read()

    def execute(self, localpath):
        """
        Locally execute a python script.
        @param      localpath       local python script
        @return                     output, error
        """
        exe = subprocess.Popen([sys.executable, localpath],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        out, error = exe.communicate()
        return out, error

    def feed(self, any_, script_python=False, params=None):
        """
        Displays something.

        @param      any_                string
        @param      script_python       if True, the function processes script sections
        @param      params              extra parameters, see @me process_scripts

        A script section looks like:

        ::

            <script type="text/python">
            from pandas import DataFrame
            pars = [ { "key":k, "value":v } for k,v in params ]
            tbl = DataFrame (pars)
            print ( tbl.tohtml(class_table="myclasstable") )
            </script>
        """
        if params is None:
            params = {}

        if isinstance(any_, bytes):
            if script_python:
                raise SystemError("unable to execute script from bytes")
            self.wfile.write(any_)
        else:
            if script_python:
                any_ = self.process_scripts(any_, params)
            text = any_.encode("utf-8")
            self.wfile.write(text)

    def shutdown(self):
        """
        Shuts down the service from the service itself (not from another thread).
        For the time being, the function generates the following exception:

        ::

            Traceback (most recent call last):
              File "simple_server_custom.py", line 225, in <module>
                run_server(None)
              File "simple_server_custom.py", line 219, in run_server
                server.serve_forever()
              File "c:\\python33\\lib\\socketserver.py", line 237, in serve_forever
                poll_interval)
              File "c:\\python33\\lib\\socketserver.py", line 155, in _eintr_retry
                return func(*args)
            ValueError: file descriptor cannot be a negative integer (-1)

        A better way to shut it down should is recommended. The use of the function:

        ::

            self.server.shutdown()

        freezes the server because this function should not be run in the same thread.
        """
        # self.server.close()
        # help(self.server.socket)
        # self.server.socket.shutdown(socket.SHUT_RDWR)
        self.server.socket.close()
        # self.server.shutdown()
        fLOG("end of shut down")

    def main_page(self):
        """
        Returns the main page (case the server is called
        with no path).
        @return     default page
        """
        return "index.html"

    def serve_content(self, path, method="GET"):
        """
        Tells what to do based on the path. The function intercepts the
        path ``/localfile/``, otherwise it calls ``serve_content_web``.

        If you type ``http://localhost:8080/localfile/__file__``,
        it will display this file.

        @param      path        ParseResult
        @param      method      GET or POST
        """
        if path.path == "" or path.path == "/":
            temp = "/" + self.main_page()
            self.do_redirect(temp)

        else:
            params = parse_qs(path.query)
            params["__path__"] = path
            # here you might want to look into a local path... f2r = HOME +
            # path

            url = path.geturl()
            params["__url__"] = path

            if url.startswith("/localfile/"):
                localpath = path.path[len("/localfile/"):]
                self.LOG("localpath ", localpath, os.path.isfile(localpath))

                if localpath == "shutdown":
                    self.LOG("call shutdown")
                    self.shutdown()

                elif localpath == "__file__":
                    self.LOG("display file __file__", localpath)
                    self.send_response(200)
                    self.send_headers("__file__.txt")
                    content = self.get_file_content(__file__, "r")
                    self.feed(content)

                else:
                    self.send_response(200)
                    _, ftype = self.get_ftype(localpath)
                    execute = eval(params.get("execute", ["True"])[  # pylint: disable=W0123
                                   0])  # pylint: disable=W0123
                    path = params.get("path", [None])[0]
                    keep = eval(params.get("keep", ["False"])[  # pylint: disable=W0123
                                0])  # pylint: disable=W0123
                    if keep and path not in self.get_pathes():
                        self.LOG(
                            "execute",
                            execute,
                            "- ftype",
                            ftype,
                            " - path",
                            path,
                            " keep ",
                            keep)
                        self.add_path(path)
                    else:
                        self.LOG(
                            "execute",
                            execute,
                            "- ftype",
                            ftype,
                            " - path",
                            path)

                    if ftype != 'execute' or not execute:
                        content = self.get_file_content(localpath, ftype, path)
                        ext = os.path.splitext(localpath)[-1].lower()
                        if ext in [
                                ".py", ".c", ".cpp", ".hpp", ".h", ".r", ".sql", ".js", ".java", ".css"]:
                            self.send_headers(".html")
                            self.feed(
                                self.html_code_renderer(
                                    localpath,
                                    content))
                        else:
                            self.send_headers(localpath)
                            self.feed(content)
                    else:
                        self.LOG("execute file ", localpath)
                        out, err = self.execute(localpath)
                        if len(err) > 0:
                            self.send_error(404)
                            self.feed(
                                "Requested resource %s unavailable" %
                                localpath)
                        else:
                            self.send_headers(localpath)
                            self.feed(out)

            elif url.startswith("/js/"):
                found = None
                for jspa in self.get_javascript_paths():
                    file = os.path.join(jspa, url[4:])
                    if os.path.exists(file):
                        found = file

                if found is None:
                    self.send_response(200)
                    self.send_headers("")
                    self.feed(
                        "Unable to serve content for url: '{}'.".format(path.geturl()))
                    self.send_error(404)
                else:
                    _, ft = self.get_ftype(found)
                    if ft == "r":
                        try:
                            with open(found, ft, encoding="utf8") as f:
                                content = f.read()
                        except UnicodeDecodeError as e:
                            self.LOG("file is not utf8", found)
                            with open(found, ft) as f:
                                content = f.read()
                    else:
                        self.LOG("reading binary")
                        with open(found, ft) as f:
                            content = f.read()

                    self.send_response(200)
                    self.send_headers(found)
                    self.feed(content)

            elif url.startswith("/debug_string/"):
                # debugging purposes
                self.send_response(200)
                self.send_headers("debug.html")
                self.feed(html_debug_string, False, params)

            elif url.startswith("/fetchurlclean/"):
                self.send_response(200)
                self.send_headers("debug.html")
                url = path.path.replace("/fetchurlclean/", "")
                try:
                    content = get_url_content_timeout(url)
                except Exception as e:
                    content = "<html><body>ERROR (1): %s</body></html>" % e
                if content is None or len(content) == 0:
                    content = "<html><body>ERROR (1): content is empty</body></html>"

                stre = io.StringIO()
                pars = HTMLScriptParserRemove(outStream=stre)
                pars.feed(content)
                content = stre.getvalue()

                self.feed(content, False, params={})

            elif url.startswith("/fetchurl/"):
                self.send_response(200)
                self.send_headers("debug.html")
                url = path.path.replace("/fetchurl/", "")
                try:
                    content = get_url_content_timeout(url)
                except Exception as e:
                    content = "<html><body>ERROR (2): %s</body></html>" % e
                self.feed(content, False, params={})

            else:
                self.serve_content_web(path, method, params)

    def get_javascript_paths(self):
        """
        Returns all the location where the server should
        look for a java script.
        @return         list of paths
        """
        return [SimpleHandler.javascript_path]

    def html_code_renderer(self, localpath, content):
        """
        Produces a :epkg:`html` code for code.

        @param      localpath   local path to file (local or not)
        @param      content     content of the file
        @return                 html string
        """
        res = [html_header % (localpath, getpass.getuser(), "code")]
        res.append("<pre class=\"prettyprint\">")
        res.append(content.replace("<", "&lt;").replace(">", "&gt;"))
        res.append(html_footer)
        return "\n".join(res)

    def serve_content_web(self, path, method, params):
        """
        Functions to overload (executed after serve_content).

        @param      path        ParseResult
        @param      method      GET or POST
        @param      params      params parsed from the url + others
        """
        self.send_response(200)
        self.send_headers("")
        self.feed("Unable to serve content for url: '{}'\n{}".format(
            path.geturl(), str(params)))
        self.send_error(404)

    def process_scripts(self, content, params):
        """
        Parses a :epkg:`HTML` string, extract script section
        (only python script for the time being)
        and returns the final page.

        @param      content     html string
        @param      params      dictionary with what is known from the server
        @return                 html content
        """
        st = StringIO()
        parser = HTMLScriptParser(
            outStream=st,
            catch_exception=True,
            context=params)
        parser.feed(content)
        res = st.getvalue()
        return res


class ThreadServer (Thread):
    """
    Defines a thread which holds a web server.

    @var    server      the server of run
    """

    def __init__(self, server):
        """
        @param      server to run
        """
        Thread.__init__(self)
        self.server = server

    def run(self):
        """
        Runs the server.
        """
        self.server.serve_forever()

    def shutdown(self):
        """
        Shuts down the server, if it does not work,
        you can still kill the thread:

        ::

            self.kill()
        """
        self.server.shutdown()
        self.server.server_close()


def run_server(server, thread=False, port=8080):
    """
    Runs the server.
    @param      server      if None, it becomes ``HTTPServer(('localhost', 8080), SimpleHandler)``
    @param      thread      if True, the server is run in a thread
                            and the function returns right away,
                            otherwite, it runs the server.
    @param      port        port to use
    @return                 server if thread is False, the thread otherwise (the thread is started)

    @warning If you kill the python program while the thread is still running, python interpreter might be closed completely.
    """
    if server is None:
        server = HTTPServer(('localhost', port), SimpleHandler)
    if thread:
        th = ThreadServer(server)
        th.start()
        return th
    else:
        server.serve_forever()
        return server


if __name__ == '__main__':
    fLOG(OutputPrint=True)
    fLOG("running server")
    run_server(None)
    fLOG("end running server")

    # http://localhost:8080/localfile/D:\Dupre\_data\informatique\support\python_td_2013\programme\td9_by_hours.json
    # http://localhost:8080/localfile/tag-cloud.html?path=D:\Dupre\_data\program\pyhome\pyhome3\_nrt\nrt_internet\data&keep=True
    # http://localhost:8080/debug_string/

    """
    from pyquickhelper.loghelper import fLOG
    from pyrsslocal.internet.simple_server.simple_server_custom import run_server

    fLOG(OutputPrint=True)
    fLOG("running server")
    run_server(None)
    fLOG("end running server")
    """
