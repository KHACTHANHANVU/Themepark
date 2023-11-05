var mysql = require('mysql');
var fs = require('fs');
var config = {
    host:"themeparkprojectdb.mysql.database.azure.com",
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


function check_login_creds(username, password) {
    conn.query("SELECT * FROM * WHERE ( = ?) AND ( = ?)", [username, password])
    conn.end()
};