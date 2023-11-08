var general = require('../general_util.js');
var conn = general.connection;
var fs = require('fs');
var http = require('http');
var path = require('path');
var url = require('url');

const hostname = '127.0.0.1';
const port = process.env.port || 8080;

http.createServer(function(req, res) {
    
    if (req.url == "/styles.css") {
        fs.readFile('./public/styles.css', function (err, file) {
            if (err) throw err;
            res.writeHead(200, {'Content-Type': 'text/css'});
            res.write(file);
            res.end();
        });
    } else if (req.url == '/') {
        console.log('here')
        fs.readFile(path.join(__dirname, '..', 'public', 'carousel.html'), function (err, file) {
            if (err) {console.log(__dirname); throw err;}
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(file);
            res.end();
        });
    } else {
        console.log(req.url);
    }
}).listen(port);
