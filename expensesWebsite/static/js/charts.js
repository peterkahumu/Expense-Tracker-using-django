const renderChart = (data, labels) => {
   const config = {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: "Expenses per category for the last six months",
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)', 
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)', 
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)', 
                    'rgba(201, 203, 207, 0.6)',
                ],
                
                borderColor: [
                    'rgba(255, 99, 132, 0.6)', 
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)', 
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)', 
                    'rgba(201, 203, 207, 0.6)',
                ],
                
                
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Expenses Per Category",
                }
            }
        }
    };

    var canvas = document.getElementById('expensesChart').getContext('2d');
    const myChart = new Chart(canvas, config);
}

const getChartData = () => {
    fetch('expense-summary')
    .then((response) => response.json())
    .then((data) => {
        const category_data = data.Expense_category;
        const [values, labels] = [Object.values(category_data), Object.keys(category_data)];

        renderChart(values, labels);
    })
}

document.onload = getChartData();