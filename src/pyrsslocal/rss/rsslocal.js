function getUrlVars() 
{
    var vars = {};
    var parts = window.location.href.replace('/[?&]+([^=&]+)=([^&]*)/gi', function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function getUrlVarsString() 
{
    var ind = window.location.href.indexOf("?") ;
    if (ind != -1) {
        return window.location.href.substring(ind, window.location.href.length) ;
    }
    else {
        return '' ;
    }
}

function setPositions(listDiv)
{
    sendimp("url/" + document.location.href); 
    for (var i = 0 ; i < listDiv.length ; ++i)
    {
        var divObject = document.getElementById(listDiv[i]);
        var pos = getPosition(listDiv[i]);
        divObject.scrollTop = pos ;
    }
}

function sendlog(link) 
{
    var info = 'logs/click/' + getUUID() + '/' + encodeURIComponent(link) ;
    var pageRequest = new XMLHttpRequest()
    pageRequest.open('GET', info, false);
    pageRequest.send(null);
    //return pageRequest.responseXML;
}

function sendimp(link) 
{
    var info = 'logs/imp/' + getUUID() + '/' + encodeURIComponent(link) ;
    var pageRequest = new XMLHttpRequest()
    pageRequest.open('GET', info, false);
    pageRequest.send(null);
    //return pageRequest.responseXML;
}

function createCookie(name,value,days) 
{
	if (days) 
    {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) 
{
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) 
{
	createCookie(name,"",-1);
}

function savePosition(divId)
{
    var intY = document.getElementById(divId).scrollTop;
    if (intY >= 0) {
        createCookie("divid" + divId, "y" + intY + "_", 1) ;
    }
}

function getPosition(divId)
{
    var cook  = readCookie("divid" + divId) ;
    if (cook == null) return 0 ;
    var start = cook.indexOf("y") ;
    if (start == -1) return 0 ;
    var end   = cook.indexOf("_", start) ;
    var sub = cook.substring( start+1, end) ;
    return sub ;
}

function generateUUID()
{
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x7|0x8)).toString(16);
    });
    return uuid;
}

function getUUID()
{
    var uuid = readCookie("rssuuid") ;
    if (uuid == null) {
        var uu = generateUUID() ;
        createCookie("rssuuid", uu) ;
        return uu ;
    }
    else {
        return uuid ;
    }
}

//// part for loading documents

function loadDoc(urlPage, idpageElement, exescript, anchorbegin)
{
    var pageElement = document.getElementById(idpageElement);
    var xmlhttp = null; 
    if (window.XMLHttpRequest) {   
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else {   
        // code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            processEventText(pageElement, xmlhttp.responseText, exescript, anchorbegin) ;
        }
        else {
            processEventText(pageElement, '<body>unable to access <a href="' + urlPage + '">' + urlPage + '</a> status ' + xmlhttp.status + '</body>', exescript) ;
        }
    }
    
    urlPage = "/fetchurlclean/" + urlPage ;
    xmlhttp.open("GET",urlPage,true);
    xmlhttp.send(null);
}

function loadExe(urlPage, idpageElement)
{
    var pageElement = document.getElementById(idpageElement);
    var xmlhttp = null; 
    if (window.XMLHttpRequest) {   
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else {   
        // code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            processEventText(pageElement, xmlhttp.responseText, true, '') ;
        }
        else {
            processEventText(pageElement, '<body>unable to access <a href="' + urlPage + '">' + urlPage + '</a> status ' + xmlhttp.status + '</body>', exescript) ;
        }
    }
    
    urlPage = "/rssfetchlocalexe/" + urlPage ;
    xmlhttp.open("GET",urlPage,true);
    xmlhttp.send(null);
}

function processEventText(pageElement, body, exescript, anchorbegin)
{
    var bodyp = body.indexOf("<body>") + 6;
    if (anchorbegin.length > 0) {
        var anchor = body.indexOf(anchorbegin, bodyp) + anchorbegin.length;
        if (anchor > bodyp) bodyp = anchor ;
    }
    var bodype = body.lastIndexOf("</body>");
    var page = body.substring(bodyp, bodype);
    pageElement.innerHTML = page ;
    
    if (exescript) {
        // on execute les scripts de la page
        var scripts = [];

        ret = pageElement.childNodes;
        for ( var i = 0; ret[i]; i++ ) {
          if ( scripts && nodeName( ret[i], "script" ) && 
              (!ret[i].type || ret[i].type.toLowerCase() === "text/javascript") ) 
            {
                scripts.push( ret[i].parentNode ? ret[i].parentNode.removeChild( ret[i] )
                                   : ret[i] );
            }
        }

        for(script in scripts)
        {
          evalScript(scripts[script]);
        }    
    }
}
  
function evalScript( elem ) 
{
    data = ( elem.text || elem.textContent || elem.innerHTML || "" );

    var head = document.getElementsByTagName("head")[0] || 
                  document.documentElement ;
    var script = document.createElement("script");
    script.type = "text/javascript";
    
   try {
      // doesn't work on ie...
      script.appendChild(document.createTextNode(data));      
    } catch(e) {
      // IE has funky script nodes
      script.text = data;
    }
    
    head.insertBefore( script, head.firstChild );
    head.removeChild( script );

    if ( elem.parentNode ) {
        elem.parentNode.removeChild( elem );
    }
}


