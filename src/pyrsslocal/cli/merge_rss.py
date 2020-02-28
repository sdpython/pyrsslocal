"""
@file
@brief Manipulate :epkg:`RSS` streams.
"""
import os
from ..rss.rss_helper import enumerate_rss_merge, to_rss, to_html


def compile_rss_blogs(links, url, description,
                      template=None, title="BLOG",
                      author="AUTHOR", keywords="blog,python",
                      out_html="index.html", out_rss="rssfile.xml",
                      validate=None, fLOG=print):
    """
    Compiles multiple blogs in one single blog. Uses
    :epkg:`RSS` files.

    @param      links           list of urls of blogs to merge
    @param      url             publishing url
    @param      description     description of the aggregation
    @param      title           title of the aggregation
    @param      author          author of the aggregation
    @param      keywords        keywords for the blog post
    @param      template        change the template for the blog aggregation
    @param      out_html        output :epkg:`HTML`
    @param      out_rss         output :epkg:`RSS`
    @param      validate        None or a function to validate a blog post,
                                ``validate(blog: BlogPost) -> bool``
    @param      fLOG            logging function
    """
    collect = []
    for i, blog in enumerate(
            enumerate_rss_merge(
                links, title=title, min_size=min_size)):
        fLOG("[compile_rss_blogs] reading blog {0}: {1} - '{2}'".format(
            i, blog.pubDate, blog.link))
        if validate in (None, '') or validate(blog):
            collect.append(blog)

    fLOG("[compile_rss_blogs] create '{0}'".format(out_rss))
    rss = to_rss(collect, url, description)
    with open(out_rss, "w", encoding="utf-8") as f:
        f.write(rss)

    fLOG("[compile_rss_blogs] create '{0}'".format(out_html))
    html = to_html(collect, template=template, title=title,
                   author=author, keywords=keywords,
                   header=description, rssfile=os.path.split(out_rss)[-1])
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
