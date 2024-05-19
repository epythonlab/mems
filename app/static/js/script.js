
// JavaScript to handle active class based on current URL
const currentUrl = window.location.pathname;
const navLinks = document.querySelectorAll('.nav .nav-link');

navLinks.forEach(link => {
    const linkUrl = link.getAttribute('href');
    if (currentUrl === linkUrl) {
        link.classList.add('active');
    }
});

// js for searching 
document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.getElementById('search');
  const suggestions = document.getElementById('suggestions');
  
  searchInput.addEventListener('input', function() {
    const query = searchInput.value.toLowerCase();
    if (query.length === 0) {
      suggestions.classList.remove('active');
      return;
    }

    fetch(`/search-suggestions?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        if (data.length > 0) {
          suggestions.innerHTML = data.map(item => `<li data-email="${item.description}">${item.name} - ${item.description} (${item.category})</li>`).join('');
          suggestions.classList.add('active');
        } else {
          suggestions.classList.remove('active');
        }
      });
  });

  suggestions.addEventListener('click', function(e) {
    if (e.target.tagName === 'LI') {
      const email = e.target.getAttribute('data-email');
      window.location.href = `/users?email=${encodeURIComponent(email)}`;
      searchInput.value = email; // Set input value to the selected email
    }
  });

  document.addEventListener('click', function(e) {
    if (!suggestions.contains(e.target) && e.target !== searchInput) {
      suggestions.classList.remove('active');
    }
  });
});

  