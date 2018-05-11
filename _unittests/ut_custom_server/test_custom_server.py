"""
@brief      test log(time=4s)
"""


import sys
import os
import unittest
import pandas


try:
    import src
    import pyquickhelper as skip_
    import pyensae as skip__
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyensae",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import src
    import pyquickhelper as skip_
    import pyensae as skip__

from pyquickhelper.loghelper import fLOG
from pyensae.sql.database_main import Database
from src.pyrsslocal.custom_server.aserver import CustomDBServer, CustomDBServerHandler
from src.pyrsslocal.helper.download_helper import get_url_content_timeout


class TestCustomServer(unittest.TestCase):

    def test_custom_server(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        fold = os.path.abspath(os.path.split(__file__)[0])
        dbfile = os.path.join(fold, "out_custom_server.db3")
        if os.path.exists(dbfile):
            os.remove(dbfile)

        db = Database(dbfile, LOG=fLOG)
        df = pandas.DataFrame([{"name": "xavier", "module": "pyrsslocal"}])
        db.connect()
        db.import_dataframe(df, "example")
        db.close()

        server = CustomDBServer(
            ('localhost',
             8097),
            dbfile,
            CustomDBServerHandler)
        thread = CustomDBServer.run_server(server, dbfile=dbfile, thread=True)

        url = "http://localhost:8097/p_aserver.html"
        cont = get_url_content_timeout(url)
        assert len(cont) > 0
        assert "xavier" in cont

        thread.shutdown()
        assert not thread.is_alive()

        assert os.path.exists(dbfile)

    def test_custom_server_location(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        fold = os.path.abspath(os.path.split(__file__)[0])
        dbfile = os.path.join(fold, "out_custom_server2.db3")
        if os.path.exists(dbfile):
            os.remove(dbfile)

        db = Database(dbfile, LOG=fLOG)
        df = pandas.DataFrame([{"name": "xavier", "module": "pyrsslocal"}])
        db.connect()
        db.import_dataframe(df, "example")
        db.close()

        server = CustomDBServer(('localhost', 8099), dbfile, CustomDBServerHandler,
                                root=os.path.join(fold, "data"))
        thread = CustomDBServer.run_server(server, dbfile=dbfile, thread=True,
                                           extra_path=os.path.join(fold, "data"))

        url = "http://localhost:8099/index.html"
        cont = get_url_content_timeout(url)
        assert len(cont) > 0
        assert "unittest" in cont

        thread.shutdown()
        assert not thread.is_alive()
        assert os.path.exists(dbfile)


if __name__ == "__main__":

    enabled = False
    if enabled:
        import webbrowser
        port = 8098
        fold = os.path.abspath(os.path.split(__file__)[0])
        dbfile = os.path.join(fold, "out_custom_server.db3")

        db = Database(dbfile)
        df = pandas.DataFrame([{"name": "xavier", "module": "pyrsslocal"}])
        db.connect()
        db.import_dataframe(df, "example")
        db.close()

        url = "http://localhost:%d/p_aserver.html" % port
        fLOG("opening ", url)
        webbrowser.open(url)
        CustomDBServer.run_server(
            None,
            dbfile,
            port=port,
            extra_path=os.path.join(
                fold,
                "data"))

    unittest.main()
