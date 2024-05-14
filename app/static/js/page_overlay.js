
// js for overlay details of the data row
document.querySelectorAll('.open-detail-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        var rowId = this.getAttribute('data-row-id'); // Get the ID from the button's data attribute
        document.getElementById('overlay').style.display = 'flex';
        loadForm(rowId); // Pass the ID to the loadForm function
    });
  });
  
  document.getElementById('overlay').addEventListener('click', function(event) {
    if (event.target === this) {
        closeForm();
    }
  });
  
  document.getElementById('close-form-btn').addEventListener('click', function() {
    closeForm();
  });
  
  function loadForm(rowId) {
    fetch('/user_detail?id=' + rowId) // Pass the ID as a query parameter
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
  // end of the js for overlay page content
  