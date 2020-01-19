var express = require('express');
var router = express.Router();

/* GET admin page. */
router.get('/', function(req, res, next) {
  res.render('pages/dashboardPage', { title: 'AdminPage :: NetHive :: Zero-to-Low Latency Monitoring System' });
});

router.get('/config', function(req,res,next){
  res.render('pages/configurationPage',{ title: 'AdminPage :: NetHive :: Zero-to-Low Latency Monitoring System' });
});

router.get('/logs/web', function(req,res,next){
  res.render('pages/logs/logsWebPage',{ title: 'AdminPage :: NetHive :: Zero-to-Low Latency Monitoring System' });
});

router.get('/logs/audit', function(req,res,next){
  res.render('pages/logs/logsAuditPage',{ title: 'AdminPage :: NetHive :: Zero-to-Low Latency Monitoring System' });
});

router.get('/logs/bash', function(req,res,next){
  res.render('pages/logs/logsBashPage',{ title: 'AdminPage :: NetHive :: Zero-to-Low Latency Monitoring System' });
});

module.exports = router;
