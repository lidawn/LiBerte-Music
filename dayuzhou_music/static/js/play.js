function playsong(is_playable,id,name,artist,album){
	$.ajax({
			type : "POST",
			url : "/get_link/",
			data : {is_playable:is_playable,id:id,name:name,artist:artist,album:album},
			dataType : "text",
			success : function(ret){
				if(ret != "404")
				{
					song = {
						title: name,
						artist: artist,
						album: album,
						cover:'',
						mp3: ret,
						ogg: ''
						};
						playlist.push(song);
						//console.log(playlist);
						$('#playlist').append('<li>'+song.artist+' - '+song.title+'</li>');
				}
			}
		});
}

function playalbum(){

}

function playcollect(){

}