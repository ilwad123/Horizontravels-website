function getarrivalcity(deptcity)    
    {
          var req = new XMLHttpRequest();        
          arrivalslist = document.getElementById('arrivalslist');        
          
          req.onreadystatechange = function(){
              if (req.readyState == 4){
                  if (req.status != 200){
                      //error handling code here
                  }
                  else{
                      var response = JSON.parse(req.responseText);                   
                      //document.getElementById('myDiv').innerHTML = response.username
                      var size = response.size;                   
                      //alert(response.returncities[0]);
                      for (var x=0; x < arrivalslist.length; x++){
                          arrivalslist.remove(x);                        
                      }
                      
                      for (var i=0; i < size; i++){  
  
                              arrivalslist.add(new Option(response.returncities[i], response.returncities[i]));    
                      }
                         // var option = document.createElement("Option");
                          //option.text = response.returncities;
                          //arrivalslist.add(option);
                  }
              }
          }
          req.open('GET', '/returncity/?q='+deptcity);
          req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");   
          req.send(); 
          return false;
      }
  