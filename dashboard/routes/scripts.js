require('jquery')

var express = require('express');
var router = express.Router();

// router.get('/jquery.min.js', function(req, res) {
//     res.sendFile('/jquery/dist/jquery.min.js', {'root' : '/../node_modules'});
// });

router.get('/jquery-ui-dist/jquery-ui.min.js', function(req, res) {
    res.sendFile(__dirname + '/../node_modules/jquery-ui-dist/jquery-ui.min.js');
});

router.get('/bootstrap/dist/js/bootstrap.bundle.min.js', function(req, res) {
    res.sendFile(__dirname + '/../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js');
});

router.get('/chart.js/Chart.min.js', function(req, res) {
    res.sendFile(__dirname + '/../node_modules/chart.js/dist/Chart.min.js');
});

module.exports = router;
