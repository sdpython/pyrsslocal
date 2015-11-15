"""
@file
@brief description of a RSS stream

.. requires feedparser

"""
import datetime

from pyquickhelper import fLOG
from ..xmlhelper.xmlfilewalk import xml_filter_iterator
from .rss_blogpost import BlogPost
from ..helper.download_helper import get_url_content_timeout


class StreamRSS:

    """

    .. requires feedparser

    description of an RSS stream

    @code
       <outline text="Freakonometrics" title="Freakonometrics"
            type="rss"
            xmlUrl="http://freakonometrics.hypotheses.org/feed"
            htmlUrl="http://freakonometrics.hypotheses.org" />
    @endcode

    @var    titleb      title of the stream
    @var    type        type
    @var    xmlUrl      url of the rss stream
    @var    htmlUrl     main page of the blog
    @var    keywordsb   list of keywords
    """

    def __init__(
            self, titleb, type, xmlUrl, htmlUrl, keywordsb, id=-1, nb=None):
        """
        constructor

        @param    titleb      title of the stream
        @param    type        type
        @param    xmlUrl      url of the rss stream
        @param    htmlUrl     main page of the blog
        @param    keywordsb   keywords
        @param    id          an id
        @param    nb          not included in the database, part of the statistics with can be added if they not None
        """
        self.titleb = titleb
        self.type = type
        self.xmlUrl = xmlUrl
        self.htmlUrl = htmlUrl
        self.keywordsb = keywordsb
        self.id = id
        self.stat = {}
        if nb is not None:
            self.stat["nb"] = nb

    def __str__(self):
        """
        usual
        """
        return "%s: %s (%s)" % (self.type, self.titleb, self.xmlUrl)

    def __lt__(self, o):
        """
        cmp operator
        """
        s1 = self.__str__().lower()
        s2 = self.__str__().lower()
        return s1 < s2

    @property
    def index(self):
        """
        defines the column to use as an index
        """
        return "xmlUrl"

    @property
    def asdict(self):
        """
        return all members as a dictionary

        @return     dictionary
        """
        return {"titleb": self.titleb,
                "type": self.type,
                "xmlUrl": self.xmlUrl,
                "htmlUrl": self.htmlUrl,
                "keywordsb": self.keywordsb}

    @staticmethod
    def schema_database_read():
        """
        return all members names and types as a dictionary

        @return     dictionary
        """
        return {0: ("titleb", str),
                1: ("type", str),
                2: ("xmlUrl", str),
                3: ("htmlUrl", str),
                4: ("keywordsb", str),
                5: ("id", int, "PRIMARYKEY", "AUTOINCREMENT")}

    @property
    def schema_database(self):
        """
        return all members names and types as a dictionary

        @return     dictionary
        """
        return {0: ("titleb", str),
                1: ("type", str),
                2: ("xmlUrl", str),
                3: ("htmlUrl", str),
                4: ("keywordsb", str),
                -1: ("id", int, "PRIMARYKEY", "AUTOINCREMENT")}

    @property
    def asrow(self):
        """
        returns all the values as a row (following the schema given by @see me schema_database)

        @return     list of values
        """
        return [self.titleb,
                self.type,
                self.xmlUrl,
                self.htmlUrl,
                ",".join(self.keywordsb)]

    @staticmethod
    def enumerate_stream_from_google_list(file, encoding="utf8"):
        """
        retrieve the list of RSS streams from a dump made with Google Reader
        @param      file        filename
        @param      encoding    encoding
        @return                 list of StreamRSS

        The format is the following:

        @example(An entry in the XML config file)
        @code
           <outline text="Freakonometrics"
                title="Freakonometrics"
                type="rss"
                xmlUrl="http://freakonometrics.hypotheses.org/feed"
                htmlUrl="http://freakonometrics.hypotheses.org" />
        @endcode
        @endexample

        """
        with open(file, "r", encoding=encoding) as ff:
            for nb_, o in enumerate(
                    xml_filter_iterator(ff,
                                        lambda f: True,
                                        log=True,
                                        xmlformat=False,
                                        fLOG=fLOG)):
                for oo in o.enumerate_on_tag("outline", recursive=True):
                    if isinstance(oo, tuple):
                        raise ValueError("wrong format file: " + file)
                    else:
                        if len(oo.other) == 0 and "xmlUrl" in oo:
                            if len(oo["xmlUrl"]) > 0:
                                obj = StreamRSS(
                                    titleb=oo["title"],
                                    type=oo["type"],
                                    xmlUrl=oo["xmlUrl"],
                                    htmlUrl=oo["htmlUrl"],
                                    keywordsb=[])
                                yield obj

    @staticmethod
    def fill_table(db, tablename, iterator_on):
        """
        fill a table of a database, if the table does not exists, it creates it

        @param      db              database object (@see cl Database)
        @param      tablename       name of a table (created if it does not exists)
        @param      iterator_on     iterator_on on StreamRSS object

        Example:
        @code
        res = list( StreamRSS.enumerate_stream_from_google_list(file) )
        StreamRSS.fill_table(db, "blogs", res)
        @endcode
        """
        db.fill_table_with_objects(
            tablename,
            iterator_on,
            check_existence=True)

    def enumerate_post(self, path=None, fLOG=fLOG):
        """
        parses a rss stream.

        @param      path    if None, use self.xmlUrl, otherwise, uses this path (url or local file)
        @param      fLOG    logging function
        @return             list of BlogPost

        We expect the format to be:
        @code
        {'summary_detail':
                {'base': '',
                 'value': '<p> J\'ai encore perdu des ... </p>',
                 'language': None,
                 'type': 'text/html'},
          'title_detail':
                {'base': '',
                'value': 'Installer pip pour Python',
                'language': None,
                'type': 'text/plain'},
           'published': '2013-06-24 00:00:00',
           'published_parsed': time.struct_time(tm_year=2013, tm_mon=6, tm_mday=24, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=175, tm_isdst=0),
           'link': 'http://www.xavierdupre.fr/blog/xd_blog.html?date=2013-06-24',
           'summary': '<p> J\'ai encore perdu de... </p>',
           'guidislink': False,
           'title': 'Installer pip pour Python',
           'links': [{'href': 'http://www.xavierdupre.fr/blog/xd_blog.html?date=2013-06-24',
                    'rel': 'alternate', 'type': 'text/html'}],
            'id': 'http://www.xavierdupre.fr/blog/xd_blog.html?date=2013-06-24'}
        @endcode

        If there is no date, the function will give the date of today (assuming you fetch posts from this blog everyday).
        If the id is not present, the guid will be the url, otherwise, it will be the id.
        """
        import feedparser
        if path is None:
            path = self.xmlUrl

        if path.startswith("http://"):
            cont = get_url_content_timeout(path)
            if cont is None:
                fLOG("unable to retrieve content for url: ", path)
        else:
            cont = path

        if cont is not None:

            if "<title>" not in cont:
                fLOG("unable to parse content from " + self.xmlUrl)

            d = feedparser.parse(cont)
            if len(d["entries"]) == 0:
                fLOG("*** no post for ", path)

            for post in d["entries"]:
                titleb = post.get("title", "-")
                url = post.get("link", "")

                try:
                    id = post["id"]
                    guid = url if post["guidislink"] else id
                except KeyError:
                    id = url
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

                bl = BlogPost(self, titleb, guid, isPermaLink, url, desc, date)
                yield bl

    @staticmethod
    def enumerate_post_from_rsslist(list_rss_stream, fLOG=fLOG):
        """
        enumerate all posts found in all rss_streams given as a list

        @param      list_rss_stream     list of rss streams
        @param      fLOG                logging function
        @return                         enumeration of blog post
        """
        for rss in list_rss_stream:
            try:
                fLOG("reading post from", rss)
            except UnicodeEncodeError:
                fLOG("reading post from", [rss], "encoding issue")
            for post in rss.enumerate_post():
                yield post

    @property
    def stat_nb(self):
        """
        return the statistics nb:  ``self.stat.get("nb", 0)``
        @return         number
        """
        return self.stat.get("nb", 0)

    templates = {"default": """
                        <p class="%s"><a href="%s" onmousedown="sendlog('blog/{0.id}/in')">{0.titleb}</a>
                        <a href="{0.htmlUrl}" target="_blank" onmousedown="sendlog('blog/{0.id}/outimg')">
                        <img src="/arrowi.png" width="12px" /></a></p>
                        """.replace("                        ", ""),
                 "default_stat": """
                        <tr class="%s"><td>
                        <a href="%s" onmousedown="sendlog('blog/{0.id}/in')">{0.titleb}</a>
                        <a href="{0.htmlUrl}" target="_blank" onmousedown="sendlog('blog/{0.id}/outimg')">
                        <img src="/arrowi.png" width="12px" /></a>
                        </td><td>{0.stat_nb}</td></tr>
                        """.replace("                        ", ""),
                 }

    def html(self, template=None,
             action="{0.htmlUrl}",
             style="blogtitle",
             addlog=True):
        """
        display the blogs in HTML format, the template contains two kinds of informations:
        - {0.member}: this string will be replaced by the member

        @param      template        html template, if not None, it can equal to another default template:
                                        - default
                                        - default_stat
        @param      action          url to use when clicking on a blog
        @param      style           style of the paragraph containing the url
        @param      addlog          if True, url will be prefix by ``/logs/click/`` in order to be logged
        @return                     html string

        If the template is None, it will be replaced a default value (see the code and the variable ``template``).

        """
        if template is None:
            template = StreamRSS.templates["default"] % (style, action)
        else:
            template = StreamRSS.templates.get(
                template,
                template) % (style,
                             action)

        template = template.replace("__id__", str(self.id))
        res = template.format(self)
        return res
