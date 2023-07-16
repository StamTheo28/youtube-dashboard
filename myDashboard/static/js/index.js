document.addEventListener('DOMContentLoaded', function() {
	var closeButton = document.getElementById('close');
	var errorPopup = document.getElementById('error-popup');

	closeButton.addEventListener('click', function() {
		errorPopup.style.display = 'none';
	});
});

$(document).ready(function() {
	$('#calculate-button').click(function() {
	  // Show the loading overlay
	  $('#loading-overlay').show();
  
	  // Make an AJAX request to the calculate_view
	  $.ajax({
		type: 'GET',
		url: '/calculate/',
		success: function(response) {
		  // Hide the loading overlay
		  $('#loading-overlay').hide();
		  
		  // Process the response from the calculate_view
		  var result = response.result;
		  // Do something with the result
		},
		error: function() {
		  // Handle the error case
		  $('#loading-overlay').hide();
		}
	  });
	});
  });