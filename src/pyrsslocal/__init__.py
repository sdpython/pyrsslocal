#-*- coding: utf-8 -*-
"""
@file
@brief Shortcuts for module pyrsslocal.
"""

__version__ = "0.8"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/pyrsslocal"
__url__ = "http://www.xavierdupre.fr/app/pyrsslocal/helpsphinx/index.html"
__downloadUrl__ = "http://www.xavierdupre.fr/site2013/index_code.html#pyrsslocal"
__license__ = "MIT License"


def _setup_hook():
    """
    does nothing
    """
    pass


from .rss.rss_helper import rss_update_run_server, rss_run_server
from .rss.rss_database import DatabaseRSS
from .custom_server.aserver import CustomDBServerHandler, CustomDBServer
from .helper.subscription_helper import get_subscriptions_example
from .rss.rss_simple_server import RSSSimpleHandler, RSSServer
