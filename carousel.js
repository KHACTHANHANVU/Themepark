/*

function get_users(age) {
  const query = conn.query("SELECT first_name FROM novapark.visitor WHERE age = 18", [age], function (err, result, field) {
    if (err) throw err;
    console.log(result);
  });

  // Note: You should not call conn.end() here if you intend to use the connection for multiple queries.
  // Close the connection when you're done with it.

  console.log(query);
}

// Use the connection in your carousel.js
get_users(10);
*/

// Implement your carousel functionality here
// You can continue using the 'conn' object for database operations as needed.

var general = require('./general_util.js');
var conn = general.connection;
var fs = require('fs');
var http = require('http');
var path = require('path')

const hostname = '127.0.0.1';
const port = process.env.port || 8080;

fs.readFile(path.join(__dirname, '..', 'carousel.html'), function(err, file) {
  if (err) throw err;

  console.log("first\n");
  http.createServer(function(req, res) {
    res.statusCode = 200
    res.write(file);
    console.log(req.url)
    res.end()

  }).listen(port)
  console.log("second\n");
});



