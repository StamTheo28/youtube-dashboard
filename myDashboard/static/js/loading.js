document.addEventListener('DOMContentLoaded', function() {
  // Make an AJAX request to the analysis view
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/path/to/analysis/', true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      if (response.completed) {
        // Redirect to the dashboard page when the computation is complete
        window.location.href = '/path/to/dashboard/';
      }
    }
  };
  xhr.send();
});
