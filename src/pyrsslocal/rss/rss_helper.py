"""
@file
@brief Various function to automate the collection of blog posts.
"""
import os
import webbrowser
import sys
import threading
import datetime
from textwrap import dedent
from jinja2 import Template
from pyquickhelper.filehelper import read_content_ufs
from pyensae.sql.database_main import Database
from .rss_stream import StreamRSS
from .rss_blogpost import BlogPost
from .rss_simple_server import RSSServer


def rss_from_xml_to_database(file, database="database_rss.db3",
                             table="blogs", fLOG=None):
    """
    Parses a list of blogs stored in a :epkg:`XML`
    file using Google Reader format,
    stores the results in a :epkg:`SQLite` database.

    @param  file            (str) xml file containing the list of blogs, example:
    @param  database        database file (sqlite)
    @param  table           table name
    @param  fLOG            logging function
    @return                 number of stored blogs

    The XML file should contain the following:

    ::

        <outline text="XD blog"
                title="XD blog" type="rss"
                xmlUrl="http://www.xavierdupre.fr/blog/xdbrss.xml"
                htmlUrl="http://www.xavierdupre.fr/blog/xd_blog.html" />

    The function does not check whether or not the blogs were
    already added to the database,
    they will be added a second time. If the table
    does not exist, it will be created.
    """
    res = list(StreamRSS.enumerate_stream_from_google_list(file))
    db = Database(database, LOG=fLOG)
    db.connect()
    StreamRSS.fill_table(db, table, res)
    db.close()
    return len(res)


def rss_download_post_to_database(database="database_rss.db3",
                                  table_blog="blogs",
                                  table_post="posts",
                                  fLOG=None):
    """
    Downloads all posts from a list of blogs stored
    in a database by function @see fn rss_from_xml_to_database.

    @param      database        database file name (SQLite format)
    @param      table_blog      table name of the blogs
    @param      table_post      table name of the post
    @param      fLOG            logging function
    @return                     number of posts downloaded
    """
    db = Database(database, LOG=fLOG)
    db.connect()
    rss_list = list(db.enumerate_objects(table_blog, StreamRSS))
    list_post = list(
        StreamRSS.enumerate_post_from_rsslist(rss_list, fLOG=fLOG))
    BlogPost.fill_table(db, table_post, list_post, skip_exception=True)
    db.close()

    return len(list_post)


def rss_update_run_server(dbfile, xml_blogs, port=8093, browser=None, period="today",
                          server=None, thread=False, fLOG=None):
    """
    Creates a database if it does not exists,
    add a table for blogs and posts,
    update the database, starts a server and
    open a browser.

    @param      dbfile      (str) sqllite database to create
    @param      xml_blogs   (str) xml description of blogs (google format) (file or string)
    @param      port        the main page will be ``http://localhost:port/``
    @param      browser     (str) to choose a different browser than the default one
    @param      period      (str) when opening the browser, it can show the results for last day or last week
    @param      server      to set up your own server
    @param      thread      to start the server in a separate thread
    @param      fLOG        logging function
    @return                 see @see fn rss_run_server

    You can read the blog post `pyhome3 RSS Reader
    <http://www.xavierdupre.fr/blog/2013-07-28_nojs.html>`_.
    """
    rss_from_xml_to_database(xml_blogs, database=dbfile, fLOG=fLOG)
    rss_download_post_to_database(database=dbfile, fLOG=fLOG)
    return rss_run_server(dbfile, port, browser=browser, period=period, server=server, thread=thread, fLOG=fLOG)


def rss_run_server(dbfile, port=8093, browser=None, period="today",
                   server=None, thread=False, fLOG=None):
    """
    Starts a server and open a browser on a page reading blog posts.

    @param      dbfile      (str) sqllite database to create
    @param      port        the main page will be ``http://localhost:port/``
    @param      browser     (str) to choose a different browser than the default one
    @param      period      (str) when opening the browser, it can show the results for last day or last week
    @param      server      to set up your own server
    @param      thread      to start the server in a separate thread
    @param      fLOG        logging function

    You can read the blog post `RSS Reader
    <http://www.xavierdupre.fr/blog/2013-07-28_nojs.html>`_.

    If *browser* is "none", the browser is not started.
    """
    if not os.path.exists(dbfile):
        raise FileNotFoundError(dbfile)

    def open_browser():
        url = "http://localhost:%d/rss_reader.html?search=%s" % (port, period)
        if fLOG:
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

    # webbrowser.open does get back until the browser is closed if the browser was launched
    # with this only tab. If a new tab was create this function quickly endss
    th = threading.Thread(target=open_browser)
    th.start()
    ret = RSSServer.run_server(
        server, dbfile, port=port, thread=thread, fLOG=fLOG)
    # we should close the thread here if it is still alive
    return ret


def enumerate_post_from_rss(content, rss_stream=None):
    """
    Parses a :epkg:`RSS` stream.

    @param      content :epkg:`RSS` content
    @return             list of @see cl BlogPost
    """
    import feedparser  # pylint: disable=C0415
    d = feedparser.parse(content)

    if d is not None:
        for post in d["entries"]:
            titleb = post.get("title", "-")
            url = post.get("link", "")

            try:
                id_ = post["id"]
                guid = url if post["guidislink"] else id_
            except KeyError:
                id_ = url
                guid = url

            try:
                desc = post["summary_detail"]["value"]
            except KeyError:
                try:
                    desc = post["summary"]
                except KeyError:
                    desc = ""

            isPermaLink = True

            try:
                structTime = post["published_parsed"]
                date = datetime.datetime(*structTime[:6])
            except KeyError:
                try:
                    structTime = post["updated_parsed"]
                    date = datetime.datetime(*structTime[:6])
                except KeyError:
                    date = datetime.datetime.now()
            except TypeError as e:
                structTime = post["published_parsed"]
                if structTime is None:
                    date = datetime.datetime.now()
                else:
                    raise e

            if date > datetime.datetime.now():
                date = datetime.datetime.now()

            bl = BlogPost(rss_stream, titleb, guid,
                          isPermaLink, url, desc, date)
            yield bl


