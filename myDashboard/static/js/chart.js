// Create a tag cloud
const tagCloudData = JSON.parse(document.getElementById('tag_cloud').textContent);

// Check if tags are available to create cloud graph
if (tagCloudData!=null){
    const list = [];
    for (const i in tagCloudData) {
        list.push([i,tagCloudData[i] ]);
    }

    WordCloud(document.getElementById('word_cloud'), {
        list: list,
        weightFactor: 25,
        fontFamily: 'Arial, sans-serif',
        color: 'random-dark',
        rotateRatio: 0.4,
        gridSize: 15,
        shuffle: true,
        minSize: 15,
        maxWords: 40,
    });
}

// Function to handle word hover event
function handleWordHover(event) {
    const word = event.target.getAttribute('data-word');
    event.target.setAttribute('title', word);
}

// Add event listeners to each word in the word cloud
const wordCloudElements = document.querySelectorAll('.wordcloud-word');
wordCloudElements.forEach((element) => {
    element.addEventListener('mouseover', handleWordHover);
    element.addEventListener('mouseout', () => {
        element.removeAttribute('title');
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
            const color = button.dataset.color; 
            document.documentElement.style.setProperty('--selected-color', color);
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


    // Remove the 'chart-container-expanded' class if the table-container exists
    const chartTableContainer = document.querySelector('.chart-table-container');
    const tableContainer = document.getElementById('tableContainer');

    // Check if the table container exists
    if (tableContainer || section==='sentiment') {
        chartTableContainer.style.justifyContent = 'center';
    } else {
        chartTableContainer.style.justifyContent = 'initial';
    }



    // Create graph
    chartInstance = new Chart(ctx, getGraphSettings(section, data))
}

function renderTable(section) {
    const table = document.createElement('table');
    table.id = 'dataTable';
    const data = datasets[section];
    const tableContainer = document.getElementById('tableContainer');
    
  
    if (section === 'sentiment') {
            tableContainer.remove();
        
    } else {
        if (!tableContainer && section != "sentiment") {
            // If the table container does not exist, create it and append it to the parent container
            const parentContainer = document.querySelector('.chart-table-container');
            const newTableContainer = document.createElement('div');
            newTableContainer.className = 'table-container';
            newTableContainer.id = 'tableContainer';
            newTableContainer.appendChild(getTableSettings(table, section, data));
            parentContainer.appendChild(newTableContainer);
        } else {
            // If the table container exists, just update its content
            tableContainer.innerHTML = ''; // Clear existing content
            tableContainer.appendChild(getTableSettings(table, section, data)); // Append the new table
        }
        adjustContainerSize()
    }
}



function getTableSettings(table, section, data){

    if (section==='length'){
        
        const minData = Math.min(...data);
        const maxData = Math.max(...data);
        const binCount = Math.ceil(Math.sqrt(data.length)); 
        const binWidth = Math.ceil((maxData - minData) / binCount); // Round up the bin width

        const bins = Array(binCount).fill(0);

        data.forEach((value) => {
            const binIndex = Math.floor((value - minData) / binWidth);
            if (binIndex >= 0 && binIndex < binCount) {
                bins[binIndex]++;
            }
        });

        const binLabels = [];
        for (let i = 0; i < binCount; i++) {
            const lower = minData + i * binWidth;
            const upper = minData + (i + 1) * binWidth;
            binLabels.push(`${lower} - ${upper}`);
        }

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
        for (let i = 0; i < binCount; i++) {
            const row = document.createElement('tr');
            const labelCell = document.createElement('td');
            labelCell.textContent = `${binLabels[i]}`;
            const countCell = document.createElement('td');
            countCell.textContent = bins[i];
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
    }
}

function getGraphSettings(section, data){
    if (section === 'length'){
       // Create histogram data
        const values = Object.values(data);
        const minData = Math.min(...values);
        const maxData = Math.max(...values);
        const binCount = Math.ceil(Math.sqrt(values.length)); 
        const binWidth = Math.ceil((maxData - minData) / binCount); // Round up the bin width

        const bins = Array(binCount).fill(0);

        data.forEach((value) => {
            const binIndex = Math.floor((value - minData) / binWidth);
            if (binIndex >= 0 && binIndex < binCount) {
                bins[binIndex]++;
            }
        });

        const binLabels = [];
        for (let i = 0; i < binCount; i++) {
            const lower = minData + i * binWidth;
            const upper = minData + (i + 1) * binWidth;
            binLabels.push(`${lower} - ${upper}`);
        }


        const graphSettings = {
            type: 'bar',
            data: {
                labels: binLabels,
                datasets: [{
                    label: "Distribution of Comment lengths",
                    data: bins,
                    backgroundColor: "#87CEEB",
                    barPercentage: 1.0, 
                    categoryPercentage: 1.0, 
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true, 
                        },
                    }],
                },
            },
        };

        return graphSettings

    } else if(section === 'frequency'){
        const graphSettings = {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Top '+Object.keys(data).length.toString()+' most frequent words',
                    data: Object.values(data),
                    backgroundColor: "#9370DB",
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
                            stepSize: 1,
                            labelString: 'Count'

                        },
                    }],
                },
            }
        }
        return graphSettings

    } else {
// Convert the data to the required format
        data = datasets[section]
        const roundedData = Object.values(data).map(value => parseFloat(value.toFixed(1)));
        
        const graphSettings = {
                type: 'pie',
                data: {
                    labels: Object.keys(data),
                    datasets: [{
                        data: roundedData,
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
            }
        return graphSettings
    }
};

// Function to dynamically adjust the container size based on the table size
function adjustContainerSize() {
    const container = document.getElementById('tableContainer');
    const table = document.getElementById('dataTable');
    
    // Get the width and height of the table, including the borders and padding
    // Add 10 to the height to prevent y-axis overflow
    const tableWidth = table.offsetWidth;
    const tableHeight = table.offsetHeight + 15;
    
    // Set the container width and height based on the table size
    container.style.width = tableWidth + 'px';
    container.style.height = tableHeight + 'px';
  }

// Initial rendering on page load
// Render the initial table on page load
renderTable('length');
// Render the initial graph on page load
renderGraph('length');
// Render initial button
updateSelectedButton('length');



let scatterInstance = null

function updateScatterPlot() {
    // Get the canvas element and context
    var canvas = document.getElementById('scatterGraph');
    var sac = canvas.getContext('2d');

    // Retrieve activity data and adjust format
    const data = datasets['activity'];

    // Get the dropdown element
    var dropdown = document.getElementById("x-axis-option");

    const activityData = Object.entries(data[dropdown.value]).map(([date, count]) => ({ x: date, y: count }));

    const maxCount = activityData.reduce((max, dataPoint) => {
        return Math.max(max, dataPoint.y);
    }, 0);

    // Clear the canvas and all event listeners
    canvas.width  = 400;
    canvas.height = 400; 
    sac.clearRect(0, 0, canvas.width, canvas.height);

    // ScatterChart settings
    if (scatterInstance) {
        scatterInstance.destroy(); // Clear previous chart and event listeners
    }

    scatterInstance = new Chart(sac, {
        type: 'line', 
        data: {
            datasets: [{
                label: 'Comments Published per ' + dropdown.value,
                data: activityData,
                backgroundColor: "rgba(255, 165, 0, 0.2)", 
                borderColor: "#FFA509",
                pointBackgroundColor: "#FFA509",
                pointBorderColor: 'rgba(255, 255, 255, 1)',
                pointRadius: 5,
                fill: true, 
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            height: 350,

            scales: {
                xAxes: [{
                    type: 'category', // Use 'category' for x-axis with month names
                    labels: activityData.map(item => item.x), // Provide the x-axis labels (month names)
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true, // Set the y-axis to start from zero
                        suggestedMax: maxCount+1,
                        stepSize: 2,
                    },
                }],
            },
        },
    });
}


updateScatterPlot();












