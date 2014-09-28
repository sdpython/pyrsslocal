"""
@file
@brief Uses `Flask <http://flask.pocoo.org/>`_ to build pages.
"""

from flask import Flask, Response,redirect,url_for,render_template
import os

try:
    from .rss_flask_helper import get_text_file, get_binary_file
except:
    from rss_flask_helper import get_text_file, get_binary_file

# -- HELP BEGIN EXCLUDE --
app = Flask(__name__)
app.config.from_object(__name__)
# -- HELP END EXCLUDE --


# -- HELP BEGIN EXCLUDE --
@app.route("/")
# -- HELP END EXCLUDE --
def main_page():
    """
    serves the main page
    """
    return get_resource ("rss_reader.html")
    
# -- HELP BEGIN EXCLUDE --
@app.errorhandler(500)
# -- HELP END EXCLUDE --
def internal_error(error):
    """
    intercept an error
    """
    return  render_template("errors.html", 
                error=str(error), 
                message="Internal Error"), 500

# -- HELP BEGIN EXCLUDE --
@app.errorhandler(404)
# -- HELP END EXCLUDE --
def not_found(error):
    """
    intercept an error
    """
    return  render_template("errors.html", 
                error=str(error),
                message="Not Found"), 404   
    
# -- HELP BEGIN EXCLUDE --
@app.route('/js/', defaults={'path': ''})
@app.route('/js/<path:path>')
# -- HELP END EXCLUDE --
def get_js(path):  # pragma: no cover
    """
    serves static files
    
    @param      path        relative path
    @return                 content
    """
    try:
        mimetypes = {
            ".js":      ("application/javascript",get_text_file),
        }
        ext      = os.path.splitext(path)[1]
        cp       = mimetypes[ext]
        mimetype = cp[0]
        content  = cp[1](os.path.join("..","javascript",path))
        r        = Response(content, mimetype=mimetype)    
        return r
    except Exception as e :
        print(e)
        raise e

# -- HELP BEGIN EXCLUDE --
@app.route('/logs/', defaults={'path': ''})
@app.route('/logs/<path:path>')
# -- HELP END EXCLUDE --
def url_logging(path):  # pragma: no cover
    """
    serves static files
    
    @param      path        relative path
    @return                 content
    """
    print("logging",path)
    
# -- HELP BEGIN EXCLUDE --
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# -- HELP END EXCLUDE --
def get_resource(path):  # pragma: no cover
    """
    serves static files
    
    @param      path        relative path
    @return                 content
    """
    try:
        mimetypes = {
            ".css":     ("text/css",get_text_file),
            ".html":    ("text/html",get_text_file),
            ".js":      ("application/javascript",get_text_file),
            ".png":     ("image/png",get_binary_file),
        }
        ext      = os.path.splitext(path)[1]
        cp       = mimetypes.get(ext, ("text/plain",get_binary_file))
        mimetype = cp[0]
        content  = cp[1](path)
        r        = Response(content, mimetype=mimetype)    
        return r
    except Exception as e :
        print(e)
        raise e


# -- HELP BEGIN EXCLUDE --
if __name__ == "__main__":
    app.run()
# -- HELP END EXCLUDE --

    