
// JavaScript to handle active class based on current URL
const currentUrl = window.location.pathname;
const navLinks = document.querySelectorAll('.nav .nav-link');

navLinks.forEach(link => {
    const linkUrl = link.getAttribute('href');
    if (currentUrl === linkUrl) {
        link.classList.add('active');
    }
});
