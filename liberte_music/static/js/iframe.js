$(".fake").on("click",function(evt){
	if (evt.target.href == window.parent.location.href)
	{
		return false;
	}
	else
	{
		window.parent.location.href = evt.target.href;
	}
	
});