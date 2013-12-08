function windowReady()
{
	var pxPageWidth = $(window).width();
	var fontPageWidth = Math.floor(pxPageWidth * 0.9);
	
	$("input[name=question]").css("width", fontPageWidth);
	
	$("#info").text("");
}

function resizeQuestionInput()
{
	var pxPageWidth = $(window).width();
	var fontPageWidth = Math.floor(pxPageWidth * 0.9);
	
	$("input[name=question]").css("width", fontPageWidth);
}

function validateQuestion() {
	var question = $("#questionForm").find('input[name="question"]').val();
	if (question == "")
	{
		$("#info").text("Input field cannot be empty.");
		return false;
	}
	else
	{
		return true;
	}
}