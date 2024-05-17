// JS for pagination from database
function updateRowsPerPage() {
    var selectedRowsPerPage = document.getElementById("maxRows").value;
    var currentUrl = window.location.href;
    var newUrl;

    // Check if the URL already contains 'rows_per_page' parameter
    if (currentUrl.includes('rows_per_page=')) {
        // Update the 'rows_per_page' parameter value in the URL
        newUrl = currentUrl.replace(/rows_per_page=\d+/, 'rows_per_page=' + selectedRowsPerPage);
    } else {
        // Append 'rows_per_page' parameter to the URL
        var separator = currentUrl.includes('?') ? '&' : '?';
        newUrl = currentUrl + separator + 'rows_per_page=' + selectedRowsPerPage;
    }

    // Navigate to the new URL
    window.location.href = newUrl;
}

// sorting table rows
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
