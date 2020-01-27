var URI = 'http://localhost:3000/logs/cvss/priority/desc';

function severity(score){
    var span = "";
    var badge = "";
    var severity="";

    if(score == 0.0 ){
        badge = "badge bg-black";
        severity = "None";
    }
    else if(score >= 0.1 && score <= 3.9){
        badge = "badge bg-green";
        severity = "Low";
    }
    else if(score >= 4.0 && score <= 6.9){
        badge = "badge bg-yellow";
        severity = "Medium";
    }
    else if(score >= 7.0 && score <= 8.9){
        badge = "badge bg-red";
        severity = "High";
    }
    else if(score >= 9.0 && score <= 10.0){
        badge = "badge bg-purple";
        severity = "Critical";
    }
    
    span = "<span class='"+badge+"'>"+score+" "+severity+"</span>";
    return span
}

function appendData(e) {
    var score = severity(e.SUMMARIZE_RESULT.score);

    var tr  = "<tr></tr>";
    var td1 = $("<td></td>").text(e.timestamp);   // Create with jQuery
    var td2 = $("<td></td>").text("test");   // Create with jQuery
    var td3 = $("<td></td>").text(e.SUMMARIZE_RESULT.vector);   // Create with jQuery
    var td4 = $("<td></td>").append(score);   // Create with jQuery
    $("#table-cvss tbody").append(tr);      // Append the new elements 
    $("#table-cvss tbody tr:last-child").append(td1,td2,td3,td4);
}

function emptyData(){
    $("#table-cvss tbody").empty();
}

setInterval(() => {
fetch(URI)
  .then(
    function(response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
          response.status);
        return;
      }

      // Examine the text in the response
      response.json().then(function(data) {
        // console.log(data);
        emptyData();
        data.forEach(element => {
            // console.log(element.vector)
            appendData(element);
        });
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });
}, 3000);
