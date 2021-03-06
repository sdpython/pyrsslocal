"""
@file
@brief  This modules contains a class which implements a simple server.
"""

import sys
import os
import urllib
import datetime
from http.server import HTTPServer
from socketserver import ThreadingMixIn
from .rss_database import DatabaseRSS
from ..simple_server.simple_server_custom import SimpleHandler, ThreadServer


class RSSSimpleHandler(SimpleHandler):

    """
    You can read the blog post `RSS Reader
    <http://www.xavierdupre.fr/blog/2013-07-28_nojs.html>`_.
    Defines a simple handler used by HTTPServer.
    Firefox works better for local files.
    This server serves RSS content.

    For every section containing a python script, the class will add a local
    variable ``dbrss`` which gives access to the blogs database.
    That's why the following section works:

    ::

        <script type="text/python">
        for blogs in dbrss.enumerate_blogs() :
            print (blogs.html())
        </script>

    Whenever a url is preceded by ``/logs/click/```,
    the class will log an event in the logs.
    The final page will look like this:

    @image images/page1.png

    .. faqref:
        :title: The server is slow or does not respond to a click)

        For some reason, it usually happens on Firefox.
        Chrome works better. The script python embedded in the HTML page
        and interpreted by the server make it slow to run.
        It should be replaced by javascript. Maybe Firefox detects the answer is not
        fast enough and it requires one or two more clicks to get the server to respond.
    """

    def __init__(self, request, client_address, server):
        """
        Regular constructor, an instance is created for each request,
        do not store any data for a longer time than a request.
        """
        SimpleHandler.__init__(self, request, client_address, server)
        #self.m_database  = server._my_database
        #self.m_main_page = server._my_main_page
        #self.m_root      = server._my_root

    def main_page(self):
        """
        Returns the main page (case the server is called with no path).
        @return     default page
        """
        return self.server._my_main_page

    def get_javascript_paths(self):
        """
        Returns all the location where the server should look for a java script.
        @return         list of paths
        """
        return [self.server._my_root, SimpleHandler.javascript_path]

    def interpret_parameter_as_list_int(self, ps):
        """
        Interprets a list of parameters, each of them is a list of integer
        separated by ``,``.

        @param      ps      something like ``params.get("blog_selected")``
        @return             list of int
        """
        res = []
        for ins in ps:
            spl = ins.split(",")
            ii = [int(_) for _ in spl]
            res.extend(ii)
        return res

    def process_event(self, st):
        """
        Processes an event, and log it.

        @param      st      string to process
        """
        self.server.process_event(st)

    def serve_content_web(self, path, method, params):
        """
        Functions to overload (executed after serve_content).

        @param      path        ParseResult
        @param      method      GET or POST
        @param      params      params parsed from the url + others
        """
        if path.path.startswith("/logs/"):
            url = path.path[6:]
            targ = urllib.parse.unquote(url)
            self.process_event(targ)
            self.send_response(200)
            self.send_headers("")
        else:
            if path.path.startswith("/rssfetchlocalexe/"):
                url = path.path.replace("/rssfetchlocalexe/", "")
            else:
                url = path.path

            htype, ftype = self.get_ftype(url)
            local = os.path.join(self.server._my_root, url.lstrip("/"))
            if htype == "text/html":
                if os.path.exists(local):
                    content = self.get_file_content(local, ftype)
                    self.send_response(200)
                    self.send_headers(path.path)

                    # context
                    params["dbrss"] = self.server._my_database
                    params["main_page"] = url
                    params["blog_selected"] = self.interpret_parameter_as_list_int(
                        params.get(
                            "blog_selected",
                            []))
                    params["post_selected"] = self.interpret_parameter_as_list_int(
                        params.get(
                            "post_selected",
                            []))
                    params["search"] = params.get("search", [None])[0]
                    params[
                        "website"] = "http://%s:%d/" % self.server.server_address
                    self.feed(content, True, params)
                else:
                    self.send_response(200)
                    self.send_headers("")
                    self.feed(
                        "unable to find (RSSSimpleHandler): " +
                        path.geturl() +
                        "\nlocal file:" +
                        local +
                        "\n")
                    self.send_error(404)

            elif os.path.exists(local):
                content = self.get_file_content(local, ftype)
                self.send_response(200)
                self.send_headers(url)
                self.feed(content, False, params)

            else:
                self.send_response(200)
                self.send_headers("")
                self.feed(
                    "unable to find (RSSSimpleHandler): " +
                    path.geturl() +
                    "\nlocal file:" +
                    local +
                    "\n")
                self.send_error(404)


