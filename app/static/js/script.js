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
  
  // Add event listeners to input fields
  document.getElementById("new_password").addEventListener("input", validatePassword);
  document.getElementById("confirm_pass").addEventListener("input", validatePassword);
  
  // Disable submit button by default
  document.getElementById("submit_button").setAttribute("disabled", "disabled");

//   password validation script ended up here

