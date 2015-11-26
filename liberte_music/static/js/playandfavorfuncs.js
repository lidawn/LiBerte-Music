//虾米推荐全部播放
function playall_xiami_taste(){
	var xiami_str = document.getElementById("taste_xiami").value;
	if(xiami_str!="")
	{
		var xiami = JSON.parse( xiami_str );
		var length = xiami.length ;
		var ul = window.parent.document.getElementById("playlist");
		if(window.parent.playlist[0]["title"] == "-")
		{
			window.parent.playlist.shift();
			var li = ul.childNodes[0];
			ul.removeChild(li);
		}
		var length_playlist = window.parent.playlist.length;
		for (var i = 0; i < length; i++) {
			song = {
				title: xiami[i]["name"],
				title_url:"http://www.xiami.com/song/"+xiami[i]["id"],
				artist: xiami[i]["artist_name"],
				album: xiami[i]["album_name"],
				cover:xiami[i]["cover"],
				mp3: xiami[i]["mp3Url"],
				ogg: ''
			};
				
			window.parent.playlist.push(song);
			localStorage.setItem("playlist",JSON.stringify(window.parent.playlist));
			var li = document.createElement('li');
			li.textContent = song.artist+' - '+song.title;
			ul.appendChild(li);
			localStorage.setItem("playlist_ul",ul.parentNode.innerHTML);
		}
		window.parent.switchTrack(length_playlist);
	}
}
//虾米推荐，因为直接有歌曲URL
function playsong_xiami_taste(id,name,artist,album,cover,mp3Url){
	var title_url= "http://www.xiami.com/song/"+id;
	song = {
		title: name,
		title_url:title_url,
		artist: artist,
		album: album,
		cover:cover,
		mp3: mp3Url,
		ogg: ''
	};
	var ul = window.parent.document.getElementById("playlist");

	if(window.parent.playlist[0]["title"] == "-")
	{
		window.parent.playlist.shift();
		var li = ul.childNodes[0];
		ul.removeChild(li);
	}
	var length_playlist = window.parent.playlist.length;
	window.parent.playlist.push(song);
	localStorage.setItem("playlist",JSON.stringify(window.parent.playlist));
	var li = document.createElement('li');
	li.textContent = song.artist+' - '+song.title;
	ul.appendChild(li);
	localStorage.setItem("playlist_ul",ul.parentNode.innerHTML);
	window.parent.switchTrack(length_playlist);
}
//标准播放
function playsong(is_playable,type,id,name,artist,artist_id,album,album_id,cover){
	var title_url;
	if(type=='n')
	{
		title_url = "http://music.163.com/song?id="+id
	}
	else
	{
		title_url = "http://www.xiami.com/song/"+id
	}
	$.ajax({
		type : "POST",
		url : "/get_link/",
		data : {is_playable:is_playable,type:type,id:id,name:name,artist:artist,artist_id:artist_id,album:album,album_id:album_id,cover:cover},
		dataType : "text",
		success : function(ret){
			rarray = ret.split(";")
			if(rarray[0] != "404")
			{
				song = {
					title: name,
					title_url:title_url,
					artist: artist,
					album: album,
					cover:rarray[1],
					mp3: rarray[0],
					ogg: ''
				};
				var ul = window.parent.document.getElementById("playlist");
				if(window.parent.playlist[0]["title"] == "-")
				{
					window.parent.playlist.shift();
					var li = ul.childNodes[0];
					ul.removeChild(li);
				}
				var length_playlist = window.parent.playlist.length;
				window.parent.playlist.push(song);
				localStorage.setItem("playlist",JSON.stringify(window.parent.playlist));
				var li = document.createElement('li');
				li.textContent = song.artist+' - '+song.title;
				ul.appendChild(li);
				localStorage.setItem("playlist_ul",ul.parentNode.innerHTML);
				window.parent.switchTrack(length_playlist);
			}
		}
	});
}

//播放网易收藏全部
function playall_netease_detail(){
	var detail_str = document.getElementById("detail").value;
		
	if(detail_str!="")
	{
		
		var detail = JSON.parse( detail_str );
		var length = detail.length ;
		var ul = window.parent.document.getElementById("playlist");

		if(window.parent.playlist[0]["title"] == "-")
		{
			window.parent.playlist.shift();
			var li = ul.childNodes[0];
			ul.removeChild(li);
		}
		var length_playlist = window.parent.playlist.length;
		for (var i = 0; i < length; i++) {
			
			song = {
				title: detail[i]["name"],
				title_url: "http://music.163.com/song?id="+detail[i]["id"],
				artist: detail[i]["artist_name"],
				album: detail[i]["album_name"],
				cover:detail[i]["cover"],
				mp3: detail[i]["mp3Url"],
				ogg: ''
			};
			window.parent.playlist.push(song);
			localStorage.setItem("playlist",JSON.stringify(window.parent.playlist));
			var li = document.createElement('li');
			li.textContent = song.artist+' - '+song.title;
			ul.appendChild(li);
			localStorage.setItem("playlist_ul",ul.parentNode.innerHTML);
		}
		window.parent.switchTrack(length_playlist);
	}
}

//网易收藏，因为直接由歌曲URL
function playsong_netease_detail(id,name,artist,album,cover,mp3Url){
	song = {
		title: name,
		title_url:"http://music.163.com/song?id="+id,
		artist: artist,
		album: album,
		cover:cover,
		mp3: mp3Url,
		ogg: ''
	};
	var ul = window.parent.document.getElementById("playlist");
	if(window.parent.playlist[0]["title"] == "-")
	{
		window.parent.playlist.shift();
		var li = ul.childNodes[0];
		ul.removeChild(li);
	}
	var length_playlist = window.parent.playlist.length;
	window.parent.playlist.push(song);
	localStorage.setItem("playlist",JSON.stringify(window.parent.playlist));
	var li = document.createElement('li');
	li.textContent = song.artist+' - '+song.title;
	ul.appendChild(li);
	localStorage.setItem("playlist_ul",ul.parentNode.innerHTML);
	window.parent.switchTrack(length_playlist);
}

//添加收藏
function favorsong(type,id,name,artist,artist_id,album,album_id){
		
	if(window.event.target.nodeName == "SPAN")
	{
		var button = window.event.target.parentNode;
	}
	else
	{
		var button = window.event.target;
	}
	$.ajax({
		type : "POST",
		url : "/add_to_playlist/",
		data : {type:type,id:id,name:name,artist:artist,artist_id:artist_id,album:album,album_id:album_id},
		dataType : "text",
		success : function(ret){
			if(ret == "True")
			{
				button.className = "btn btn-danger btn-sm";
				button.childNodes[1].className = "glyphicon glyphicon-star";
			}
		}
	});
}