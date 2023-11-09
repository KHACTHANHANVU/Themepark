var mysql = require('mysql');
var fs = require('fs');
var http = require('http');
var path = require('path')

var config = {
    host:"themeparkproject.mysql.database.azure.com",
    user:"team3",
    password:"Password1",
    database:"novapark",
    port:3306,
    ssl:{ca:fs.readFileSync("DigiCertGlobalRootCA.crt.pem")}
}
var conn=mysql.createConnection(config);
conn.connect(function(err) {
    if (err) throw err;
    console.log("Connected!");
});


function get_visitors() {
    query = conn.query("SELECT first_name FROM novapark.visitor", [age], function (err, result, field) {
        if (err) throw err;
        console.log(result);
    })
    conn.end()
    console.log(query)
};

