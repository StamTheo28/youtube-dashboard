document.addEventListener('DOMContentLoaded', function() {
    // Create Sentiment Pie Chart
    var ctx = document.getElementById('sentimentPieChart').getContext('2d');
    const mydata = JSON.parse(document.getElementById('sentiment_percentages').textContent);
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(mydata),
            datasets: [{
                data: Object.values(mydata),
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(255, 99, 132, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Percentages of Comment Sentiments',
                fontSize: 18,
                fontColor: '#000000',
                fontStyle: 'bold'
            },
        tooltips: {
            callbacks: {
                label: function (tooltipItem, data) {
                    const dataset = data.datasets[tooltipItem.datasetIndex];
                    const currentValue = dataset.data[tooltipItem.index];
                    return `${data.labels[tooltipItem.index]}: ${currentValue}%`;
                    },
            },
        },
        }
    });

});


// Container for section graphs
const datasets = JSON.parse(document.getElementById('section_data').textContent);
let chartInstance = null;

function handleGraphButtonClick(section) {
    updateSelectedButton(section);

    // Remove the existing graph and table
    removeGraph();
    removeTable();

    // Render the graph and table for the selected dataset
    renderGraph(section);
    renderTable(section);
}

function updateSelectedButton(section) {
    const buttons = document.querySelectorAll('.section-button');
    buttons.forEach((button) => {
        if (button.dataset.name === section) {
            button.classList.add('selected');
        } else {
            button.classList.remove('selected');
        }
    });
}

function removeGraph() {
    if (chartInstance) {
        chartInstance.destroy();
    }
}

function removeTable() {
    const existingTable = document.getElementById('dataTable');
    if (existingTable) {
        existingTable.remove();
    }
}

function renderGraph(section) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const data = datasets[section];
    // Create graph
    chartInstance = new Chart(ctx, getGraphSettings(section, data))
}

function renderTable(section) {
    const table = document.createElement('table');
    table.id = 'dataTable';
    removeTable()
    const data = datasets[section];
    const tableContainer = document.getElementById('tableContainer');

     

    tableContainer.appendChild(getTableSettings(table, section, data));
}

function getTableSettings(table, section, data){

    if (section==='length'){
        
        const min = Math.min(...data);
        const max = Math.max(...data);
        const numRanges = Math.ceil(Math.sqrt(data.length)); 
        
        const intervalWidth = (max - min) / numRanges;
        const counts = new Array(numRanges).fill(0);

        // Count how many data points fall into each interval
        data.forEach((length) => {
            const intervalIndex = Math.ceil((length - min) / intervalWidth);
            counts[intervalIndex]++;
        });

        // Create the table and its header row
        const headerRow = document.createElement('tr');
        const headerCellRange = document.createElement('th');
        headerCellRange.textContent = 'Range';
        const headerCellCount = document.createElement('th');
        headerCellCount.textContent = 'Count';
        headerRow.appendChild(headerCellRange);
        headerRow.appendChild(headerCellCount);
        table.appendChild(headerRow);

        // Add table data rows for each interval
        for (let i = 0; i < numRanges; i++) {
            const row = document.createElement('tr');
            const rangeStart = min + i * intervalWidth;
            const rangeEnd = min + (i + 1) * intervalWidth - 1;
            const labelCell = document.createElement('td');
            labelCell.textContent = `${rangeStart} - ${rangeEnd}`;
            const countCell = document.createElement('td');
            countCell.textContent = counts[i];
            row.appendChild(labelCell);
            row.appendChild(countCell);
            table.appendChild(row);
        }
        return table
    } else if (section==='frequency'){
        // Create the table and its header row
        const headerRow = document.createElement('tr');
        const headerCellLabel = document.createElement('th');
        headerCellLabel.textContent = 'Word';
        const headerCellCount = document.createElement('th');
        headerCellCount.textContent = 'Count';
        headerRow.appendChild(headerCellLabel);
        headerRow.appendChild(headerCellCount);
        table.appendChild(headerRow);

        // Add table data rows
        for (const label in data) {
            const row = document.createElement('tr');
            const labelCell = document.createElement('td');
            labelCell.textContent = label;
            const countCell = document.createElement('td');
            countCell.textContent = data[label];
            row.appendChild(labelCell);
            row.appendChild(countCell);
            table.appendChild(row);
        }
        return table
    } else {
         // Create the table and its header row
         const headerRow = document.createElement('tr');
         const headerCellLabel = document.createElement('th');
         headerCellLabel.textContent = 'Emoji';
         const headerCellCount = document.createElement('th');
         headerCellCount.textContent = 'Count';
         headerRow.appendChild(headerCellLabel);
         headerRow.appendChild(headerCellCount);
         table.appendChild(headerRow);
 
         // Add table data rows
         for (const label in data) {
             const row = document.createElement('tr');
             const labelCell = document.createElement('td');
             labelCell.textContent = label;
             const countCell = document.createElement('td');
             countCell.textContent = data[label];
             row.appendChild(labelCell);
             row.appendChild(countCell);
             table.appendChild(row);
         }
         return table
    }
}

