-- Active: 1700086382953@@themeparkproject.mysql.database.azure.com@3306@novapark
CREATE DATABASE IF NOT EXISTS novapark;

USE novapark;


CREATE TABLE novapark.staff (
	staff_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    pswrd VARCHAR(10),
    phone_no CHAR(10),
    addrs VARCHAR(35),
    supervisor_id SMALLINT,
    hours_work CHAR(3),
    hourly_wage NUMERIC(8,2) NOT NULL CHECK(hourly_wage > 7.25),
    dob DATE NOT NULL,
    job ENUM('manager', 'repair', 'rides') NOT,
);

ALTER TABLE novapark.staff ADD FOREIGN KEY (supervisor_id) REFERENCES novapark.staff(staff_id);

ALTER TABLE novapark.staff AUTO_INCREMENT=100;

CREATE TABLE novapark.customer (
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    pswrd VARCHAR(10),
    email VARCHAR(35),
    phone CHAR(10),
    pass_credits SMALLINT,
    num_passes INT,
    PRIMARY KEY (email),
    FOREIGN KEY (email) REFERENCES novapark.park_pass(cust_email)
);

CREATE TABLE novapark.card_info {
    eamil VARCHAR(35) PRIMARY KEY,
    card_num VARCHAR(16),
    cvv VARCHAR(3),
    exp_month VARCHAR(2),
    exp_year VARCHAR(2)

};

ALTER TABLE novapark.customer AUTO_INCREMENT=100;

CREATE TABLE novapark.park_pass (
    cust_email VARCHAR(35),
    num_passes INT,
    pass_type ENUM('daily', 'weekly', 'montly'),
    date_bought DATETIME,
    is_valid BOOLEAN,
    PRIMARY KEY (cust_email, pass_type, date_bought)
);


CREATE TABLE novapark.amusement_ride (
	ride_name VARCHAR(12) NOT NULL,
    ride_no SMALLINT,
    is_working BOOL DEFAULT TRUE,
    date_of_last_repair DATETIME,
    PRIMARY KEY (ride_no)
    # FOREIGN KEY (ride_no) REFERENCES novapark.ride_repair(ride_no)
);

ALTER TABLE novapark.amusement_ride ADD FOREIGN KEY (ride_no) REFERENCES novapark.ride_repair(ride_no);

CREATE TABLE novapark.ride_repair (
	ride_no SMALLINT,
    date_of_issue DATETIME NOT NULL,
    repair_date DATETIME NOT NULL,
    repair_cost FLOAT NOT NULL,
    PRIMARY KEY (ride_no),
    FOREIGN KEY (ride_no) REFERENCES novapark.amusement_ride(ride_no)
);

CREATE TABLE novapark.events (
	event_no SMALLINT PRIMARY KEY AUTO_INCREMENT,
    e_name VARCHAR(22) NOT NULL,
    start_date DATE,
    end_date DATE
);

CREATE TABLE novapark.business_day (
	num_of_visitors SMALLINT NOT NULL CHECK(num_of_visitors > -1),
    b_date DATE PRIMARY KEY,
    revenue NUMERIC(8,2) NOT NULL CHECK (revenue > 0.0),
    expenses NUMERIC(8,2) NOT NULL CHECK (expenses > 0.0)    
);


