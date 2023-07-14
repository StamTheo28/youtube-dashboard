document.addEventListener('DOMContentLoaded', function() {
    var chartData = JSON.parse('{{ sentiment }}');
    
    var data = {
      labels: Object.keys(chartData),
      datasets: [{
        data: Object.values(chartData),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#8DE081'
        ]
      }]
    };
  
    var options = {
      responsive: true
    };
  
    var ctx = document.getElementById('pieChart').getContext('2d');
    new Chart(ctx, {
      type: 'pie',
      data: data,
      options: options
    });
  });
  