function getGraphSettings(section, data){
    if (section === 'length'){
        // Create histogram data
        const values = Object.values(data)
        
        const minData = Math.min(...values);
        const maxData = Math.max(...values);
        const binCount = Math.ceil(Math.sqrt(values.length)); 
        console.log(binCount)
        const binWidth = (maxData - minData) / binCount;

        const bins = Array(binCount).fill(0);

        data.forEach((value) => {
            const binIndex = Math.floor((value - minData) / binWidth);
            if (binIndex >= 0 && binIndex < binCount) {
                bins[binIndex]++;
            }
        });

        const binLabels = [];
        for (let i = 0; i < binCount; i++) {
            binLabels.push(`${minData + i * binWidth} - ${minData + (i + 1) * binWidth}`);
        }


        const graphSettings =  {
            type: 'bar',
            data: {
                labels: binLabels,
                datasets: [{
                    data: bins,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    barPercentage: 1.0, 
                    categoryPercentage: 1.0, 
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                    },
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        }
        return graphSettings

    } else if(section === 'frequency'){
        const graphSettings = {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Data',
                    data: Object.values(data),
                    backgroundColor: 'rgba(54, 170, 235, 0.6)',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    xAxes: [{
                        gridLines: {
                            display: false,
                        },
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true, // Set the y-axis to start from zero
                        },
                    }],
                },
            }
        }
        return graphSettings

    } else {

        const scatterData = Object.entries(data).map(([emoji, count]) => ({ x: count, y: count, r: 10, emoji: emoji }));

        const graphSettings = {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Emoji Counts',
                    data: scatterData,
                    backgroundColor: 'rgba(54, 200, 235, 0.6)',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Emoji Count',
                        },
                    },
                    y: {
                        type: 'linear',
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Emoji Count',
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: false // Hide legend as we are using custom emojis
                    },
                    datalabels: {
                        align: 'center',
                        anchor: 'center',
                        color: 'black',
                        font: {
                            size: 16, // Set label font size
                        },
                        formatter: function(value, context) {
                            // Use the emoji as the label content
                            return context.dataset.data[context.dataIndex].emoji;
                        },
                        // Custom draw function to place emojis at the data point coordinates
                        draw: function(context) {
                            const dataPoint = context.dataPoint;
                            const emoji = dataPoint.emoji;
                            const fontSize = 16;
                            const x = dataPoint.x;
                            const y = dataPoint.y;
        
                            context.ctx.font = fontSize + 'px Arial';
                            context.ctx.textAlign = 'center';
                            context.ctx.textBaseline = 'middle';
                            context.ctx.fillText(emoji, x, y);
                        }
                    }
                }
            }
        };
        return graphSettings
    }
};

// Initial rendering on page load
// Render the initial table on page load
renderTable('length');
// Render the initial graph on page load
renderGraph('length');
// Render initial button
updateSelectedButton('length');

