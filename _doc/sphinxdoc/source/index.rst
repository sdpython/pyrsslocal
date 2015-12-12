pyrsslocal documentation
========================

.. image:: https://travis-ci.org/sdpython/pyrsslocal.svg?branch=master
    :target: https://travis-ci.org/sdpython/pyrsslocal
    :alt: Build status
    
.. image:: https://ci.appveyor.com/api/projects/status/3v5swlh83cp2wdpt?svg=true
    :target: https://ci.appveyor.com/project/sdpython/pyrsslocal
    :alt: Build Status Windows
    
.. image:: https://badge.fury.io/py/pyrsslocal.svg
    :target: http://badge.fury.io/py/pyrsslocal

.. image:: http://img.shields.io/pypi/dm/pyrsslocal.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/pyrsslocal

.. image:: http://img.shields.io/github/issues/sdpython/pyrsslocal.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/pyrsslocal/issues
    
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://landscape.io/github/sdpython/pyrsslocal/master/landscape.svg?style=flat
   :target: https://landscape.io/github/sdpython/pyrsslocal/master
   :alt: Code Health

**Links:** `pypi <https://pypi.python.org/pypi/pyrsslocal/>`_,
`github <https://github.com/sdpython/pyrsslocal/>`_,
`documentation <http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/index.html>`_,
`wheel <http://www.xavierdupre.fr/site2013/index_code.html#pyrsslocal>`_,
:ref:`l-README`,
:ref:`blog <ap-main-0>`


What is it?
-----------

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
    
Yu can create an empty with::

    from pyrsslocal import write_subscriptions_example
    xml_blogs = "subscriptions.xml"
    write_subscriptions_example(xml_blogs)

You can enumerate the blog posts in the database::

    from pyrsslocal import pyrsslocal
    db = DatabaseRSS(dbfile, LOG = fLOG)
    for blog in db.enumerate_posts() :
        print (blog)
        
Installation
------------

``pip install pyrsslocal``


Snapshots    
---------

Main page:

.. image:: page1.png
    :width: 600px

Marked blog posts:

.. image:: page2.png
    :width: 600px

Search page:

.. image:: page3.png
    :width: 600px


Quick start
-----------

.. toctree::
    :maxdepth: 1
    
    all_example
    all_notebooks
        

Functionalities
---------------

* retrieve blog posts and store them into a SQLite database
* Python server accepting python script inside HMTL pages
* run Python script after adding variables to the script context
* download webpage and handle encoding
* javascript files to emphasize python syntax in a HTML page
* a custom server to HTML as an interface for a local program


Navigation
----------

.. toctree::
    :maxdepth: 1
    
    indexmenu


    
Indices and tables
------------------

+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`l-modules`     |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods`   | :ref:`l-staticmethods` | :ref:`l-properties`                            |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`modindex`      |  :ref:`l-example`   | :ref:`search`       | :ref:`l-license`   | :ref:`l-changes`       | :ref:`l-README`                                |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`genindex`      |  :ref:`l-FAQ`       | :ref:`l-notebooks`  |                    | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+

  
