// JavaScript function to handle multi-step registration form
function handleMultiStepForm(nextButtonClass, previousButtonClass, submitButtonClass, progressBarId) {
    let fieldsets = document.querySelectorAll("fieldset");
    let nextButtons = document.querySelectorAll("." + nextButtonClass);
    let previousButtons = document.querySelectorAll("." + previousButtonClass);
    let submitButtons = document.querySelectorAll("." + submitButtonClass);
    let progressBarLi = document.querySelectorAll("#" + progressBarId + " li");

    // Event listener for next buttons
    nextButtons.forEach(nextButton => {
        nextButton.addEventListener("click", function() {
            let current_fs = this.parentNode;
            let next_fs = this.parentNode.nextElementSibling;
            
            // Check if the current fieldset has any required inputs that are empty
            if (!checkEmptyInputs(current_fs)) {
                console.log("Required input is empty!");
                return; // If any required input is empty, do not proceed
            } else {
                console.log("All required inputs are filled.");
            }
            
            // Activate next step on progressbar using the index of next_fs
            progressBarLi[Array.from(fieldsets).indexOf(next_fs)].classList.add("active");
            
            // Hide the current fieldset
            current_fs.style.display = "none";
            
            // Show the next fieldset
            next_fs.style.display = "block"; 
        });
    });

    // Event listener for previous buttons
    previousButtons.forEach(previousButton => {
        previousButton.addEventListener("click", function() {
            let current_fs = this.parentNode;
            let previous_fs = this.parentNode.previousElementSibling;
            
            // Activate previous step on progressbar using the index of current_fs
            progressBarLi[Array.from(fieldsets).indexOf(current_fs)].classList.remove("active");
            
            // Hide the current fieldset
            current_fs.style.display = "none";
            
            // Show the previous fieldset
            previous_fs.style.display = "block"; 
        });
    });

    // Event listener for submit buttons
    submitButtons.forEach(submitButton => {
        submitButton.addEventListener("click", function() {
            return false;
        });
    });
}

// Call the function with the appropriate parameters
handleMultiStepForm("next", "previous", "submit", "progressbar");


// Javascript function to check empty inputs
function checkEmptyInputs(fieldset) {
    let inputs = fieldset.querySelectorAll("input[required], select[required], textarea[required]");
    
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].value.trim() === "") {
            // Display error message
            inputs[i].insertAdjacentHTML('afterend', '<div class="error-message float-end" style="color:red;">Please fill the required field!</div>');
            document.getElementById('emailError').textContent = "";
            return false; // Stop checking further inputs
        } else {
            // Remove error message if exists
            let errorMessage = inputs[i].nextElementSibling;
            if (errorMessage && errorMessage.classList.contains('error-message')) {
                errorMessage.remove();
            }
        }
    }
    return true; // All required inputs are filled
}

//<!-- javascript to handle the login and register form in the same page -->
document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.querySelector(".register-form");
    const loginForm = document.querySelector("#login-form");

    const registerButton = document.querySelector(".register");
    const loginButton = document.querySelector(".login");
    
    // Function to hide the login form and show the register form
    function showRegisterForm() {
        registerForm.classList.remove("hidden");
        document.title = "Register new user";
        loginForm.classList.add("hidden");
    }

    // Function to hide the register form and show the login form
    function showLoginForm() {
        loginForm.classList.remove("hidden");
        document.title = "Sign in to Medem"; // update the title of each form
        registerForm.classList.add("hidden");
    }

    // Add click event listeners to the register and login buttons
    registerButton.addEventListener("click", showRegisterForm);
    loginButton.addEventListener("click", showLoginForm);
});

// JavaScript function to check and validate the email address already registered using AJAX
function validateEmail(emailInputId, emailErrorId, nextButtonId) {
    var emailInput = document.getElementById(emailInputId);
    var emailError = document.getElementById(emailErrorId);
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var nextButton = document.getElementById(nextButtonId);
  
    emailInput.addEventListener('input', function() {
        var email = this.value;
  
        if (emailRegex.test(email)) {
            // Send an AJAX request to check if the email exists
            fetch('/check_email?email=' + encodeURIComponent(email))
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        // Disable submit button if validation fails
                        nextButton.setAttribute("disabled", "disabled");
                        emailError.textContent = "Email already registered! Please reset your password or use a different email.";
                       
                    } else {
                        emailError.textContent = "";
                        nextButton.disabled = false;
                    }
                });
        } else {
            emailError.textContent = "Please enter a valid email address.";
            // Disable submit button by default
            document.getElementById("next").setAttribute("disabled", "disabled");
        }
    });
  }
  
  // Call the function with the appropriate IDs
  validateEmail('emailInput', 'emailError', 'next');
  

// hide/show password - js
function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const togglePassword = document.querySelector('.toggle-password');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        togglePassword.textContent = '🙈'; // Hide icon
    } else {
        passwordInput.type = 'password';
        togglePassword.textContent = '👁️'; // Show icon
    }
    }