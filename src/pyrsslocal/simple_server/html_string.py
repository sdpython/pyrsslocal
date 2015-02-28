"""
@file
@brief This module contains various string useful when a html page has to be produced.

It contains the following variables:

@var    html_header     a HTML header to use this way:
                                html_header % (title, author, keywords)
@var    html_footr      a HTML footer
"""

html_header = """
<?xml version="1.0" encoding="utf-8"?>
<html>
<head>
<link href="/js/pyrsslocal.ico" rel="shortcut icon"/>
<link href="/js/pMenu.css" rel="stylesheet" type="text/css"/>
<link rel="stylesheet" type="text/css" href="/js/prettify.css"/>
<title>%s</title>
<meta content="%s" name="author"/>
<meta content="%s" name="keywords"/>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<script src="/js/latexit.js" type="text/javascript"></script>
<script src="/js/run_prettify.js" type="text/javascript"></script>
<link href="/js/shCore.css" rel="stylesheet" type="text/css" />
<link href="/js/shThemeDefault.css" rel="stylesheet" type="text/css" />
<script src="/js/shCore.js" type="text/javascript"></script>
<script src="/js/shAutoloader.js" type="text/javascript"></script>
</head>
<body>
"""

html_footer = """
<script type="text/javascript">
SyntaxHighlighter.autoloader(
  'js jscript javascript  /js/shBrushJScript.js',
  'py python /js/shBrushPython.js',
  'xml html /js/shBrushXml.js',
  'cpp c /js/shBrushCpp.js',
  'sql /js/shBrushSql.js',
  'php /js/shBrushPhp.js',
  'vb vba /js/shBrushVb.js',
  'cs /js/shBrushCSharp.js',
  'css /js/shBrushCss.js'
);
SyntaxHighlighter.all();
</script>
</body>
</html>
"""


debug_string_script = """
from pandas import DataFrame
from pyrsslocal.helper.externs import df2html
pars = [ { "key":k, "value":v } for k,v in params.items() ]
tbl = DataFrame (pars)
print ( df2html(tbl, class_table="myclasstable") )
"""

html_debug_string_script = """
<b>executing the following script python</b>
<br/>
<pre class="prettyprint">
%s
</pre>
<script type="text/python">
%s
</script>
""" % (debug_string_script, debug_string_script)

html_debug_string = "\n".join(
    [html_header % ("debug", "xd", ""), html_debug_string_script, html_footer])
