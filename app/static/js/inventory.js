

function confirmDelete(itemId) {
  if (confirm("Are you sure you want to delete this item?")) {
    // If user confirms, redirect to delete route
    window.location.href = "/deleteInventoryItem/" + itemId;
  } else {
    // If user cancels, do nothing
    event.preventDefault();
  }
}

// adding input field to add more categories in one button click
function addField() {
  const dynamicFields = document.getElementById("dynamicFields");
  const inputCount = dynamicFields.children.length;
  const newField = document.createElement("div");
  newField.classList.add("form-group", "input-group", "mb-3");
  newField.innerHTML = `
        <input type="text" class="form-control" name="name[]" id="name${inputCount}" placeholder="Category Name ${
    inputCount + 2
  }" required>
        <div class="input-group-append">
            <button type="button" class="btn btn-danger mt-0" onclick="removeField(this)">
                <i class="fas fa-minus"></i>
            </button>
        </div>
    `;
  dynamicFields.appendChild(newField);
}

function removeField(button) {
  button.closest(".form-group").remove();
}

// js - to edit category on the table row
function editCategory(categoryId) {
  const row = document.getElementById("category-" + categoryId);
  row.querySelector(".category-name").style.display = "none";
  row.querySelector(".category-input").style.display = "inline-block";
  row.querySelector(".btn-edit").style.display = "none";
  row.querySelector(".btn-save").style.display = "inline-block";
  row.querySelector(".btn-x").style.display = "inline-block";
}

function saveCategory(categoryId) {
  const row = document.getElementById("category-" + categoryId);
  const newName = row.querySelector(".category-input").value;

  fetch(`/update_category/${categoryId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: newName }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        row.querySelector(".category-name").textContent = newName;
        cancelEdit(categoryId);
      } else {
        alert("Error updating category");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function cancelEdit(categoryId) {
  const row = document.getElementById("category-" + categoryId);
  row.querySelector(".category-name").style.display = "inline";
  row.querySelector(".category-input").style.display = "none";
  row.querySelector(".btn-edit").style.display = "inline-block";
  row.querySelector(".btn-save").style.display = "none";
  row.querySelector(".btn-x").style.display = "none";
}

function updateRowsPerPage() {
  var prodRowsPerPage = document.getElementById("prodMaxRows").value;
  var catRowsPerPage = document.getElementById("catMaxRows").value;

  var url = new URL(window.location.href);
  url.searchParams.set("prod_rows_per_page", prodRowsPerPage);
  url.searchParams.set("cat_rows_per_page", catRowsPerPage);
  url.searchParams.set("prod_page", 1); // Reset to first page for products
  url.searchParams.set("cat_page", 1); // Reset to first page for categories

  window.location.href = url.href;
}
document.addEventListener("DOMContentLoaded", function () {
  // Retrieve active tab from local storage
  var activeTab = localStorage.getItem("activeTab");
  if (activeTab) {
    showTab(activeTab);
  }

  // Add event listener to tab buttons
  var tabButtons = document.querySelectorAll(".nav-link");
  tabButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var tabId = this.getAttribute("aria-controls");
      showTab(tabId);
      // Store active tab in local storage
      localStorage.setItem("activeTab", tabId);
    });
  });
});

function showTab(tabId) {
  // Get all tabs and hide them
  var tabs = document.querySelectorAll(".tab-pane");
  tabs.forEach(function (tab) {
    tab.classList.remove("show", "active");
  });

  // Get all tab buttons and deactivate them
  var tabButtons = document.querySelectorAll(".nav-link");
  tabButtons.forEach(function (button) {
    button.classList.remove("active");
  });

  // Show the selected tab and activate its button
  document.getElementById(tabId).classList.add("show", "active");
  document.getElementById(tabId + "-tab").classList.add("active");
}
