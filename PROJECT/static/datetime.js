
  function setenddate(){
      var selectedstartdate = document.getElementById("Departure_date").value;
      document.getElementById("Arrival_date").min = selectedstartdate;
  }
  function initialdate(){
      var today=new Date();
      var year = today.getFullYear();
      var month = today.getMonth() + 1;
      var day = today.getDate();           
      if (month < 10) {
          month = '0' + month; 
      }
      if (day < 10) {
          day = '0' + day; 
      }
      today = year + '-' + month + '-' + day;           
      document.getElementById("Departure_date").min = today;            
  }

