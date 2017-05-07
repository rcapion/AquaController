$(document).ready(function(){
	// Setup button click handlers
	$("button").click(function() {
		var id = $(this).attr('id');
		$.ajax({
			url: '/relays/changestate',
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
						element.data = resp.relayStateText;
					}
				}
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
});
