

.. _l-README:

README / Changes
================


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
   
.. image:: https://requires.io/github/sdpython/pyrsslocal/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/pyrsslocal/requirements/?branch=master
     :alt: Requirements Status   
    
.. image:: https://codecov.io/github/sdpython/pyrsslocal/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/pyrsslocal?branch=master
    

**Links:**
    * `pypi/pyrsslocal <https://pypi.python.org/pypi/pyrsslocal/>`_
    * `GitHub/pyrsslocal <https://github.com/sdpython/pyrsslocal/>`_
    * `documentation <http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/index.html>`_
    * `Windows Setup <http://www.xavierdupre.fr/site2013/index_code.html#pyrsslocal>`_
    * `Travis <https://travis-ci.org/sdpython/pyrsslocal>`_
    * `Blog <http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/blog/main_0000.html#ap-main-0>`_


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
    
.. image:: https://github.com/sdpython/pyrsslocal/blob/master/_doc/sphinxdoc/source/page1.png

    

Versions
--------

* **0.8 - 2016/??/??**
    * **new:** function get_subscriptions_example returns a short sample of a subscription xml file
    * **new:** add class CustomDBServer to be able to use HTML as an interface for a local program
    * **fix:** the setup does not need the file ``README.rst`` anymore
    
    
