// Produce invald PopUp message
var closeButton = document.getElementById('close');
var errorPopup = document.getElementById('error-popup');


document.addEventListener('DOMContentLoaded', function () {
  closeButton.addEventListener('click', function() {
    errorPopup.style.display = 'none';
  });


  document.getElementById('myform').addEventListener('submit', function () {
      // Show the loading effect
      console.log("Loading Effect")
      document.getElementById('loadingEffect').style.display = 'block';
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


// Function to validate the URL (replace this with your actual URL validation logic)
function validateURL(url) {
  
  const regex = new RegExp(
      "^.*((youtu.be\\/)|(v\\/)|(\\/u\\/\\w\\/)|(embed\\/)|(watch\\?))\\??v?=?" +
      "([^#&?]*).*"
  );
  const match = url.match(regex);
  return  match && match[7] && match[7].length === 11 ? true : false;
}