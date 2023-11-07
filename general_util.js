var mysql = require('mysql');
var fs = require('fs');
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


function get_users(age) {
    query = conn.query("SELECT first_name FROM novapark.visitor WHERE (age > ?)", [age])
    conn.end()
    console.log(query)
};

// check_login_creds('team3','password')
get_users(10)

