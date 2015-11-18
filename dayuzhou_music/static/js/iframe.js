$(".fake").on("click",function(evt){
	
	window.parent.location.href = evt.target.href;
		//console.log(evt.target.href);
});