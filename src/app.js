const http = require('http');
const fs = require('fs');

const hostname = '127.0.0.1';
const port = process.env.port || 8080;

/*
const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
*/

fs.readFile("carousel.html", function(err, file) {
  if (err) throw err;

  console.log("first\n");
  http.createServer(function(req, res) {
    res.statusCode = 200
    res.write(file);
    res.end()
  }).listen(port)
  console.log("second\n");
});

/*
fs.readFile("carousel.html", function(err, file) {
  if (err) throw err;

  console.log("first\n");
  http.createServer(function(req, res) {
    console.log("inner first\n");
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(file);
    res.end()
    console.log("inner second\n");
  }).listen(port)
  console.log("second\n");
});
*/


