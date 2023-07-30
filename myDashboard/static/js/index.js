document.addEventListener('DOMContentLoaded', function() {
	var closeButton = document.getElementById('close');
	var errorPopup = document.getElementById('error-popup');

	closeButton.addEventListener('click', function() {
		errorPopup.style.display = 'none';
	});
});


let hoverTimeout;

function handleMouseLeave() {
  hoverTimeout = setTimeout(() => {
    const searchInput = document.querySelector('.searchInput');
    const searchButton = document.querySelector('.searchButton');
    searchInput.classList.remove('hover-effect');
    searchButton.classList.remove('hover-effect');
  }, 600); // Delay in milliseconds (200ms = 0.2 seconds)
}

function handleMouseEnter() {
  clearTimeout(hoverTimeout);
  const searchInput = document.querySelector('.searchInput');
  const searchButton = document.querySelector('.searchButton');
  searchInput.classList.add('hover-effect');
  searchButton.classList.add('hover-effect');
}


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
