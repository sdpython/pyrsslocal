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

from pyquickhelper import fLOG
from pyensae.sql.database_main import Database
from ..simple_server.simple_server_custom import SimpleHandler, ThreadServer


class CustomDBServerHandler(SimpleHandler):

    """
    The server proposes a simple way to create one server on your own.
    It includes an access to a SQLlite3 database.
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
        returns the main page (case the server is called with no path)
        @return     default page
        """
        return self.server._my_main_page

    def get_javascript_paths(self):
        """
        returns all the location where the server should look for a java script
        @return         list of paths
        """
        return [self.server._my_root, SimpleHandler.javascript_path]

    def interpret_parameter_as_list_int(self, ps):
        """
        interpret a list of parameters, each of them is a list of integer
        separated by ,

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
        process an event, and log it

        @param      st      string to process
        """
        self.server.process_event(st)

    def serve_content_web(self, path, method, params):
        """
        functions to overload (executed after serve_content)

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
            url = path.path

            htype, ftype = self.get_ftype(url)
            for p in self.server._my_root:
                local = os.path.join(p, url.lstrip("/"))
                if os.path.exists(local):
                    break

            if htype == "text/html":
                if os.path.exists(local):
                    content = self.get_file_content(local, ftype)
                    self.send_response(200)
                    self.send_headers(path.path)

                    # context
                    params["db"] = self.server._my_database
                    params["page"] = url
                    params[
                        "website"] = "http://%s:%d/" % self.server.server_address
                    self.feed(content, True, params)
                else:
                    self.send_response(200)
                    self.send_headers("")
                    self.feed(
                        "unable to find (CustomServerHanlder): " +
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
                    "unable to find (CustomServerHanlder): " +
                    path.geturl() +
                    "\nlocal file:" +
                    local +
                    "\n")
                self.send_error(404)


class CustomDBServer (ThreadingMixIn, HTTPServer):

    """
    defines a custom server which includes an access to a database,
    this database will contain de table to store the clicks

    @example(create a custom local server)

    The following code creates an instance of a local server.
    The server expects to find its content in the same folder.

    @code
    from pyensae import Database

    db = Database(dbfile)
    df = pandas.DataFrame ( [ {"name":"xavier", "module":"pyrsslocal"} ] )
    db.connect()
    db.import_dataframe(df, "example")
    db.close()

    url = "http://localhost:%d/p_aserver.html" % port
    webbrowser.open(url)
    CustomDBServer.run_server(None, dbfile, port = port, extra_path = os.path.join("."))
    @endcode

    The main page is the following one and it can contains a Python script
    which will be interpreter by the server.
    It gives access to a variable ``db`` which is a local database
    in SQLlite.

    @code
    <?xml version="1.0" encoding="utf-8"?>
    <html>
    <head>
    <link type="text/css" href="/p_aserver.css" rel="stylesheet"/>
    <title>Custom DB Server</title>
    <meta content="dupre, pyrsslocal, custom server" name="keywords"/>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <link rel="shortcut icon" href="p_aserver.ico" />
    <meta content="CustomServer from pyrsslocal" name="description" />
    <script type="text/javascript" src="/p_aserver.js"></script>
    <script src="/js/run_prettify.js" type="text/javascript"></script>

    </head>

    <body onload="setPositions(['divtable', ])" class="mymainbody">

    <div class="divtop">
    <h1>Custom DB Server unittest</h1>
    </div>

    <div class="divtable" id="divfiles" onscroll="savePosition('divtable')">

    <h2>Content of table example</h2>

    <script type="text/python">
    print("<table>")
    db.connect()
    for row in db.execute_view("SELECT * FROM example") :
        srow = [ str(_) for _ in row ]
        print( "<tr><td>{0}</td></tr>".format("</td><td>".join(srow) ) )
    db.close()
    print("</table>")
    </script>

    <p>end.</p>

    </div>
    </body>
    </html>
    @endcode

    @endexample
    """

    @staticmethod
    def schema_table(table):
        """
        returns the schema for a specific table

        @param      table name (in ["stats", "event"])
        @return     dictionary
        """
        if table == "stats":
            return {0: ("id_post", int),
                    1: ("dtime", datetime.datetime),
                    2: ("status", str),
                    3: ("rate", int),
                    4: ("comment", str),
                    }
        elif table == "event":
            return {-1: ("id_event", int, "PRIMARYKEY", "AUTOINCREMENT"),
                    0: ("dtime", datetime.datetime),
                    1: ("uuid", str),
                    2: ("type1", str),
                    3: ("type2", str),
                    4: ("args", str),
                    }
        else:
            raise Exception("unexpected table name")

    def __init__(self,
                 server_address,
                 dbfile,
                 RequestHandlerClass=CustomDBServerHandler,
                 main_page="index.html",
                 root=None,
                 logfile=None
                 ):
        """
        constructor

        @param  server_address          addess of the server
        @param  RequestHandlerClass     it should be @see cl CustomServerHandler
        @param  dbfile                  database filename (SQLlite format)
        @param  main_page               main page for the service (when requested with no specific file)
        @param  root                    folder or list of folders where the server will look into for files such as the main page
        """
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self._my_database = Database(dbfile, LOG=fLOG)
        self._my_database_ev = Database(dbfile, LOG=fLOG)

        this = os.path.abspath(os.path.split(__file__)[0])
        if root is None:
            root = [this]
        elif isinstance(root, str):
            root = [root, this]
        elif isinstance(root, list):
            root = root + [this]
        else:
            raise TypeError("unable to interpret root: " + str(root))

        self._my_root = root
        self._my_main_page = main_page
        self._my_address = server_address
        fLOG("CustomServer.init: root=", root)
        fLOG("CustomServer.init: db=", dbfile)

        self.table_event = "cs_events"
        self.table_stats = "cs_stats"

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

        self._my_database_ev.connect()
        if not self._my_database_ev.has_table(self.table_stats):
            schema = CustomDBServer.schema_table("stats")
            self._my_database_ev.create_table(self.table_stats, schema)
            self._my_database_ev.commit()
            self._my_database_ev.create_index(
                "id_post_" +
                self.table_stats,
                self.table_stats,
                "id_post",
                False)
            self._my_database_ev.commit()

        if not self._my_database_ev.has_table(self.table_event):
            schema = CustomDBServer.schema_table("event")
            self._my_database_ev.create_table(self.table_event, schema)
            self._my_database_ev.commit()
        self._my_database_ev.close()

    def __enter__(self):
        """
        what to do when creating the class
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        what to do when removing the instance (close the log file)
        """
        if self.flog is not None and self.logfile != "stdout":
            self.flog.close()

    def process_event(self, event):
        """
        process an event, it expects a format like the following:

        @code
        type1/uuid/type2/args
        @endcode

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
        self._my_database_ev.insert(self.table_event, values)
        if status is not None:
            self._my_database_ev.insert(self.table_stats, status)
        self._my_database_ev.commit()
        self._my_database_ev.close()

    @staticmethod
    def run_server(server, dbfile, thread=False, port=8080, logfile=None,
                   extra_path=None):
        """
        start the server

        @param      server      if None, it becomes ``CustomServer(dbfile, ('localhost', 8080), CustomServerHandler)``
        @param      dbfile      file to the RSS database (SQLite)
        @param      thread      if True, the server is run in a thread
                                and the function returns right away,
                                otherwite, it runs the server.
        @param      port        port to use
        @param      logfile     file for the log or "stdout" for the standard output
        @param      extra_path  additional path the server should look into to find a page
        @return                 server if thread is False, the thread otherwise (the thread is started)

        @warning If you kill the python program while the thread is still running, python interpreter might be closed completely.

        """
        if server is None:
            server = CustomDBServer(
                ('localhost',
                 port),
                dbfile,
                CustomDBServerHandler,
                logfile=logfile,
                root=extra_path)
        if thread:
            th = ThreadServer(server)
            th.start()
            return th
        else:
            server.serve_forever()
            return server
