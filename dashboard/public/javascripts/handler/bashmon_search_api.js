var client = require('./elasticsearch-client.js');


function startBashLog (callback,method, sortby){
    let query = {};
    
    if(method=="timestamp"){
      query = {"@timestamp":sortby};
    }
    client.search({  
      index: 'nethive-bash-*',
      type: '_doc',
      body: {
        sort: [query],
        size: 5,
      }
    },function (error, response,status) {
        if (error){
          console.log("search error: "+error)
          callback({"error":"searching failed.."})
        }
        else {
          // console.log("--- Response ---");
          console.log(response);
          // console.log("--- Hits ---");
            callback(response.hits.hits);
        }
    });
}

module.exports = startBashLog;