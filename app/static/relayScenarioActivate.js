$(document).ready(function(){
	// Setup button click handlers
	$("button").click(function() {
		var id = $(this).attr('id');
		if (document.getElementById(id).firstChild) {
			document.getElementById(id).firstChild.data = 'Activating...';
		}
		$.ajax({
			url: '/relayscenario/activate',
			data: id,
			type: 'POST',
			success: function(response){
				var resp = JSON.parse(response);
				var element = document.getElementById(resp.ID).firstChild;
				if (element) {
					if (resp.error) {
						element.data = resp.error;
						console.log(resp)
					} else {
						element.data = resp.activationText;
						setTimeout(function() {
							element.data = 'Activate';
						}, 5000);
					}
				}
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
});
