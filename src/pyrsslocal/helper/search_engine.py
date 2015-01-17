#coding:latin-1
"""
@file

@brief various function to get the content of a page, of a search page...
"""

import urllib, urllib.request, time, random, re, os

from pyquickhelper import fLOG

def extract_bing_result (searchPage, filter = lambda u : True) :
    """
    extract the first results from a search page assuming it coms from `Bing <http://www.bing.com>`_
    @param      searchPage      content of `Bing <http://www.bing.com>`_ search page
    @param      filter          remove some urls if this function is False ``filter(u)`` --> True or False
    @return                     a list with the urls
    """
    reg = re.compile("""<h3><a href="(.*?)" h="ID=SERP,""")
    all = reg.findall (searchPage)
    if all == None or len(all) == 0 :
        return None
    else :
        if len(all) > 10 : all = all[:10]
        alltemp = sorted ([ (len(_), _) for _ in all ])    # here I sort by length, maybe not the best idea
        #alltemp = [ (len(_), _) for _ in all ]  # or not
        all = [ _ for _ in alltemp if filter(_[1]) ]
        if len(all) == 0 :
            for _ in alltemp :
                print (_)
            raise ValueError("unable to find a proper url")
        res = all [0][1]
        if res in ["http://chrome.angrybirds.com/"] :
            for _ in all :
                print (_)
            raise ValueError("bad result " + res)
        return all[0][1]

def query_bing (    query,
                    folderCache = "cacheSearchPage",
                    filter = lambda u : True,
                    flog = fLOG) :
    """
    returns the search page from `Bing <http://www.bing.com>`_ for a specific query
    @param      query           search query
    @param      folderCache     folder used to stored the result page or to retrieve a page if the query was already searched for
    @param      filter          remove some urls if this function is False ``filter(u)`` --> True or False
    @param      flog            logging function
    @return                     list of urls
    """
    if not os.path.exists (folderCache) : os.mkdir (folderCache)
    cache = os.path.join(folderCache, "%s.bing.html" % query)
    if os.path.exists (cache) :
        f = open(cache, "r", encoding="utf8")
        text = f.read()
        f.close ()
    else :
        flog ("    downloading results for ", query)
        x = 1. + random.random()
        time.sleep(x)
        url = "http://www.bing.com/search?q=" + query.replace(" ", "%20")
        u = urllib.request.urlopen(url)
        text = u.read()
        u.close()
        text = text.decode("utf8")

        flog ("    caching results for ", query, " in ", cache)
        f = open(cache, "w", encoding="utf8")
        f.write (text)
        f.close ()

    url = extract_bing_result(text, filter)
    return url