"""
@file
@brief Uses `Flask <http://flask.pocoo.org/>`_ to build pages.
"""

from flask import Flask, Response,redirect,url_for,render_template
import os

try:
    from .rss_flask_helper import main_page_content, get_text_file, get_binary_file
except:
    from rss_flask_helper import main_page_content, get_text_file, get_binary_file

app = Flask(__name__)
app.config.from_object(__name__)



@app.route("/")
def main_page():
    """
    serves the main page
    """
    return get_resource ("rss_reader.html")
    
@app.errorhandler(500)
def internal_error(error):
    """
    intercept an error
    """
    return  render_template("errors.html", 
                error=str(error), 
                message="Internal Error"), 500

@app.errorhandler(404)
def not_found(error):
    """
    intercept an error
    """
    return  render_template("errors.html", 
                error=str(error),
                message="Not Found"), 404   
    
@app.route('/js/', defaults={'path': ''})
@app.route('/js/<path:path>')
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

@app.route('/logs/', defaults={'path': ''})
@app.route('/logs/<path:path>')
def url_logging(path):  # pragma: no cover
    """
    serves static files
    
    @param      path        relative path
    @return                 content
    """
    print("logging",path)
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
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


if __name__ == "__main__":
    app.run()