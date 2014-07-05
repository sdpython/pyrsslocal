"""
@file

@brief various function to get the content from a url
"""

from urllib.error import HTTPError, URLError
import urllib, urllib.request
import socket, http, gzip

from pyquickhelper import fLOG

def get_url_content(url, useMozilla = False):
    """
    retrieve the content of an url
    @param      url             (str) url
    @param      useMozilla      (bool) to use an header fill with Mozilla
    @return                     page
    """
    if useMozilla :
        req = urllib.request.Request(url, headers= { 'User-agent': 'Mozilla/5.0' })
        u = urllib.request.urlopen(req)
        text = u.read()
        u.close()
        text = text.decode("utf8")
        return text
    else :
        u = urllib.request.urlopen(url)
        text = u.read()
        u.close()
        text = text.decode("utf8")
        return text

def get_url_content_timeout(url, timeout = 10, output = None, encoding = "utf8"):
    """
    download a file from internet (we assume it is text information, otherwise, encoding should be None)
    
    @param      url         (str) url
    @param      timeout     (in seconds), after this time, the function drops an returns None, -1 for forever
    @param      output      (str) if None, the content is stored in that file
    @param      encoding    (str) utf8 by default, but if it is None, the returned information is binary
    @return                 content of the url
    
    If the function automatically detects that the downloaded data is in gzip
    format, it will decompress it.
    """
    try:
        if timeout != -1 :
            with urllib.request.urlopen(url, timeout=timeout) as ur :
                res = ur.read()
        else :
            with urllib.request.urlopen(url) as ur :
                res = ur.read()
    except (HTTPError, URLError) as error:
        fLOG("unable to retrieve content from ", url, "exc:", str(error))
        return None
    except socket.timeout as e:
        fLOG("unable to retrieve content from ", url, " because of timeout: ", timeout)
        return None
    except ConnectionResetError as e:
        fLOG("unable to retrieve content from ", url, " because of ConnectionResetError: ", e)
        return None
    except http.client.BadStatusLine as e:
        fLOG("unable to retrieve content from ", url, " because of http.client.BadStatusLine: ", e)
        return None
    except http.client.IncompleteRead as e:
        fLOG("unable to retrieve content from ", url, " because of http.client.IncompleteRead: ", e)
        return None
    except Exception as e:
        fLOG("unable to retrieve content from ", url, " because of unknown exception: ", e)
        raise e

    if len(res) >= 2 and res[:2] == b"\x1f\x8B" :
        # gzip format
        res = gzip.decompress(res)

    if encoding != None :
        try :
            content = res.decode(encoding)
        except UnicodeDecodeError as e :
            # we try different encoding
            
            laste  = [ e ]
            othenc = ["iso-8859-1", "latin-1"]
            
            for encode in othenc :
                try :
                    content = res.decode(encode)
                    break
                except UnicodeDecodeError as e :
                    laste.append(e)
                    content = None
                    
            if content == None :
                mes = [ "unable to parse blog post: " +  url ]
                mes.append ( "tried:" + str([ encoding] + othenc) )
                mes.append ( "beginning:\n" + str([res])[:50])
                for e in laste :
                    mes.append("Exception: " + str(e))
                raise ValueError ( "\n".join(mes))
    else :
        content = res
    
    if output != None :
        if encoding != None :
            with open(output,"w",encoding = encoding) as f :
                f.write (content)
        else :
            with open(output,"wb") as f :
                f.write (content)
    
    return content
    
