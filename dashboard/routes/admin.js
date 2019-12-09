var express = require('express');
var router = express.Router();

/* GET admin page. */
router.get('/', function(req, res, next) {
  res.render('admin', { title: 'AdminPage :: NetHive :: Zero-to-Low Latency Monitoring System' });
});

router.get('/dashboard', function(req, res, next) {
  res.render('pages/dashboardPage');
});

router.get('/config', function(req,res,next){
  res.render('pages/configurationPage');
});

router.get('/logs/web', function(req,res,next){
  res.render('pages/logs/logsWebPage');
});

router.get('/logs/audit', function(req,res,next){
  res.render('pages/logs/logsAuditPage');
});

router.get('/logs/bash', function(req,res,next){
  res.render('pages/logs/logsBashPage');
});

module.exports = router;
