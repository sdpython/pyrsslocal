
.. image:: https://github.com/sdpython/pyrsslocal/blob/master/_doc/sphinxdoc/source/phdoc_static/project_ico.png?raw=true
    :target: https://github.com/sdpython/pyrsslocal/

.. _l-README:

pyrsslocal: local RSS reader
============================

.. image:: https://travis-ci.com/sdpython/pyrsslocal.svg?branch=master
    :target: https://app.travis-ci.com/github/sdpython/pyrsslocal
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/0cc1qtlccq8k7hdx?svg=true
    :target: https://ci.appveyor.com/project/sdpython/pyrsslocal
    :alt: Build Status Windows

.. image:: https://circleci.com/gh/sdpython/pyrsslocal/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/pyrsslocal/tree/master

.. image:: https://badge.fury.io/py/pyrsslocal.svg
    :target: http://badge.fury.io/py/pyrsslocal

.. image:: http://img.shields.io/github/issues/sdpython/pyrsslocal.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/pyrsslocal/issues

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://codecov.io/github/sdpython/pyrsslocal/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/pyrsslocal?branch=master

.. image:: https://pepy.tech/badge/pyrsslocal/month
    :target: https://pepy.tech/project/pyrsslocal/month
    :alt: Downloads

.. image:: https://img.shields.io/github/forks/sdpython/pyrsslocal.svg
    :target: https://github.com/sdpython/pyrsslocal/
    :alt: Forks

.. image:: https://img.shields.io/github/stars/sdpython/pyrsslocal.svg
    :target: https://github.com/sdpython/pyrsslocal/
    :alt: Stars

.. image:: https://img.shields.io/github/repo-size/sdpython/pyrsslocal
    :target: https://github.com/sdpython/pyrsslocal/
    :alt: size

This extension proposes a way to download new posts from blogs
and to navigate through them with a couple of HTML pages
managed by a local python server using a SQLite database:

::

    from pyrsslocal import rss_update_run_server
    fLOG (OutputPrint = True)
    xml_blogs = "subscriptions.xml"
    dbfile = "rss_posts.db3"
    rss_update_run_server(dbfile, xml_blogs)

The previous example takes a dump of blogs url coming from the former Google Reader (see below),
downloads RSS streams, loads everything into a database (SQLlite format),
and opens a local web application to read them, mark them, or search their titles.
The XML file which describes the blogs looks like this::

    <?xml version="1.0" encoding="UTF-8"?>
    <opml version="1.0">
        <body>

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

        </body>
    </opml>

.. only:: html

    .. image:: https://github.com/sdpython/pyrsslocal/blob/master/_doc/sphinxdoc/source/page1.png

.. only:: latex

    .. image:: page1.png

The design is not very efficient. It could be faster using a templating
library such a *jinja2*.

**Links:**

* `GitHub/pyrsslocal <https://github.com/sdpython/pyrsslocal/>`_
* `documentation <http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/blog/main_0000.html#ap-main-0>`_
