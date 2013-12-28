pyensae documentation
=====================

.. contents::
   :depth: 3


Introduction
------------



The project is hosted `here <http://www.xavierdupre.fr/site2013/index_code.html>`_ 
and on github: `pyrsslocal <https://github.com/sdpython/pyrsslocal/>`_.

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


Contribution
------------

The library is public and available on `github <https://github.com/sdpython/pyrsslocal/>`_. 
Please do not commit without running the unit test and add a unit test for every of your contributions.
See :ref:`l-doctestunit` to see how to run them and to generate the documentation.

Dependencies
------------

    * `pyquickhelper <http://www.xavierdupre.fr/app/pyquickhelper/helpsphinx/index.html>`_
    * `pyensae <http://www.xavierdupre.fr/app/pyensae/helpsphinx/index.html>`_


About this documentation
------------------------

.. toctree::
    :maxdepth: 2

    generatedoc
    glossary

    
Indices and tables
==================

+------------------+---------------------+------------------+------------------+------------------------+---------------------+
| :ref:`l-modules` |  :ref:`l-functions` | :ref:`l-classes` | :ref:`l-methods` | :ref:`l-staticmethods` | :ref:`l-properties` |
+------------------+---------------------+------------------+------------------+------------------------+---------------------+
| :ref:`genindex`  |  :ref:`modindex`    | :ref:`search`    | :ref:`l-license` | :ref:`l-changes`       | :ref:`l-README`     |
+------------------+---------------------+------------------+------------------+------------------------+---------------------+
   

