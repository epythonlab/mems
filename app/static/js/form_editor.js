// <!-- JavaScript to enable form editing -->

    function enableEdit(section) {
        // Get the input fields within the specified section
        const inputs = document.querySelectorAll(`#${section}Form input`);
        

        // Enable all input fields in the section
        inputs.forEach(input => {
            input.removeAttribute('readonly');
            input.classList.remove('read-only-input');
        });

        // Show the save button and hide the edit button in the section
        document.getElementById(`saveButton${capitalizeFirstLetter(section)}`).style.display = 'block';
        document.getElementById(`editButton${capitalizeFirstLetter(section)}`).style.display = 'none';
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

