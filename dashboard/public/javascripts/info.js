var client = require('./elasticsearch-client.js');

client.cluster.health({},function(err,resp,status) {  
  console.log("-- Client Health --",resp);
});