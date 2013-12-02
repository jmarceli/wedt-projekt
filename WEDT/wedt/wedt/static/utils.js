function resizeQuestionInput()
{
	var pxPageWidth = $(window).width();
	var fontPageWidth = Math.floor(pxPageWidth * 0.9);
	
	$("input[name=question]").css("width", fontPageWidth);
}