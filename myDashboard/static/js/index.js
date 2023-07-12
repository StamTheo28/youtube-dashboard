let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
	nav.classList.toggle("navclose");
})

alert("Hello world")


function toggleViewMore() {
	var paragraph = document.getElementById('paragraph');
	var btn = document.getElementById('viewMoreBtn');
	
	if (paragraph.classList.contains('show')) {
	  paragraph.classList.remove('show');
	  btn.textContent = 'View More';
	} else {
	  paragraph.classList.add('show');
	  btn.textContent = 'View Less';
	}
  }