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


first_name = [
    'Noel', 'Jerry', 'Jerald'
];

last_name = [
    'Bob', 'Mood', 'Steve'
];

ticket_no  = [
    '1234568', '1234569', '1234570'
];
phone = [
    '1111111111', '1111112222', '1112221111'
];
is_present = [
    false, true, false
];
age = [
    18, 24, 15
];
num_of_visitations = [
    2, 5, 1
];

visitors = [
    ['Noel', 'Bob', '1234568', '1111111111', false, 18, 2],
    ['Jerry', 'Mood', '1234569', '1111112222', true, 24, 5],
    ['Jerald', 'Steve', '1234570', '1112221111', false, 15, 1]
]

tickets = [
    ['1234568', 100],
    ['1234569', 100],
    ['1234570', 50]
]

console.log(visitors);


/*
conn.query("SELECT * FROM novapark.visitor", function (err, result, field) {
    if (err) throw err;
    console.log(result);
})*/

var i = "INSESRT INTO novapark.visitor (first_name, last_name, ticket_no, phone, is_prese".length;
console.log(i);

console.log("INSESRT INTO novapark.visitor (first_name, last_name, ticket_no, phone, is_present, age, num_of_visitations) VALUES ?;", [visitors]);

i = "INSESRT INTO novapark.tickets (t_no, price, t_type) SET ('1234568', 100), ('1234".length;
console.log(i);

conn.query("INSESRT INTO novapark.tickets (t_no, price, t_type) SET ?;", 
            [tickets], function (err, result) {
    if (err) throw err;
    console.log(result);
});






