
var data = "{\"EVENT_DATA\":{\"elastic_id\":\"osPr2m4BGbUPoE8lEH3W\",\"command\":\"sudo python3 main.py \",\"workdir\":\"/home/sh/Documents/Research/Blackhead\",\"hostname\":\"siahaan\",\"exectime\":\"2019-12-06T18:14:18.174\",\"executor\":\"sh\",\"type\":\"TYPE_BASH_CENTRALIZED\",\"source\":\"/var/log/bash/history.log\"},\"EVENT_TYPE\":\"BASH_MONITOR\",\"@timestamp\":\"2019-12-06 11:20:15.921991\"}";
 
var objects = JSON.parse(data);

function logsHandler(table,theader){
    $(table).append("<tr>");
    for(var i=1 ; i <= $(theader).length ; i++){
        $(table+" tr:last").append("<td>"+objects["EVENT_DATA"][$(theader+':nth-child('+i+')').text()]+"</td>")
        console.log(objects["EVENT_DATA"][$(theader+':nth-child('+i+')').text()]);
    }
    $(table).append("</tr>");
}

function logsTypeHandler(type){
    var theader, table;
    if(type == "BASH_MONITOR"){
        table = "#table-bash tbody";
        theader = "#table-bash thead th";
    }
    return logsHandler(table, theader);
}

function messageHandler(objects){
    for (var i in objects) {
        if (objects.hasOwnProperty(i)) {
            if(i == "EVENT_TYPE"){
                // return objects[i] == "BASH_MONITOR" ? bashLogHandler(objects) : "not";
                logsTypeHandler(objects[i]);            
            }
        }         
    }
    return false;
}

messageHandler(objects);
messageHandler(objects);

// console.log(obj["EVENT_TYPE"]);