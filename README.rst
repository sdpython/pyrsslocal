.. _l-README:

README
======

.. contents::
   :depth: 3


Description
-----------

The project is hosted `here <http://www.xavierdupre.fr/site2013/index_code.html>`_ 
on github: `github/pyrsslocal <https://github.com/sdpython/pyrsslocal/>`_,
on pypi: `pypi/pyrsslocal <https://pypi.python.org/pypi/pyrsslocal/>`_.

::

    from pyquickhelper  import fLOG
    from pyrsslocal     import rss_update_run_server
    fLOG (OutputPrint = True)
    xml_blogs = "_unittests/ut_rss/data/subscriptions.xml"
    dbfile    = "rss_posts.db3"
    rss_update_run_server(dbfile, xml_blogs)

The previous example takes a dump of blogs url coming from the former Google Reader, 
downloads RSS streams, loads everything into a database (SQLlite format),
and opens a local web application to read them, mark them, or search their titles.
You can find more at `pyrsslocal <http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/index.html>`_.
The XML file which describes the blogs looks like this::

    <?xml version="1.0" encoding="UTF-8"?>
    <opml version="1.0">
        <head>
            <title>Xavier subscriptions in Google Reader</title>
        </head>
        <body>
        
            <outline title="new" text="new_">
            
                <!--
                <outline text=""
                    title="" 
                    type="rss"
                    xmlUrl="" 
                    htmlUrl=""/>
                    -->

                <outline text="XD blog" 
                         title="XD blog" 
                         type="rss"
                         xmlUrl="http://www.xavierdupre.fr/blog/xdbrss.xml" 
                         htmlUrl="http://www.xavierdupre.fr/blog/xd_blog.html" />
            </outline>
            
        </body>
    </opml>

The function updates a SQLite database, going through all blogs and collecting posts.
It then starts a Python server and shows a page with various to navigate through the posts.
The server logs every click and requested url.

