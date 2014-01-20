// initialize foundation
$(document).foundation();

// add close button to dropdown
$('#howto-close').click(function() { $('body').trigger('click')});

function validateQuestion() {
  // url validation RegExp
  var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
  var message = 'Provided URL seems to be invalid, please check it once more';
  var question = $("#questionForm").find('input[name="question"]').val();

	if (regexp.test(question)) {
		return true;
  }
  else {
    $('#alert').html('<div class="alert-box alert" data-alert><span id="info">' + message + '</span><a class="close" href="#">&times;</a></div>');
    $(document).foundation('alert');
    return false;
  }
}
