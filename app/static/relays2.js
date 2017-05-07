$(function(){

	$('form').on('submit',function(event){
		var id = $('#relayID',this).val();
		var state = $('#relayState',this).val();
		console.log($('form').serialize());
		var test ='relayID=' + $('#relayID',this).val() + '&relayState=' + $('#relayState',this).val();
		console.log(test);
		$.ajax({
			url: '/process',
			data: test,
			type: 'POST',
			success: function(response){
				console.log(response);
				var resp = JSON.parse(response);
				console.log(resp);
				$('#relayState', this).val(resp.relayState);
				$('#relayStateText', this).text(resp.relayStateText);
			},
			error: function(error){
				console.log(error);
				$('#relayState').val(response.error);
			}
		});
		event.preventDefault();
	});
});
