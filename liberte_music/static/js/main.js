
window.onhashchange = function(){
	//console.log("aa changed!");
	var _url = window.location.href;
	//访问去除#后的URL
	_url = _url.replace("/#","");
	//console.log("1 "+_url);

	_iframe = document.getElementById("l_iframe");
	_iframe.parentNode.removeChild(_iframe);
	_iframe = document.createElement('iframe');
	_iframe.id = 'l_iframe';
	_iframe.src = 'about:blank';
	_iframe.height = document.body.scrollHeight;
	_iframe.scrolling = "auto";
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

window.onresize = function(){
	//console.log("resize");
	var _iframe = document.getElementById("l_iframe");
	
	_iframe.height = document.body.clientHeight;
	//console.log(_iframe.height);

	_iframe.scrolling = "auto";
};

$(document).ready(function(){
	//load playlist
	var playlist_str = localStorage.getItem("playlist");
	var playlist_ul_str = localStorage.getItem("playlist_ul");
	var playlist = JSON.parse(playlist_str);
	window.playlist = playlist;
	document.getElementById("playlist-ul").innerHTML = playlist_ul_str;

	$("#playlist").delegate("li", "click", function(evt) {
		var _i = $("#playlist li").index($(evt.target));
		//console.log("i is :", _i);
		switchTrack(_i);
	});

	//setup iframe
	var _url = window.location.href;
	//console.log(document);
	_url = _url.replace("/#","");
	
	_iframe = document.getElementById("l_iframe");
	_iframe.parentNode.removeChild(_iframe);
	_iframe = document.createElement('iframe');
	_iframe.id = 'l_iframe';
	_iframe.src = 'about:blank';
	_iframe.height = document.body.scrollHeight;
	_iframe.scrolling = "auto";
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

