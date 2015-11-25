
window.onhashchange = function(){
	console.log("aa changed!");
	var _url = window.location.href;
	//访问去除#后的URL
	_url = _url.replace("/#","");
	console.log("1 "+_url);

	_iframe = document.getElementById("l_iframe");
	_iframe.parentNode.removeChild(_iframe);
	_iframe = document.createElement('iframe');
	_iframe.id = 'l_iframe';
	_iframe.src = 'about:blank';
	document.body.insertAdjacentElement('beforeEnd',_iframe);
	if(_url.indexOf("/",8) == _url.length - 1)
	{
		_iframe.contentWindow.location.href = "/home/";
	}
	else
	{
		_iframe.contentWindow.location.href = _url;
	}
};

$(document).ready(function(){
	var _url = window.location.href;
	//console.log(document);
	_url = _url.replace("/#","");
	
	_iframe = document.getElementById("l_iframe");
	_iframe.parentNode.removeChild(_iframe);
	_iframe = document.createElement('iframe');
	_iframe.id = 'l_iframe';
	_iframe.src = 'about:blank';
	
	document.body.insertAdjacentElement('beforeEnd',_iframe);
	
	if(_url.indexOf("/",8) == _url.length - 1)
	{
		_iframe.contentWindow.location.href = "/home/";
		//console.log(_iframe.contentWindow.location.href);
	}
	else
	{
		_iframe.contentWindow.location.href = _url;
	}
});

