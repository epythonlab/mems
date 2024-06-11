document.querySelectorAll('.open-detail-btn').forEach(function(button) {
  button.addEventListener('click', function() {
      var rowId = this.getAttribute('data-row-id'); // Get the ID from the button's data attribute
      document.getElementById('overlay').style.display = 'flex';
      var pageUrl = this.getAttribute('data-page-url'); // Get the page URL from the button's data attribute
      loadForm(pageUrl, rowId); // Pass the ID to the loadForm function
  });
});

document.getElementById('overlay').addEventListener('click', function(event) {
  if (event.target === this) {
      closeForm();
  }
});

document.getElementById('close-form-btn').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent default anchor behavior
  closeForm();
});

function loadForm(pageUrl, rowId) {
  console.log(pageUrl, rowId)
  fetch(pageUrl + '?id=' + rowId) // Pass the ID as a query parameter
  .then(response => response.text())
  .then(html => {
      document.getElementById('overlay').innerHTML = html;
      document.getElementById('detail').addEventListener('submit', function(event) {
          event.preventDefault();
          // Handle form submission here
          closeForm();
      });
  })
  .catch(error => console.error('Error loading form:', error));
}

function closeForm() {
  document.getElementById('overlay').style.display = 'none';
  document.getElementById('overlay').innerHTML = '';
}
