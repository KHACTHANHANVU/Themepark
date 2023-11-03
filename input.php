
<?php

$host = "themeparkdbproj.database.windows.net";
$user = "team3";
$password = "Password1"
$conn = new mysqli($host, $user, $password);

// azure database for mysql servers -> themeparkprojectdb
// themeparkprojectdb.mysql.database.azure.com

$CREATE = "create database if not exists novapark;";

?>

<?php
// PHP Data Objects(PDO) Sample Code:
try {
    $conn = new PDO("sqlsrv:server = tcp:themeparkdbproj.database.windows.net,1433; Database = ThemePark", "team3", "{your_password_here}");
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch (PDOException $e) {
    print("Error connecting to SQL Server.");
    die(print_r($e));
}

// SQL Server Extension Sample Code:
$connectionInfo = array("UID" => "team3", "pwd" => "{your_password_here}", "Database" => "ThemePark", "LoginTimeout" => 30, "Encrypt" => 1, "TrustServerCertificate" => 0);
$serverName = "tcp:themeparkdbproj.database.windows.net,1433";
$conn = sqlsrv_connect($serverName, $connectionInfo);
?>

# https://storageforwebsite.z13.web.core.windows.net/
# https://storageforwebsite-secondary.z13.web.core.windows.net/
# https://stackoverflow.com/questions/4081981/how-to-connect-database-to-my-website