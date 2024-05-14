// JavaScript to handle active class based on current URL
function setActiveNavLink() {
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav .nav-link');

    navLinks.forEach(link => {
        const linkUrl = link.getAttribute('href');
        if (currentUrl === linkUrl) {
            link.classList.add('active');
        }
    });
}

// JavaScript for overlay details of the data row
function setupOverlay() {
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
}

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

// JS for password validation
function setupPasswordValidation() {
    document.addEventListener("DOMContentLoaded", function() {
        // Add event listeners to input fields
        document.getElementById("new_password").addEventListener("input", validatePassword);
        document.getElementById("confirm_pass").addEventListener("input", validatePassword);
        // Disable submit button by default (outside the event listener)
        document.getElementById("submit_button").setAttribute("disabled", "disabled");
    });
}

// Function to validate password and enable/disable submit button
function validatePassword() {
    // Get input values
    var password = document.getElementById("new_password").value;
    var confirmPassword = document.getElementById("confirm_pass").value;
 
    // Regular expression pattern for password validation
    var passwordPattern = /^(?=.*\d)(?=.*[a-zA-Z])(?=.*[^\w\d\s:])([^\s]){8,}$/;
 
    // Get DOM elements
    var submitButton = document.getElementById("submit_button");
    var passwordIcon = document.getElementById("password_icon");
    var confirmPasswordIcon = document.getElementById("confirm_password_icon");
    var passwordConfirmationError = document.getElementById("password_confirmation_error");
 
    // Check if passwords match
    var arePasswordsMatching = password === confirmPassword;
 
    // Display tick marks or X marks based on validation result
    passwordIcon.innerHTML = password.match(passwordPattern) ? "<i class='fas fa-check text-success'></i>" : "<i class='fas fa-times text-danger'></i>";
    confirmPasswordIcon.innerHTML = arePasswordsMatching ? "<i class='fas fa-check text-success'></i>" : "<i class='fas fa-times text-danger'></i>";
 
    // Clear error message if validation passes
    passwordConfirmationError.innerText = "";
 
    // Check if passwords match and meet pattern requirements
    if (!arePasswordsMatching) {
      passwordConfirmationError.innerText = "Passwords do not match.";
    } else if (!password.match(passwordPattern)) {
      passwordConfirmationError.innerText = "Password must contain at least 8 characters, one letter, one number, and one special character.";
    } else {
      // Enable submit button if validation passes
      submitButton.removeAttribute("disabled");
      return;
    }
 
    // Disable submit button if validation fails
    submitButton.setAttribute("disabled", "disabled");
}

// JS for table sorting
function setupTableSorting() {
    document.addEventListener('DOMContentLoaded', function() {
        const sortableHeaders = document.querySelectorAll('.sortable');
        
        sortableHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const column = header.cellIndex;
                const sortOrder = header.classList.contains('sorted-asc') ? 'desc' : 'asc';
                
                clearSortIndicators();
                sortTable(column, sortOrder);
                
                header.classList.toggle('sorted-asc', sortOrder === 'asc');
                header.classList.toggle('sorted-desc', sortOrder === 'desc');
            });
        });
    });
}

function clearSortIndicators() {
    document.querySelectorAll('.sortable').forEach(header => {
        header.classList.remove('sorted-asc', 'sorted-desc');
    });
}

function sortTable(column, sortOrder) {
      // Get the table body and all rows in the table
  const tbody = document.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));

  // Sort the rows based on the content of the specified column
  rows.sort((a, b) => {
      // Extract the text content of the cells in the specified column, handling cases where cells might be undefined
      const aValue = (a.cells[column] && a.cells[column].textContent.trim()) || '';
      const bValue = (b.cells[column] && b.cells[column].textContent.trim()) || '';

      // Compare the values based on the specified sort order (asc or desc)
      if (sortOrder === 'asc') {
          return aValue.localeCompare(bValue);
      } else {
          return bValue.localeCompare(aValue);
      }
  });

  // Reorder the rows in the table based on the sorted array
  rows.forEach(row => tbody.appendChild(row));
}
}

// JS for pagination
function updateRowsPerPage() {
    // Your pagination logic here...
    var selectedRowsPerPage = document.getElementById("maxRows").value;
  var currentUrl = window.location.href;
  var newUrl;

  // Check if the URL already contains 'state' parameter
  if (currentUrl.includes('state=')) {
      // Update the 'state' parameter value in the URL
      newUrl = currentUrl.replace(/state=\d+/, 'state=' + selectedRowsPerPage);
  } else {
      // Append 'state' parameter to the URL
      var separator = currentUrl.includes('?') ? '&' : '?';
      newUrl = currentUrl + separator + 'state=' + selectedRowsPerPage;
  }

  // Navigate to the new URL
  window.location.href = newUrl;
}

// JS for view and close buttons
function setupViewCloseButtons() {
    document.getElementById('view-btn').addEventListener('click', function() {
        document.getElementById('detail-page').style.right = '0';
    });

    document.getElementById('close-btn').addEventListener('click', function() {
        document.getElementById('detail-page').style.right = '-100%';
    });
}

// Call functions to initialize different modules
document.addEventListener('DOMContentLoaded', function() {
    setActiveNavLink();
    setupOverlay();
    setupPasswordValidation();
    setupTableSorting();
    setupViewCloseButtons();
});
