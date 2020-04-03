var express = require('express');
var router = express.Router();
var cpu = require('../public/javascripts/handler/stats')
/* GET admin page. */
router.get('/usrcpu', function(req, res, next) {
  res.json(cpu());
});


module.exports = router;
