
const renderCharts = (data, labels) => {
    var ctx = document.getElementById('myPieChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Last one week expense',
                data: data,
                backgroundColor: [
                    '#FFB3B3', // Light Red
                    '#FFCC99', // Light Orange
                    '#FFFF99', // Light Yellow
                    '#CCFFCC', // Light Green
                    '#99CCFF', // Light Blue
                    '#D1B3FF', // Light Purple
                    '#FFB3FF', // Light Pink
                    '#FF6666', // Light Salmon
                    '#B3E0FF', // Pale Blue
                    '#D9F2D9'  // Light Mint
                ],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Weekly Expense per Category'
            },
            legend: {
                position: 'bottom'
            }
        }
    });
};

const getChartData = () => {
    fetch('/expense_week')
        .then(res => res.json())
        .then(results => {
            const category_data = results.expense_category_data;
            const labels = Object.keys(category_data);
            const data = Object.values(category_data);
            renderCharts(data, labels);
        })
        .catch(err => console.log("Error fetching chart data:", err));
};

document.addEventListener("DOMContentLoaded", getChartData);
