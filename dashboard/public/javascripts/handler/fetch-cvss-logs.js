var URI = 'http://localhost:3000/logs/cvss/timestamp/desc';

function fetchConversation(){
    var score = severity(e.SUMMARIZE_RESULT.score);
    let img = "<img src='/images/face-placeholder.png' alt='' style='height:64px; width:64px'>"
    var tr  = "<tr></tr>";
    var td1 = $("<td></td>").text(e.timestamp);   // Create with jQuery
    var td2 = $("<td></td>").text("test");   // Create with jQuery
    var td3 = $("<td></td>").text(e.SUMMARIZE_RESULT.vector);   // Create with jQuery
    var td4 = $("<td></td>").append(score);   // Create with jQuery
    $("#notifs").append(tr);      // Append the new elements 
    $("#table-cvss tbody tr:last-child").append(td1,td2,td3,td4);
}
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
    var td2 = $("<td></td>").text(e.vul_tag);   // Create with jQuery
    var td3 = $("<td></td>").text(e.SUMMARIZE_RESULT.vector);   // Create with jQuery
    var td4 = $("<td></td>").append(score);   // Create with jQuery
    $("#table-cvss tbody").append(tr);      // Append the new elements 
    $("#table-cvss tbody tr:last-child").append(td1,td2,td3,td4);
}

function emptyData(){
    $("#table-cvss tbody").empty();
}
function getRecent(data){
    let recent
    if(URI.split("/").slice(-1) == "desc"){
        recent = data[0].timestamp
    }
    if(URI.split("/").slice(-1) == "asc"){
        
        recent = data.slice(-1)[0].timestamp
    }
    return recent
}
function setRecentDate(recent){
        function binDigitize(number){
            // make sure the integer consists of two digits
            if(number < 10){
                return "0" + number.toString()
            }
            return number.toString()
        }
        let date_template = new Date(recent);
        let hours = binDigitize(date_template.getHours())
        let minutes = binDigitize(date_template.getMinutes())
        let seconds = binDigitize(date_template.getSeconds())
        let year = binDigitize(date_template.getFullYear() - 2000)
        let month = binDigitize(date_template.getMonth() + 1)
        let day = binDigitize(date_template.getDay())
        let final_recent = day + "/" + month + "/" + year + " " + hours + ":" + minutes + ":" + seconds
        return final_recent
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
        let recent  = getRecent(data)
        let final_recent = setRecentDate(recent)
        $("#last_attack").html(final_recent)
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
