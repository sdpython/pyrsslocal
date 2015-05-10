"""
@file
@brief Various function to automate the collection of blog posts.
"""
import os
import webbrowser
import sys

from .rss_stream import StreamRSS
from .rss_blogpost import BlogPost
from pyquickhelper.loghelper.flog import fLOG
from pyensae.sql.database_main import Database
from .rss_simple_server import RSSServer


def rss_from_xml_to_database(file,
                             database="database_rss.db3",
                             table="blogs"):
    """
    parses a list of blogs stored in a XML file using Google Reader format,
    stores the results in a SQLite database

    @param  file            (str) xml file containing the list of blogs, example:
    @param  database        database file (sqlite)
    @param  table           table name
    @return                 number of stored blogs

    The XML file should contain the following:
    @code
        <outline text="XD blog"
                title="XD blog" type="rss"
                xmlUrl="http://www.xavierdupre.fr/blog/xdbrss.xml"
                htmlUrl="http://www.xavierdupre.fr/blog/xd_blog.html" />
    @endcode

    The function does not check whether or not the blogs were already added to the database,
    they will be added a second time. If the table does not exist, it will be created.
    """
    res = list(StreamRSS.enumerate_stream_from_google_list(file))
    db = Database(database, LOG=fLOG)
    db.connect()
    StreamRSS.fill_table(db, table, res)
    db.close()
    return len(res)


def rss_download_post_to_database(database="database_rss.db3",
                                  table_blog="blogs",
                                  table_post="posts"):
    """
    download all post from a list of blogs stored in a database by function @see fn rss_from_xml_to_database

    @param      database        database file name (SQLite format)
    @param      table_blog      table name of the blogs
    @param      table_post      table name of the post
    @return                     number of posts downloaded
    """
    db = Database(database, LOG=fLOG)
    db.connect()
    rss_list = list(db.enumerate_objects(table_blog, StreamRSS))
    list_post = list(StreamRSS.enumerate_post_from_rsslist(rss_list))
    BlogPost.fill_table(db, table_post, list_post, skip_exception=True)
    db.close()

    return len(list_post)


def rss_update_run_server(dbfile, xml_blogs, port=8093, browser=None, period="today",
                          server=None, thread=False):
    """
    create a database if it does not exists, add a table for blogs and posts,
    update the database, starts a server and open a browser

    @param      dbfile      (str) sqllite database to create
    @param      xml_blogs   (str) xml description of blogs (google format) (file or string)
    @param      port        the main page will be ``http://localhost:port/``
    @param      browser     (str) to choose a different browser than the default one
    @param      period      (str) when opening the browser, it can show the results for last day or last week
    @param      server      to set up your own server
    @param      thread      to start the server in a separate thread
    @return                 see @see fn rss_run_server

    You can read the blog post `pyhome3 RSS Reader <http://www.xavierdupre.fr/blog/2013-07-28_nojs.html>`_.

    """
    rss_from_xml_to_database(xml_blogs, database=dbfile)
    rss_download_post_to_database(database=dbfile)
    return rss_run_server(dbfile, port, browser=browser, period=period, server=server, thread=thread)


def rss_run_server(dbfile, port=8093, browser=None, period="today",
                   server=None, thread=False):
    """
    starts a server and open a browser on a page reading blog posts

    @param      dbfile      (str) sqllite database to create
    @param      port        the main page will be ``http://localhost:port/``
    @param      browser     (str) to choose a different browser than the default one
    @param      period      (str) when opening the browser, it can show the results for last day or last week
    @param      server      to set up your own server
    @param      thread      to start the server in a separate thread

    You can read the blog post `RSS Reader <http://www.xavierdupre.fr/blog/2013-07-28_nojs.html>`_.

    If *browser* is "none", the browser is not started.

    """
    if not os.path.exists(dbfile):
        raise FileNotFoundError(dbfile)

    url = "http://localhost:%d/rss_reader.html?search=%s" % (port, period)
    fLOG("opening ", url)
    if browser is not None:
        if browser in ["none", "None"]:
            pass
        else:
            try:
                b = webbrowser.get(browser)
            except webbrowser.Error as e:
                if browser == "firefox" and sys.platform.startswith("win"):
                    webbrowser.register(
                        'firefox',
                        None,
                        webbrowser.GenericBrowser(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"))
                    b = webbrowser.get(browser)
                else:
                    raise e
            b.open(url)
    else:
        webbrowser.open(url)
    return RSSServer.run_server(server, dbfile, port=port, thread=thread)
