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


def extract_bing_result(searchPage, filter=lambda u: True):
    """
    extract the first results from a search page assuming it coms from `Bing <http://www.bing.com>`_
    @param      searchPage      content of `Bing <http://www.bing.com>`_ search page
    @param      filter          remove some urls if this function is False ``filter(u)`` --> True or False
    @return                     a list with the urls
    """
    reg = re.compile("""<h2><a href="(.*?)" h="ID=SERP,""")
    all = reg.findall(searchPage)
    if all is None or len(all) == 0:
        return None
    else:
        if len(all) > 10:
            all = all[:10]
        # here I sort by length, maybe not the best idea
        alltemp = sorted([(len(_), _) for _ in all])
        # alltemp = [ (len(_), _) for _ in all ]  # or not
        all = [_ for _ in alltemp if filter(_[1])]
        if len(all) == 0:
            mes = "\n".join(str(_) for _ in alltemp)
            raise ValueError("unable to find a proper url\n" + mes)
        res = all[0][1]
        if res in ["http://chrome.angrybirds.com/"]:
            join = "\n".join(str(_) for _ in all)
            raise ValueError("bad result\n{0}".format(join))
        return [_[1] for _ in all]


def query_bing(query,
               folderCache="cacheSearchPage",
               filter=lambda u: True,
               fLOG=noLOG):
    """
    returns the search page from `Bing <http://www.bing.com>`_ for a specific query
    @param      query           search query
    @param      folderCache     folder used to stored the result page or to retrieve a page if the query was already searched for
    @param      filter          remove some urls if this function is False ``filter(u)`` --> True or False
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
        with urllib.request.urlopen(url) as u:
            text = u.read()
        text = text.decode("utf8")

        fLOG("    caching results for ", query, " in ", cache)
        with open(cache, "w", encoding="utf8") as f:
            f.write(text)

    url = extract_bing_result(text, filter)
    return url
