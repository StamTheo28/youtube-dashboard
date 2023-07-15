<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>

document.addEventListener('DOMContentLoaded', function() {
  var sentimentData = JSON.parse('{{ sentiment|safe }}');
  var labels = [];
  var data = [];
  
  for (var key in sentimentData) {
      labels.push(key);
      data.push(sentimentData[key]);
  }
  
  
  var ctx = document.getElementById('pieChart').getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'pie',
      data: {
          labels: labels,
          datasets: [{
              data: data,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.6)',
                  'rgba(255, 206, 86, 0.6)',
                  'rgba(75, 192, 192, 0.6)',
                  
              ]
          }]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          title: {
              display: true,
              text: 'Percentage of Comment Type',
              fontSize: 18,
              fontColor: '#000000',
              fontStyle: 'bold'
          }
      }
  });
});