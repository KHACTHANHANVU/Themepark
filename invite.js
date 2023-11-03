var mysql = require('mysql');
var fs = require('fs');
var conn=mysql.createConnection({host:"themeparkprojectdb.mysql.database.azure.com", user:"team3", password:"Password1", database:"novapark", port:3306, ssl:{ca:fs.readFileSync("DigiCertGlobalRootCA.crt.pem")}});
conn.connect(function(err) {
    if (err) throw err;
    console.log("Connected!");
  });
  