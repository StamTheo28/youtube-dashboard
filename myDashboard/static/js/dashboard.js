
// Read more button
var readMoreButtons = document.querySelectorAll('.read-more');

readMoreButtons.forEach(function(button) {
button.style.display = 'inline';
button.addEventListener('click', function() {
    var description = this.previousElementSibling;
    description.classList.toggle('expanded');
    this.textContent = description.classList.contains('expanded') ? 'Read Less' : 'Read More';
    });
});

