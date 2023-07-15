document.addEventListener('DOMContentLoaded', function() {
	var closeButton = document.getElementById('close');
	var errorPopup = document.getElementById('error-popup');

	closeButton.addEventListener('click', function() {
		errorPopup.style.display = 'none';
	});
	});