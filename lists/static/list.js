// Find all input elements, and for each, attach an event listener which
// reacts to on keypress events and click 
$(document).ready(function($) {
	$('#id_text').on('keypress click', function () {
		$('.has-error').hide();
	});
});