class RSSServer(ThreadingMixIn, HTTPServer):
    """
    Defines a :epkg:`RSS` server dedicated to one specific database.
    You can read the blog post `RSS Reader
    <http://www.xavierdupre.fr/blog/2013-07-28_nojs.html>`_.
    """

    def __init__(self, server_address, dbfile,
                 RequestHandlerClass=RSSSimpleHandler,
                 main_page="rss_reader.html",
                 root=os.path.abspath(os.path.split(__file__)[0]),
                 logfile=None, fLOG=None):
        """
        @param  server_address          address of the server
        @param  RequestHandlerClass     it should be @see cl RSSSimpleHandler
        @param  dbfile                  database filename (SQLlite format)
        @param  main_page               main page for the service (when requested with no specific file)
        @param  root                    folder when the server will look into for files such as the main page
        @param  fLOG                    logging function
        """
        if fLOG:
            fLOG("RSSServer.init: begin server")
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        if fLOG:
            fLOG("RSSServer.init: begin db rss")
        self._my_database = DatabaseRSS(dbfile, LOG=fLOG)
        if fLOG:
            fLOG("RSSServer.init: begin db event")
        self._my_database_ev = DatabaseRSS(dbfile, LOG=fLOG)
        if fLOG:
            fLOG("RSSServer.init: end db")
        self._my_root = root
        self._my_main_page = main_page
        self._my_address = server_address
        if SimpleHandler == RequestHandlerClass:
            raise TypeError("this request handler should not be SimpleHandler")
        if fLOG:
            fLOG("RSSServer.init: root=", root)
            fLOG("RSSServer.init: db=", dbfile)

        self.logfile = logfile
        if self.logfile is not None:
            if self.logfile == "stdout":
                self.flog = sys.stdout
            elif isinstance(self.logfile, str):
                self.flog = open(self.logfile, "a", encoding="utf8")
            else:
                self.flog = self.logfile
        else:
            self.flog = None

    def __enter__(self):
        """
        What to do when creating the class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # pylint: disable=W0221
        """
        What to do when removing the instance (close the log file).
        """
        if self.flog is not None and self.logfile != "stdout":
            self.flog.close()

    def process_event(self, event):
        """
        Processes an event, it expects a format like the following:

        ::

            type1/uuid/type2/args

        @param      event   string to log
        """
        now = datetime.datetime.now()
        if self.flog is not None:
            self.flog.write(str(now) + " " + event)
            self.flog.write("\n")
            self.flog.flush()

        info = event.split("/")

        status = None
        if len(info) >= 4 and info[2] == "status":
            status = {"status": info[4],
                      "id_post": int(info[3]),
                      "dtime": now,
                      "rate": -1,
                      "comment": ""}

        if len(info) > 4:
            info[3:] = ["/".join(info[3:])]
        if len(info) < 4:
            raise OSError("unable to log event: " + event)

        values = {"type1": info[0],
                  "uuid": info[1],
                  "type2": info[2],
                  "dtime": now,
                  "args": info[3]}

        # to avoid database to collide
        iscon = self._my_database_ev.is_connected()
        if iscon:
            if self.flog is not None:
                self.flog.write("unable to connect the database")
                if status is not None:
                    self.flog.write("unable to update status: " + str(status))
            return

        self._my_database_ev.connect()
        self._my_database_ev.insert(self._my_database.table_event, values)
        if status is not None:
            self._my_database_ev.insert(self._my_database.table_stats, status)
        self._my_database_ev.commit()
        self._my_database_ev.close()

    @staticmethod
    def run_server(server, dbfile, thread=False, port=8080,
                   logfile=None, fLOG=None):
        """
        Starts the server.

        @param      server      None or string, see below
        @param      dbfile      file to the RSS database (SQLite)
        @param      thread      if True, the server is run in a thread
                                and the function returns right away,
                                otherwite, it runs the server.
        @param      port        port to use
        @param      logfile     file for the log or "stdout" for the standard output
        @param      fLOG        logging function
        @return                 server if thread is False, the thread otherwise (the thread is started)

        About the parameter ``server``:

        * ``None``, it becomes ``RSSServer(('localhost', 8080), dbfile, RSSSimpleHandler)``
        * ``<server>``, it becomes ``RSSServer((server, 8080), dbfile, RSSSimpleHandler)``

        @warning If you kill the python program while the thread is still running,
                 python interpreter might be closed completely.
        """
        if server is None:
            server = RSSServer(
                ('localhost',
                 port),
                dbfile,
                RSSSimpleHandler,
                logfile=logfile,
                fLOG=fLOG)
        elif isinstance(server, str):
            server = RSSServer(
                (server,
                 port),
                dbfile,
                RSSSimpleHandler,
                logfile=logfile,
                fLOG=fLOG)
        if thread:
            th = ThreadServer(server)
            th.start()
            return th
        else:
            server.serve_forever()
            return server
