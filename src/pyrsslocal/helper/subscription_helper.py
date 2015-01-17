"""
@file
@brief Various functions about subscriptions
"""

_example_subscriptions = """
<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
<body>

<outline text="XD Blog"
     title="XD Blog"
     type="rss"
     xmlUrl="http://www.xavierdupre.fr/blog/xdbrss.xml"
     htmlUrl="http://www.xavierdupre.fr/blog/xd_blog.html" />

</body>
</opml>
"""

def get_subscriptions_example(filename = None):
    """
    returns an example of a subscriptions file

    @param      filename        if not None, saves the string in that file
    @return                     example
    """
    if filename is not None:
        with open(filename, "w", encoding="utf8") as f :
            f.write(_example_subscriptions)

    return _example_subscriptions