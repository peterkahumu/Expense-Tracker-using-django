const search = document.querySelector('#search');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const pagination = document.querySelector('.pagination-container');
const tableBody = document.querySelector('.table-body');

tableOutput.style.display = 'none'; // the table is hidden by default.


search.addEventListener('keyup', (event) => {

    const data = event.target.value;

    if (data.trim().length > 0){
        tableBody.innerHTML = "";
        fetch('/search', {
            body: JSON.stringify({data: data}),
            method: 'POST', 
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('data', data);

            appTable.style.display = 'none';
            pagination.style.display = 'none';
            tableOutput.style.display = 'block';

            if (data.length === 0){
                tableOutput.innerHTML = '<p>No result found.</p>'
            } else {
                data.forEach(element => {
                    tableBody.innerHTML += `
                    <tr>
                        <td>${element.amount}</td>
                        <td>${element.category}</td>
                        <td>${element.description}</td>
                        <td>${element.date}</td>

                    </tr>
                    `;
                });
            }
        });
    } else {
        appTable.style.display = 'block';
        pagination.style.display = 'block';
        tableOutput.style.display = 'none';
    }
})