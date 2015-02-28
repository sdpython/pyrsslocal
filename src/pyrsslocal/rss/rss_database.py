"""
@file
@brief description of a RSS stream
"""
import datetime
import os

from pyensae.sql.database_main import Database
from .rss_blogpost import BlogPost
from .rss_stream import StreamRSS


class DatabaseRSS (Database):

    """
    database specific to RSS

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

    def __init__(self, dbfile,
                 table_blogs="blogs",
                 table_posts="posts",
                 table_stats="posts_stat",
                 table_event="events",
                 LOG=print):
        """
        constructor

        @param    dbfile        file database
        @param    table_blogs   table name for the blogs
        @param    table_posts   table name for the posts
        @param    table_stats   table name for the posts stats
        @param    table_event   table name for the events
        @param    LOG           logging function
        """
        if not os.path.exists(dbfile):
            raise FileNotFoundError(dbfile)
        Database.__init__(self, dbfile, LOG=LOG)
        self.dbfile = dbfile
        self.table_blogs = table_blogs
        self.table_posts = table_posts
        self.table_stats = table_stats
        self.table_event = table_event
        self.connect()
        for tbl in [table_blogs, table_posts]:
            if not self.has_table(tbl):
                raise Exception("table %s not found in %s" % (tbl, dbfile))

        self.create_missing_table()
        self.close()

    def create_missing_table(self):
        """
        creates the missing tables
        """

        if self.has_table(self.table_stats) and len(self.get_table_columns(
                self.table_stats)) != len(DatabaseRSS.schema_table("stats")):
            self.remove_table(self.table_stats)

        if not self.has_table(self.table_stats):
            schema = DatabaseRSS.schema_table("stats")
            self.create_table(self.table_stats, schema)
            self.commit()
            self.create_index(
                "id_post_" +
                self.table_stats,
                self.table_stats,
                "id_post",
                False)
            self.commit()

        if not self.has_table(self.table_event):
            schema = DatabaseRSS.schema_table("event")
            self.create_table(self.table_event, schema)
            self.commit()

    def __str__(self):
        """
        usual
        """
        return "file:%s, t-blogs:%s, t-posts:%s" % (
            self.dbfile, self.table_blogs, self.table_posts)

    specific_search = {
        "today": "SELECT DISTINCT id_rss FROM {0} WHERE pubDate >= '{1}'",
        "twoday": "SELECT DISTINCT id_rss FROM {0} WHERE pubDate >= '{2}'",
        "week": "SELECT DISTINCT id_rss FROM {0} WHERE pubDate >= '{3}'",
        "frequent":  """SELECT id_rss FROM (
                                SELECT id_rss, SUM(nb)*1.0/ (MAX(day) - MIN(day)+1) AS avg_nb FROM (
                                    SELECT id_rss, day, COUNT(*) AS nb FROM (
                                        SELECT id_rss, getdayn(pubDate) AS day FROM {0} WHERE pubDate >= '{4}'
                                    ) GROUP BY id_rss, day
                                ) GROUP BY id_rss
                            ) WHERE avg_nb >= {5}""",
        "notfrequent":  """SELECT id_rss FROM (
                                SELECT id_rss, SUM(nb)*1.0/ (MAX(day) - MIN(day)+1) AS avg_nb FROM (
                                    SELECT id_rss, day, COUNT(*) AS nb FROM (
                                        SELECT id_rss, getdayn(pubDate) AS day FROM {0} WHERE pubDate >= '{4}'
                                    ) GROUP BY id_rss, day
                                ) GROUP BY id_rss
                            ) WHERE avg_nb < {5}""",
    }

    @staticmethod
    def getday(dt):
        """
        return the same datetime but with no time

        @param  dt      datetime
        @return         datetime which correspond to the beginning of the day
        """
        if isinstance(dt, str):
            res = dt.split(" ")
            return res[0]
        else:
            res = datetime.datetime(dt.year, dt.month, dt.day)
            return res

    @staticmethod
    def getdayn(dt):
        """
        return the same datetime but with no time

        @param  dt      datetime
        @return         datetime which correspond to the beginning of the day
        """
        if isinstance(dt, str):
            dt = dt.split()[0]
            ymd = dt.split("-")
            res = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]))
        else:
            res = datetime.datetime(dt.year, dt.month, dt.day)
        one = datetime.datetime(2000, 1, 1)
        d = res - one
        return d.days

    def enumerate_blogs(self, sorted=True,
                        specific=None,
                        daily_freq=1.5,
                        now=None,
                        addstat=False):
        """
        enumerates all the blogs from the database

        @param      sorted      sorted by title
        @param      specific    specific search
                                    - None: all blogs
                                    - today: get all blogs for today
                                    - twoday: get all blogs for today and yesterday
                                    - week: get all blogs for last week
                                    - notfrequent: get all blogs publishing less posts in a day than ``daily_freq``
                                    - frequent: get all blogs publishing more posts in a day than ``daily_freq``
        @param      daily_freq  see parameter specific
        @param      now         if None, today means today, if not None, ``now`` will have the meaning of today
        @param      addstat     if True, the function will a field corresponding to the number of posts from this blog
        @return                 enumeration of @see cl StreamRSS
        """
        if addstat:
            sqlstatjoinA = "SELECT A.*, nbpost FROM ("
            sqlstatjoinB = """) AS A INNER JOIN (SELECT id_rss, COUNT(*) AS nbpost FROM {0}
                                GROUP BY id_rss) ON id_rss == A.id""".format(self.table_posts)
            orderby = "nbpost DESC"
        else:
            sqlstatjoinA = ""
            sqlstatjoinB = ""
            orderby = "titleb"

        if isinstance(specific, list):
            if len(specific) == 1:
                specific = specific[0]
            else:
                raise TypeError(
                    "unable to process if specific is a list:" +
                    str(specific))

        if specific in [None, ""]:
            self.connect()
            sql = "%sSELECT titleb, type, xmlUrl, htmlUrl, keywordsb, id FROM %s%s" % (
                sqlstatjoinA, self.table_blogs, sqlstatjoinB)
            if sorted:
                sql += " ORDER BY " + orderby
            for row in self.execute(sql):
                bl = StreamRSS(*row)
                yield bl
            self.close()

        elif specific in DatabaseRSS.specific_search.keys():

            today = datetime.datetime.now() if now is None else now
            day = datetime.datetime(2013, 1, 2) - datetime.datetime(2013, 1, 1)
            yesday = today - day
            yes2 = yesday - day
            yesweek = today - (day * 7)
            yeshalf = today - (day * 180)
            self.connect()
            self.add_function("getdayn", 1, DatabaseRSS.getdayn)

            sql = "%sSELECT titleb, type, xmlUrl, htmlUrl, keywordsb, id FROM %s WHERE id IN (%s)%s" % \
                (sqlstatjoinA, self.table_blogs,
                 DatabaseRSS.specific_search[specific].format(
                     self.table_posts,
                     yesday,
                     yes2,
                     yesweek,
                     yeshalf,
                     daily_freq),
                    sqlstatjoinB)
            if sorted:
                sql += " ORDER BY " + orderby

            for row in self.execute(sql):
                bl = StreamRSS(*row)
                yield bl
            self.close()
        else:
            raise ValueError(
                "unable to interpret value %s for parameter specific" %
                specific)

    def enumerate_latest_status(self, postid, nb=1, connect=True):
        """
        retrieves the latest status for a post

        @param      postid      post id
        @param      nb          number of desired status
        @param      connect     connect (True) or skip connection (False)
        @return                 enumerate on values from ``table_stats`` ordered by decreasing time
        """
        if connect:
            self.connect()
        sch = DatabaseRSS.schema_table("stats")
        sql = "SELECT * FROM {0} WHERE id_post=={1} ORDER BY dtime DESC".format(
            self.table_stats,
            postid)
        for row in self.execute(sql):
            nb -= 1
            if nb < 0:
                break
            yield {sch[i][0]: row[i] for i in range(len(row))}
        if connect:
            self.close()

    def private_process_condition(self,
                                  blog_selection=[],
                                  post_selection=[],
                                  sorted=True,
                                  specific=None,
                                  now=None,
                                  searchterm=None
                                  ):
        """
        returns a SQL query corresponding to list of posts

        @param      blog_selection      list of blogs to consider (or empty for all)
        @param      post_selection      list of posts to consider
        @param      sorted              sorted by date
        @param      specific            specific search
                                            - None: all posts
                                            - today: get all posts for today
                                            - week: get all posts for last week
        @param      searchterm          if not None, filters using a SQL like search (using ``%``)
        @param      now                 if None, today means today, if not None, ``now`` will have the meaning of today
        @return                         SQL query
        """
        if searchterm is not None:
            if not searchterm.startswith("+") and "%" not in searchterm:
                searchterm = "%{0}%".format(searchterm)
            searchterm = searchterm.replace("'", "\\'").replace('"', '\\"')
            where = "WHERE UPPER(title) LIKE '{0}'".format(searchterm.upper())
        else:
            where = ""

        sql = """SELECT id_rss, title, guid, isPermaLink, link, description, pubDate, keywords, {0}.id AS id,
                        titleb, type, xmlUrl, htmlUrl, keywordsb, {1}.id AS idblog
                 FROM {0}
                 INNER JOIN {1}
                 ON {0}.id_rss == {1}.id
                 {2}
                 """.format(self.table_posts, self.table_blogs, where)

        cond = []
        if len(blog_selection) > 0:
            condition = ",".join(map(str, blog_selection))
            cond.append(" id_rss in (%s)" % condition)
        if len(post_selection) > 0:
            condition = ",".join(map(str, post_selection))
            cond.append("%s.id in (%s)" % (self.table_posts, condition))
        if specific in ["today", "week", "twoday"]:
            today = datetime.datetime.now() if now is None else now
            day = datetime.datetime(2013, 1, 2) - datetime.datetime(2013, 1, 1)
            dec = {"week": 7, "today": 1, "twoday": 2}.get(specific, 7)
            mdat = today - day * dec
            st = "pubDate >= '{0}'".format(mdat)
            cond.append(st)

        if len(cond) > 0:
            sql += " WHERE " + " AND ".join(cond)

        if sorted:
            sql += " ORDER BY pubDate DESC"
        return sql

    def enumerate_posts(self,
                        blog_selection=[],
                        post_selection=[],
                        sorted=True,
                        first=1000,
                        specific=None,
                        daily_freq=1.5,
                        now=None,
                        addstatus=False,
                        searchterm=None
                        ):
        """
        enumerates all the posts from the database if the blog id
        belongs to a selection (or all if blog_selection is empty)

        @param      blog_selection      list of blogs to consider (or empty for all)
        @param      post_selection      list of posts to consider
        @param      sorted              sorted by date
        @param      first               we only consider the first ``first``
        @param      specific            specific search
                                            - None: all posts
                                            - today: get all posts for today
                                            - week: get all posts for last week
        @param      daily_freq          see parameter specific
        @param      now                 if None, today means today, if not None, ``now`` will have the meaning of today
        @param      addstatus           if True, fetches the status of a blog
        @param      searchterm          if not None, filters using a SQL like search (using ``%``)
        @return                         enumeration of @see cl BlogPost
        """
        self.connect()
        sql = self.private_process_condition(
            blog_selection,
            post_selection,
            sorted,
            specific,
            now,
            searchterm)
        sql += " LIMIT %d" % first

        for row in self.execute(sql):
            row = list(row)
            row[-2] = row[-2].split(",")
            row[3] = row[3] == 1
            blog = StreamRSS(* (row[-6:]))
            row = row[:-6]
            row[0] = blog

            bl = BlogPost(*row)

            if addstatus:
                for st in self.enumerate_latest_status(bl.id, connect=False):
                    bl.add_status(st)
            yield bl
        self.close()

    def enumerate_posts_status(self,
                               blog_selection=[],
                               post_selection=[],
                               sorted=True,
                               specific=None,
                               now=None,
                               searchterm=None
                               ):
        """
        enumerate status

        @param      blog_selection      list of blogs to consider (or empty for all)
        @param      post_selection      list of posts to consider
        @param      sorted              sorted by date
        @param      specific            specific search
                                            - None: all posts
                                            - today: get all posts for today
                                            - week: get all posts for last week
        @param      now                 if None, today means today, if not None, ``now`` will have the meaning of today
        @param      searchterm          if not None, filters using a SQL like search (using ``%``)
        @return                         enumerate on values from ``table_stats`` ordered by decreasing time
        """
        self.connect()

        sql_po = self.private_process_condition(
            blog_selection,
            post_selection,
            sorted,
            specific,
            now,
            searchterm)

        sql_st = """SELECT A.id_post, status, A.dtime FROM (
                    SELECT id_post, MAX(dtime) AS dtime FROM {0}
                    GROUP BY id_post) AS A
                    INNER JOIN {0}
                    ON A.id_post == {0}.id_post""".format(self.table_stats)

        sql = """SELECT DISTINCT id_rss, title, guid, isPermaLink, link, description, pubDate, keywords, id,
                        titleb, type, xmlUrl, htmlUrl, keywordsb, idblog, status, dtime
                    FROM (
                        {0}
                    )
                    AS tA
                    INNER JOIN (
                        {1}
                    ) AS tB
                    ON tA.id == tB.id_post""". format(sql_po, sql_st)

        for row in self.execute(sql):
            row = list(row)
            row[-4] = row[-4].split(",")
            row[3] = row[3] == 1
            blog = StreamRSS(* (row[-8:-2]))
            st = {"status": row[-2], "dtime": row[-1]}
            row = row[:-8]
            row[0] = blog

            bl = BlogPost(*row)
            bl.add_status(st)
            yield bl

        self.close()
