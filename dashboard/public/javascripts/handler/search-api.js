var client = require('./elasticsearch-client.js');


function startCvssLog (callback,method, sortby){
    let query = {};
    if(method=="priority"){
      query = {"SUMMARIZE_RESULT.score":sortby};
    }
    client.search({  
      index: 'nethive-cvss',
      type: '_doc',
      body: {
        sort: [query],
        size: 5,
      }
    },function (error, response,status) {
        if (error){
          console.log("search error: "+error)
        }
        else {
          // console.log("--- Response ---");
          console.log(response);
          // console.log("--- Hits ---");
            callback(response.hits.hits);
        }
    });
}

module.exports = startCvssLog;