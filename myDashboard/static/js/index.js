// Produce invald PopUp message
var closeButton = document.getElementById('close');
var errorPopup = document.getElementById('error-popup');

// Close error popup listener
closeButton.addEventListener('click', function() {
  errorPopup.style.display = 'none';
});

// Activate loading effect listener
document.getElementById('myform').addEventListener('submit', function () {
  console.log("Activating Loading Effect")
  document.getElementById('loadingEffect').style.display = 'block';
});




// Function to validate the URL (replace this with your actual URL validation logic)
function validateURL(url) {
  
  const regex = new RegExp(
      "^.*((youtu.be\\/)|(v\\/)|(\\/u\\/\\w\\/)|(embed\\/)|(watch\\?))\\??v?=?" +
      "([^#&?]*).*"
  );
  const match = url.match(regex);
  return  match && match[7] && match[7].length === 11 ? true : false;
}