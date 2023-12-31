// Laoding effect listener
document.getElementById('myForm').addEventListener('submit', function () {
    // Show the loading effect
    console.log('Loading effect')
    document.getElementById('loadingEffect').style.display = 'block';
});

function random_color() {
    const letters = '0123456789ABCDEF';
    let color = '';
    do {
        color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
    } while (color === '#FFA500'); // Ensure orange (#FFA500) is not chosen
    return color;
}

// Comments Table Related Javascript
const jsonData = JSON.parse(document.getElementById('comments').textContent);
// Parse the JSON data passed from the Django view

var currentPage = 1;
var itemsPerPage = 10; // Number of items per page

// Function to initialize the paginator
function initPaginator(data) {
    var paginator = document.getElementById("paginator");
    var totalPages = Math.ceil(data.length / itemsPerPage);
    // Clear the paginator content before re-creating buttons
    paginator.innerHTML = "";

    // Create buttons for each page
    for (var i = 1; i <= totalPages; i++) {
        var button = document.createElement("button");
        button.textContent = i;
        button.addEventListener("click", function() {
        var pageNum = parseInt(this.textContent);
        displayPage(pageNum, data);
        });
        paginator.appendChild(button);
    }

    // Highlight the current page button
    var buttons = paginator.getElementsByTagName("button");
    for (var i = 0; i < buttons.length; i++) {
        if (parseInt(buttons[i].textContent) === currentPage) {
        buttons[i].classList.add("active");
        } else {
        buttons[i].classList.remove("active");
        }
    }
    console.log('Paginator created/Updated')
}

// Function to navigate to a specific page
function displayPage(pageNum, data) {
    currentPage = pageNum; // Update the current page number

    // Use the provided data if available; otherwise, use the original data
    var pageData = data || jsonData;
    var startIdx = (pageNum - 1) * itemsPerPage;
    var endIdx = startIdx + itemsPerPage;
    var pageItems = pageData.slice(startIdx, endIdx);

    var contentTableBody = document.querySelector("#content");
    contentTableBody.innerHTML = "";

    // Loop through the page items and create table rows
    pageItems.forEach(function(row) {
    var tr = document.createElement("tr");
    tr.innerHTML = `
        <td>${row.index}</td>
        <td class="comment-cell">${row.comment_id.substring(0, 10)}...<span class="comment-popup">${row.comment_id}</span></td>
        <td>${row.like_count}</td>
        <td>${row.reply_count}</td>
        <td><span class="${getClassForSentiment(row.sentiment)}">${row.sentiment}</span></td>
        <td>${row.comment}</td>
        <td>${row.word_length}</td>
    `;
    contentTableBody.appendChild(tr);
    });

    // Re-initialize the paginator to update the buttons and highlight the current page
    initPaginator(pageData);
}

    // Function to get the class name based on sentiment value
function getClassForSentiment(sentiment) {
    if (sentiment === "positive") {
    return "label-tag-pos";
    } else if (sentiment === "negative") {
    return "label-tag-neg";
    } else {
    return "label-tag-neu";
    }
}

// Flag to check if the paginator has been initialized
var paginatorInitialized = true;

// Function to create paginator buttons
function createPaginatorButtons() {
    var totalPages = Math.ceil(jsonData.length / itemsPerPage);
    var paginator = document.getElementById("paginator");

    for (var i = 1; i <= totalPages; i++) {
        var button = document.createElement("button");
        button.textContent = i;
        button.addEventListener("click", function() {
        var pageNum = parseInt(this.textContent);
        displayPage(pageNum);
        });
        paginator.appendChild(button);
    }

    paginatorInitialized = true; // Set the flag to true after creating buttons
}

// Function to filter and sort the data based on selected options
function filterAndSortData() {
    var selectedSentiment = document.getElementById("sentiment").value;
    var sortOrder = document.getElementById("sortOrder").value;
    var multiplier = sortOrder === "asc" ? 1 : -1;

    var filteredData = jsonData;
    if (selectedSentiment !== "all") {
        filteredData = jsonData.filter(function(row) {
        return row.sentiment === selectedSentiment;
        });
    }
    filteredData.sort(function(a, b) {
        if (sortOption === "index") {
        return multiplier * (a.index - b.index);
        } else if (sortOption === "likes") {
        return multiplier * (a.like_count - b.like_count);
        } else if (sortOption === "replies") {
        return multiplier * (a.reply_count - b.reply_count);
        } else if (sortOption === "word_length") {
        return multiplier * (a.word_length - b.word_length);
        }
    });
    console.log('Filter data based on: ', selectedSentiment,",", sortOrder,",", multiplier)
    return filteredData;
}

    // Function to handle sorting and filtering based on the selected option and order
function handleSortAndFilter() {
    sortOption = document.getElementById("sortBy").value;
    var sortOrder = document.getElementById("sortOrder").value;

    var sortedAndFilteredData = filterAndSortData();
    displayPage(1, sortedAndFilteredData); // Re-display the first page after sorting and filtering
    initPaginator(sortedAndFilteredData);
    }

// Call the initialization function when the page loads
document.getElementById("sortBy").addEventListener("change", function() {
    handleSortAndFilter();
    paginatorInitialized = false; // Reset the flag when sorting changes
    initPaginator(sortedAndFilteredData); // Reinitialize the paginator after sorting and filtering
});

document.getElementById("sortOrder").addEventListener("change", function() {
    handleSortAndFilter();
    paginatorInitialized = false; // Reset the flag when sorting changes
    initPaginator(sortedAndFilteredData); // Reinitialize the paginator after sorting and filtering
});

document.getElementById("sentiment").addEventListener("change", function() {
    handleSortAndFilter();
    paginatorInitialized = false; // Reset the flag when sentiment filter changes
    initPaginator(sortedAndFilteredData); // Reinitialize the paginator after sorting and filtering
});

// Initialize the sorting and paginator by calling the handleSortAndFilter function
handleSortAndFilter();

// Initialize the paginator only once on page load
if (!paginatorInitialized) {
    createPaginatorButtons();
}


// Create export to csv functionality
// Function to convert JSON data to CSV format
function convertToCSV(data) {
    console.log('Converting data to csv format.')
    const separator = ',';
    const keys = Object.keys(data[0]);
    const csvRows = [keys.join(separator)];

    for (const item of data) {
      const values = keys.map(key => {
        let value = item[key];
        if (key === 'comment' && typeof value === 'string' && value.includes('  ')){
            value = value.replace('  ', " ");
        }
        if (key === 'comment' && typeof value === 'string' && value.includes(',')) {
            //console.log(value)
            value = `"${value}"`; // Enclose comment value in double quotes if it contains a comma
        }
        return value;
      });
      const row = values.join(separator);
      csvRows.push(row);
    }

    return csvRows.join('\n');
  }

  // Function to download the CSV file
  function downloadCSV(csvData, filename) {
    const csvBlob = new Blob([csvData], { type: 'text/csv' });
    const csvUrl = URL.createObjectURL(csvBlob);
    const link = document.createElement('a');
    link.setAttribute('href', csvUrl);
    link.setAttribute('download', filename);
    link.click();
  }

  // Function to handle the export button click
  document.getElementById('exportButton').addEventListener('click', function () {
    const sortedAndFilteredData = filterAndSortData(); // Use your filter and sort function to get the data
    const csvData = convertToCSV(sortedAndFilteredData);
    const filename = 'comments.csv';
    downloadCSV(csvData, filename);
    console.log('Downloading comments.')
  });
