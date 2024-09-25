const search = document.querySelector('#search');
const appTable = document.querySelector('.app-table');
const outputTable = document.querySelector('.table-output');
const pagination = document.querySelector('.pagination-container');
const tableBody = document.querySelector('.table-body');

// Hide the output table by default.
outputTable.style.display = 'none';
appTable.style.display = 'block';

// Event listener for the search input
search.addEventListener('keyup', (event) => {
    const data = event.target.value.trim(); // Trim whitespace

    if (searhValue.length > 0) {
        appTable.style.display = 'none'; // Hide the main table
        pagination.style.display = 'none'; // Hide pagination
        outputTable.style.display = 'block'; // Show search results

        // Send the search request to the backend
        fetch('/income/search-income', {
            body: JSON.stringify({ data: data }),
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="4">No matching results found.</td></tr>'; // Show no results
            } else {
                tableBody.innerHTML = ''; // Clear previous results
                data.forEach(income => {
                    tableBody.innerHTML += `
                        <tr>
                            <td>${income.amount}</td>
                            <td>${income.source}</td>
                            <td>${income.description}</td>
                            <td>${income.date}</td>
                        </tr>
                    `;
                });
            }
        })
        .catch((error) => {
            console.error('Error fetching data:', error); // Handle errors
        });

    } else {
        // If search input is cleared, restore the default table
        appTable.style.display = 'block'; // Show original table
        pagination.style.display = 'block'; // Show pagination
        outputTable.style.display = 'none'; // Hide search results

        // Optionally: Fetch all data again (if needed)
        fetch('/income/search-income', {
            body: JSON.stringify({ data: '' }), // Send empty search value to reload all
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then((response) => response.json())
        .then((data) => {
            tableBody.innerHTML = ''; // Clear previous results
            data.forEach(income => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${income.amount}</td>
                        <td>${income.source}</td>
                        <td>${income.description}</td>
                        <td>${income.date}</td>
                    </tr>
                `;
            });
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        });
    }
});
