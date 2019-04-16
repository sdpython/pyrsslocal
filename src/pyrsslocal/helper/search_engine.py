"""
@file

@brief various function to get the content of a page, of a search page...
"""

import urllib
import urllib.request
import time
import random
import re
import os

from pyquickhelper.loghelper import noLOG


def extract_bing_result(searchPage, filter_=lambda u: True):
    """
    extract the first results from a search page assuming it coms from `Bing <http://www.bing.com>`_
    @param      searchPage      content of `Bing <http://www.bing.com>`_ search page
    @param      filter_         remove some urls if this function is False ``filter_(u)`` --> True or False
    @return                     a list with the urls
    """
    reg = re.compile("""<h2><a href="(.*?)" h="ID=SERP,""")
    alls = reg.findall(searchPage)
    if alls is None or len(alls) == 0:
        return None
    else:
        if len(alls) > 10:
            alls = alls[:10]
        # here I sort by length, maybe not the best idea
        alltemp = sorted([(len(_), _) for _ in alls])
        # alltemp = [ (len(_), _) for _ in alls ]  # or not
        alls = [_ for _ in alltemp if filter_(_[1])]
        if len(alls) == 0:
            mes = "\n".join(str(_) for _ in alltemp)
            raise ValueError("unable to find a proper url\n" + mes)
        res = alls[0][1]
        if res in ["http://chrome.angrybirds.com/"]:
            join = "\n".join(str(_) for _ in alls)
            raise ValueError("bad result\n{0}".format(join))
        return [_[1] for _ in alls]


def query_bing(query,
               folderCache="cacheSearchPage",
               filter_=lambda u: True,
               fLOG=noLOG):
    """
    returns the search page from `Bing <http://www.bing.com>`_ for a specific query
    @param      query           search query
    @param      folderCache     folder used to stored the result page or to retrieve a page if the query was already searched for
    @param      filter_         remove some urls if this function is False ``filter(u)`` --> True or False
    @param      fLOG            logging function
    @return                     list of urls
    """
    if not os.path.exists(folderCache):
        os.mkdir(folderCache)
    cache = os.path.join(folderCache, "%s.bing.html" % query)
    if os.path.exists(cache):
        with open(cache, "r", encoding="utf8") as f:
            text = f.read()
    else:
        fLOG("    downloading results for ", query)
        x = 1. + random.random()
        time.sleep(x)
        url = "http://www.bing.com/search?q=" + query.replace(" ", "%20")
        with urllib.request.urlopen(url) as uur:
            text = uur.read()
        text = text.decode("utf8")

        fLOG("    caching results for ", query, " in ", cache)
        with open(cache, "w", encoding="utf8") as f:
            f.write(text)

    url = extract_bing_result(text, filter_)
    return url
