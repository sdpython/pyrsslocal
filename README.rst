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

