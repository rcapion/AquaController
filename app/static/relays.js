$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : JSON.stringify({
				id : $('#relayID').val(),
				state : $('#relayState').val()
			}),
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			if (data.error) {
				$('#relayStateText').text(data.error);
			}
			else {
				$('#relayState').val(data.relayState);
				$('#relayStateText').text(data.relayStateText);
			}

		});

		event.preventDefault();

	});

});
