// <!-- JavaScript to enable form editing -->

    function enableEdit(section) {
        // Get the input fields within the specified section
        const inputs = document.querySelectorAll(`#${section}Form input`);
        

        // Enable all input fields in the section
        inputs.forEach(input => {
            input.removeAttribute('readonly');
            input.classList.remove('read-only-input');
        });

        // Show the save and cancel buttons, hide the edit button
    document.getElementById(`saveButton${capitalizeFirstLetter(section)}`).style.display = 'block';
    document.getElementById(`cancelButton${capitalizeFirstLetter(section)}`).style.display = 'block';
    document.getElementById(`editButton${capitalizeFirstLetter(section)}`).style.display = 'none';
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    function cancelForm(section) {
        // Get the input fields within the specified section
        const inputs = document.querySelectorAll(`#${section}Form input`);
    
        // Restore original values and make inputs read-only
        inputs.forEach(input => {
            input.setAttribute('readonly', 'readonly');
            input.classList.add('read-only-input');
        });
    
        // Hide the save and cancel buttons, show the edit button
        document.getElementById(`saveButton${capitalizeFirstLetter(section)}`).style.display = 'none';
        document.getElementById(`cancelButton${capitalizeFirstLetter(section)}`).style.display = 'none';
        document.getElementById(`editButton${capitalizeFirstLetter(section)}`).style.display = 'block';
    }