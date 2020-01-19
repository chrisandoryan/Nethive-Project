var elasticsearch = require('elasticsearch');

var client = new elasticsearch.Client({
    host: 'http://elastic:changeme@localhost:9200',
});

module.exports = client;