def enumerate_rss_merge(rss_urls, title="compilation"):
    """
    Merges many :epkg:`rss` file or url.

    @param      rss_urls        :epkg:`rss` files or urls
    @param      title           title
    @return                     new RSS
    """
    sts = StreamRSS(title, None, None, None, None, id=0)
    for name in rss_urls:
        content = read_content_ufs(name, min_size=5000)
        for blog in enumerate_post_from_rss(content, rss_stream=sts):
            yield blog


def to_rss(obj, link, description):
    """
    Converts something into :epkg:`RSS`.

    @param      obj             object
    @param      link            link
    @param      description     description
    @return                     content
    """
    if isinstance(obj, list):
        if len(obj) == 0:
            raise ValueError("obj cannot be empty.")
    else:
        raise TypeError("Unexpected type {}.".format(type(obj)))

    if isinstance(obj[0], StreamRSS):
        st = obj[0]
        title = st.title
    else:
        title = ""

    items = []
    for blog in obj:
        items.append(blog.to_rss_item())

    template = dedent("""
    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0">
    <channel>
    <title>{{title}}</title>
    <link>{{link}}</link>
    <description>{{description}}</description>
    {{items}}
    </channel>
    </rss>
    """)
    tpl = Template(template)
    return tpl.render(link=link, description=description,
                      items='\n'.join(items),
                      title=title)


template_html = """
<?xml version="1.0" encoding="utf-8"?>
<html>
<head>
<link href="http://www.xavierdupre.fr/pyhome3.ico" rel="shortcut icon"/>
<link href="http://www.xavierdupre.fr/blog/pMenu.css" rel="stylesheet" type="text/css"/>
<link REL="stylesheet" TYPE="text/css" href="http://www.xavierdupre.fr/blog/javascript/run_prettify.css"/>
<title>{{title}}</title>
<meta content="{{author}}" name="author"/>
<meta content="{{keywords}}" name="keywords"/>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<script src="http://www.xavierdupre.fr/blog/javascript/pMenu.js" type="text/javascript"></script>
<script src="http://www.xavierdupre.fr/blog/javascript/latexit.js" type="text/javascript"></script>
<script src="http://www.xavierdupre.fr/blog/javascript/run_prettify.js" type="text/javascript"></script>
<link href="http://www.xavierdupre.fr/blog/javascript/shCore.css" rel="stylesheet" type="text/css"/>
<link href="http://www.xavierdupre.fr/blog/javascript/shThemeDefault.css" rel="stylesheet" type="text/css"/>
<script src="http://www.xavierdupre.fr/blog/javascript/shCore.js" type="text/javascript"></script>
<script src="http://www.xavierdupre.fr/blog/javascript/shAutoloader.js" type="text/javascript"></script>
</head>

<body>

<div class="otherlayer">
<!-- other layer -->
</div>

<div class="sidebar">
</div>

<div class="maintitle">
<h1>{{title}}</h1>
<p><a href="{{rssfile.xml}}"><img src="http://www.xavierdupre.fr/blog/documents/feed-icon-16x16.png"/></a>
<i>{{header}}</i></p>

</div>

<div class="mainbody">

<hr />

{{items}}

<hr />

</div>
<script type="text/javascript">
SyntaxHighlighter.autoloader(
  'js jscript javascript http://www.xavierdupre.fr/blog/javascript/shBrushJScript.js',
  'py python http://www.xavierdupre.fr/blog/javascript/shBrushPython.js',
  'cpp http://www.xavierdupre.fr/blog/javascript/shBrushCpp.js',
  'sql http://www.xavierdupre.fr/blog/javascript/shBrushSql.js',
  'flat plain http://www.xavierdupre.fr/blog/javascript/shBrushPlain.js',
  'vba vb http://www.xavierdupre.fr/blog/javascript/shBrushVb.js',
  'bash http://www.xavierdupre.fr/blog/javascript/shBrushBash.js',
  'cs http://www.xavierdupre.fr/blog/javascript/shBrushCSharp.js',
  'php http://www.xavierdupre.fr/blog/javascript/shBrushPhp.js',
  'css http://www.xavierdupre.fr/blog/javascript/shBrushCss.js',
  'xml html http://www.xavierdupre.fr/blog/javascript/shBrushXml.js'
);
SyntaxHighlighter.all();
</script>
<div id="playscript"/>

</body>
</html>
"""


def to_html(items, template=None, title="BLOG",
            author="AUTHOR", keywords="blog,python",
            header="", rssfile="rssfile.xml",
            **context):
    """
    Produces a :epkg:`HTML`.

    @param      items       list of blog post
    @param      template    template or None to get the default one
    @param      title       blog title
    @param      author      author
    @param      keywords    keywords
    @param      header      blog description
    @param      rssfile     file RSS
    @param      context     other information
    @return                 pages
    """
    if template is None:
        template_ = Template(template_html)

    hitems = "\n".join(map(lambda b: b.to_html_item(),
                           sorted(items, reverse=True,
                                  key=lambda i: i.pubDate)))
    return template_.render(title=title, author=author, keywords=keywords,
                            items=hitems, header=header, rssfile=rssfile,
                            **context)
