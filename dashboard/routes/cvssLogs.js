var express = require('express');
var router = express.Router();

var esCvss = require('../public/javascripts/handler/search-api');
var esBash = require('../public/javascripts/handler/bashmon_search_api')
router.get('/cvss/:by/:sort/', function(req,res,next){
    esCvss( (hit) => {
        let logs = [];
        for (let i = 0; i < hit.length; i++) {
            logs.push(hit[i]._source);
        }
        res.json(logs);
    }, req.params.by, req.params.sort); 
});
router.get("/bash/:by/:sort",function(req,res,next){
	esBash( (hit) => {
        let logs = [];
        for (let i = 0; i < hit.length; i++) {
            logs.push(hit[i]._source);
        }
        res.json(logs);
    }, req.params.by, req.params.sort);
})
module.exports = router;