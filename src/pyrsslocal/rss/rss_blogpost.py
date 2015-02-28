"""
@file
@brief description of a blog post
"""
import datetime
import urllib

from pyquickhelper.loghelper.convert_helper import str_to_datetime


class BlogPost:

    """
    a blog post

    @code
        <item>
            <title>Raw food</title>
            <link>http://www.xavierdupre.fr/blog/xd_blog.html?date=2013-06-30</link>
            <guid isPermaLink="true">http://www.xavierdupre.fr/blog/xd_blog.html?date=2013-06-30</guid>
            <description>&lt;p&gt; J'ecoutais une em....</description>
            <pubDate>2013-06-30 00:00:00</pubDate>
        </item>
    @endcode

    @var    id_rss          id of the blog source
    @var    title           title of the stream
    @var    guid            guid
    @var    isPermaLink     isPermaLink
    @var    link            url of the blog post
    @var    description     description
    @var    pubDate         pubDate
    @var    keywords        list of keywords
    @var    status          status (dictionary with variables)
    """

    def __init__(self, id_rss,
                 title,
                 guid,
                 isPermaLink,
                 link,
                 description,
                 pubDate,
                 keywords=[],
                 id=-1):
        """
        constructor

        @param    id_rss          id of rss or @see cl Stream class
        @param    title           title of the stream
        @param    guid            guid
        @param    isPermaLink     isPermaLink
        @param    link            url of the blog post
        @param    description     description
        @param    pubDate         pubDate
        @param    keywords        keywords
        """
        self.id_rss = id_rss
        self.title = title
        self.guid = guid
        self.isPermaLink = isPermaLink
        self.link = link
        self.description = description
        self.pubDate = pubDate
        self.keywords = keywords
        self.id = id
        self.status = None
        self.statusList = [
            "jokes",
            "programming",
            "data",
            "reject",
            "read",
            "keep",
            "interesting",
            "teachings",
            "work"]

        if self.id_rss is None:
            raise Exception("no source (StreamRSS) for this post")
        if isinstance(self.id_rss, int):
            if self.id_rss == -1:
                raise ValueError(
                    "the source id (self.id_rss) is equal to -1, not allowed")
        elif self.id_rss.id == -1:
            raise ValueError(
                "the source id (self.id_rss.id) is equal to -1, not allowed")

        if isinstance(self.pubDate, str):
            self.pubDate = str_to_datetime(self.pubDate)

    def add_status(self, status):
        """
        attach a dictionary representing the status

        @param      status      dictionary
        """
        self.status = status

    def __str__(self):
        """
        usual
        """
        return "%s: %s (from %s)" % (
            str(self.pubDate), self.title, self.id_rss)

    @property
    def index(self):
        """
        defines the column to use as an index
        """
        return "guid"

    @property
    def indexes(self):
        """
        defines other indexes to create
        """
        return ["id_rss"]

    @property
    def asdict(self):
        """
        return all members as a dictionary

        @return     dictionary
        """
        return {"id_rss": self.id_rss,
                "title": self.title,
                "guid": self.guid,
                "isPermaLink": self.isPermaLink,
                "link": self.link,
                "description": self.description,
                "pubDate": self.pubDate,
                "keywords": self.keywords,
                }

    @staticmethod
    def schema_database_read():
        """
        return all members names and types as a dictionary

        @return     dictionary
        """
        return {0: ("id_rss", int),
                1: ("pubDate", datetime.datetime),
                2: ("title", str),
                3: ("guid", str),
                4: ("isPermaLink", int),
                5: ("link", str),
                6: ("description", str),
                7: ("keywords", str),
                8: ("id", int, "PRIMARYKEY", "AUTOINCREMENT")}

    @property
    def schema_database(self):
        """
        return all members names and types as a dictionary

        @return     dictionary
        """
        return {0: ("id_rss", int),
                1: ("pubDate", datetime.datetime),
                2: ("title", str),
                3: ("guid", str),
                4: ("isPermaLink", int),
                5: ("link", str),
                6: ("description", str),
                7: ("keywords", str),
                -1: ("id", int, "PRIMARYKEY", "AUTOINCREMENT")}

    @property
    def asrow(self):
        """
        returns all the values as a row (following the schema given by @see me schema_database)

        @return     list of values
        """
        return [self.id_rss if isinstance(self.id_rss, int) else self.id_rss.id,
                self.pubDate,
                self.title,
                self.guid,
                1 if self.isPermaLink else 0,
                self.link,
                self.description.replace("\r", "").replace("\n", " "),
                ",".join(self.keywords)]

    @staticmethod
    def fill_table(db, tablename, iterator_on, skip_exception=False):
        """
        fill a table of a database, if the table does not exists, it creates it

        @param      db              database object (@see cl Database)
        @param      tablename       name of a table (created if it does not exists)
        @param      iterator_on     iterator_on on StreamRSS object
        @param      skip_exception  skip exception while inserting an element
        """
        db.fill_table_with_objects(tablename,
                                   iterator_on,
                                   check_existence=True,
                                   skip_exception=skip_exception)

    @property
    def pubDateformat(self):
        """
        returns the date to a given format
        """
        return self.pubDate.strftime(self._ftime)

    @property
    def Status(self):
        """
        return the status
        """
        return self.status.get("status", "") if self.status is not None else ""

    @property
    def StatusTime(self):
        """
        return the status
        """
        return self.status.get("dtime", "") if self.status is not None else ""

    @property
    def StatusTimeStr(self):
        """
        return the status
        """
        return str(self.StatusTime).split()[0]

    def get_html_status(self, thispage):
        """
        returns a status written in HTML

        @param      thispage        the displayed page
        @return                     html string
        """
        all = []
        for k in self.statusList:
            if self.status is not None and "status" in self.status and self.status[
                    "status"] == k:
                style = "poststatusextbyes"
            else:
                style = "poststatusextbno"
            code = """<a class="%s" href="%s" onmousedown="sendlog('status/{0.id}/%s')">%s</a>""" % (
                style, thispage, k, k)
            all.append(code)
        return "\n".join(all)

    template = """
                            <p class="%s">{0.pubDateformat}<a href="%s" onmousedown="sendlog('post/{0.id}/in')">{0.title}</a>
                            <a href="{0.link}" target="_blank" onmousedown="sendlog('post/{0.id}/outimg')">
                            <img src="/arrowi.png" width="12px" /></a></p>
                            """.replace("                            ", "")

    templateext = """
                            <p class="%s"><a href="{0.id_rss.htmlUrl}" target="_blank" onmousedown="sendlog('blog/{0.id_rss.id}/out')">{0.id_rss.titleb}</a></p>
                            <p class="%s"><b>{0.pubDateformat} </b>
                            <a href="%s" target="_blank" onmousedown="sendlog('post/{0.id}/out')">{0.title}</a></p>
                            <p class="%s">{0.description}</p>
                            <hr />
                            """.replace("                            ", "")

    templateextst = """
                            <p class="%s"><a href="{0.id_rss.htmlUrl}" target="_blank" onmousedown="sendlog('blog/{0.id_rss.id}/out')">{0.id_rss.titleb}</a></p>
                            <p class="%s"><b>{0.pubDateformat} </b>
                            <a href="%s" target="_blank" onmousedown="sendlog('post/{0.id}/out')">{0.title}</a></p>
                            <p class="%s">{0.description}</p>
                            <p class="%s">%s</p>
                            <hr />
                            """.replace("                            ", "")

    templateShort = """
                            <tr><td class="%s">{0.StatusTimeStr}</td><td class="%s">{0.Status}</td><td class="%s">{0.pubDateformat}<a href="%s" onmousedown="sendlog('post/{0.id}/in')">{0.title}</a>
                            <a href="{0.link}" target="_blank" onmousedown="sendlog('post/{0.id}/outimg')">
                            <img src="/arrowi.png" width="12px" /></a></td></tr>
                            """.replace("                            ", "")

    templateTable = """
                            <tr><td class="%s">{0.pubDateformat}<a href="%s" onmousedown="sendlog('post/{0.id}/in')">{0.title}</a>
                            <a href="{0.link}" target="_blank" onmousedown="sendlog('post/{0.id}/outimg')">
                            <img src="/arrowi.png" width="12px" /></a></td></tr>
                            """.replace("                            ", "")

    def html(self, template=None,
             action="{0.link}",
             style=None,
             styleblog=None,
             stylestatus=None,
             ftime="%Y-%m-%d",
             extended=False,
             style_desc="description",
             addlog=True,
             addcontent=False,
             addstatus=False,
             thispage=None):
        """
        display the blogs in HTML format, the template contains two kinds of informations:
        - {0.member} : this string will be replaced by the member

        @param      template        html template
        @param      action          url to use when clicking on a blog
        @param      style           style of the paragraph containing the url, if None,
                                    it will be set to ``postitle`` or ``posttitleext``
        @param      styleblog       style of the paragraph containing the url, if None,
                                    it will be set to ``posttitleexb``
        @param      ftime           format time
        @param      extended        if True, display the title,
                                    if False, display everything
        @param      style_desc      style for the description
        @param      addlog          if True, ``link`` will contains a prefix to go through the server and be logged
        @param      addcontent      if True, the function will add some javascript code to make the content from the website appear.
        @param      addstatus       if True, add the status for this blog post
        @return                     html string

        If the template is None, it will be replaced a default value (see the code and the variable ``template``).

        """
        if template is None:
            if not extended:
                if style is None:
                    style = "posttitle"
                template = BlogPost.template % (style, action)
            else:
                if style is None:
                    style = "posttitleext"
                if styleblog is None:
                    styleblog = "posttitleextb"
                if stylestatus is None:
                    stylestatus = "poststatusextb"
                if addstatus:
                    template = BlogPost.templateextst % (
                        styleblog, style, action, style_desc, stylestatus, self.get_html_status(thispage))
                else:
                    template = BlogPost.templateext % (
                        styleblog, style, action, style_desc)
        elif template == "status":
            template = BlogPost.templateShort % (
                "posttitleext", "posttitleext", "posttitleextb", action)
        elif template == "table":
            template = BlogPost.templateTable % ("posttitleextb", action)
        elif not isinstance(template, str):
            raise Exception("expecting a format as a string")

        self._ftime = ftime  # for a property
        res = template.format(self)

        if addcontent:
            res += """
                <div id="cont%d">
                <p>waiting...</p>
                </div>
                <script type="text/javascript">
                try
                {
                    loadDoc('%s', 'cont%d', false, '%s');
                }
                catch (err)
                {
                    document.write ("<p>loading error</p>") ;
                }
                </script>
                """ % (self.id, self.link, self.id, self.title)

        return res
