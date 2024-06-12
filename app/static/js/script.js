
// JavaScript to handle active class based on current URL
const currentUrl = window.location.pathname;
const navLinks = document.querySelectorAll('.nav .nav-link');

navLinks.forEach(link => {
    const linkUrl = link.getAttribute('href');
    if (currentUrl === linkUrl) {
        link.classList.add('active');
    }
});

// auto close flash message - js
document.addEventListener('DOMContentLoaded', function () {
    // Select all alerts
    var alerts = document.querySelectorAll('.alert');
    // Set timeout to hide each alert after 5 seconds (5000 ms)
    alerts.forEach(function (alert) {
      setTimeout(function () {
        alert.classList.remove('show');
        alert.classList.add('fade');
        setTimeout(function() {
          alert.remove();
        }, 150); // Wait for fade transition to complete before removing the element
      }, 5000); // 5000 ms = 5 seconds
    });
  });