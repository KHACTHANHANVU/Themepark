-- Active: 1700086382953@@themeparkproject.mysql.database.azure.com@3306@novapark
CREATE DATABASE IF NOT EXISTS novapark;

USE novapark;


create table novapark.staff (
	staff_id smallint primary key auto_increment,
    pswrd VARCHAR(10),
    phone_no char(10),
    addrs varchar(35),
    supervisor_id char(7),
    hours_work char(3),
    hourly_wage numeric(8,2) not null check(hourly_wage > 7.25),
    dob date not null,
    job enum('manager', 'repair', 'rides') not null,
);

CREATE TABLE novapark.customer (
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    pswrd VARCHAR(10),
    email VARCHAR(35) PRIMARY KEY,
    phone CHAR(10),
    pass_credits SMALLINT,
    num_passes INT
);

CREATE TABLE novapark.park_pass (
    cust_email INT PRIMARY KEY,
    num_passes INT,
    date_bought datetime,
    is_valid boolean
);

CREATE TABLE novapark.amusement_ride (
	ride_name VARCHAR(12) NOT NULL,
    ride_no SMALLINT PRIMARY KEY,
    is_working BOOL DEFAULT TRUE,
    date_of_last_repair DATETIME,
);

CREATE TABLE novapark.ride_repair (
	ride_no SMALLINT,
    date_of_issue DATETIME NOT NULL,
    repair_date DATETIME NOT NULL,
    repair_cost FLOAT NOT NULL,
    FOREIGN KEY (ride_no) REFERENCES novapark.amusement_ride(ride_no),
);

CREATE TABLE novapark.events (
	event_no smallint primary key auto_increment,
    e_name varchar(22) not null,
    start_date date,
    end_date date
);

CREATE TABLE novapark.business_day (
	num_of_visitors smallint not null check(num_of_visitors > -1),
    b_date date primary key,
    revenue numeric(8,2) not null check (revenue > 0.0),
    expenses numeric(8,2) not null check (expenses > 0.0)    
);


