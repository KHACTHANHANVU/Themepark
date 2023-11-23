CREATE DATABASE IF NOT EXISTS novapark;

USE novapark;


CREATE TABLE novapark.staff (
	staff_id SMALLINT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    pswrd VARCHAR(10),
    phone_no CHAR(10),
    addrs VARCHAR(35),
    supervisor_id SMALLINT,
    hourly_wage NUMERIC(8,2) NOT NULL CHECK(hourly_wage > 7.25),
    dob DATE NOT NULL,
    job ENUM('manager', 'repair', 'rides') NOT NULL,
    FOREIGN KEY (supervisor_id) REFERENCES novapark.staff(staff_id)
);

ALTER TABLE novapark.staff AUTO_INCREMENT = 100;

CREATE TABLE novapark.hours_worked (
    staff_id SMALLINT,
    num_hours SMALLINT,
    cur_date DATE,
    PRIMARY KEY (staff_id, cur_date),
    FOREIGN KEY (staff_id) REFERENCES novapark.staff(staff_id)
);

CREATE TABLE novapark.customer (
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    pswrd VARCHAR(10),
    email VARCHAR(35),
    phone CHAR(10),
    pass_credits SMALLINT DEFAULT 0,
    PRIMARY KEY (email)
);

CREATE TABLE novapark.park_pass (
    cust_email VARCHAR(35),
    num_passes INT,
    sale_cost INT,
    pass_type ENUM('Silver', 'Gold', 'Platinum'),
    date_bought DATETIME,
    card_fname VARCHAR(30),
    card_lname VARCHAR(30),
    card_num VARCHAR(16),
    cvv VARCHAR(3),
    exp_month VARCHAR(2),
    exp_year VARCHAR(2),
    PRIMARY KEY (cust_email, date_bought),
    FOREIGN KEY (cust_email) REFERENCES novapark.customer(email)
);

CREATE TABLE novapark.ride_injury (
    reporter_id SMALLINT,
    ride_no SMALLINT,
    email_of_injured VARCHAR(35),
    injury_date DATETIME,
    injury_description VARCHAR(100),
    PRIMARY KEY (injury_date, email_of_injured),
    FOREIGN KEY (reporter_id) REFERENCES novapark.staff(staff_id),
    FOREIGN KEY (email_of_injured) REFERENCES novapark.customer(email),
    FOREIGN KEY (ride_no) REFERENCES novapark.amusement_ride(ride_no)
);


CREATE TABLE novapark.amusement_ride (
	ride_name VARCHAR(12) NOT NULL,
    ride_no SMALLINT AUTO_INCREMENT,
    is_working BOOL DEFAULT TRUE,
    date_of_last_repair DATETIME,
    PRIMARY KEY (ride_no)
);

ALTER TABLE novapark.amusement_ride AUTO_INCREMENT = 1;

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
    manager_id SMALLINT,
    e_name VARCHAR(22) NOT NULL,
    e_descrip VARCHAR(200),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (manager_id) REFERENCES novapark.staff(staff_id)
);

ALTER TABLE novapark.events AUTO_INCREMENT = 1;

CREATE TABLE novapark.business_day (
    b_date DATE PRIMARY KEY,
    revenue FLOAT NOT NULL CHECK (revenue > 0.0),
    expenses FLOAT NOT NULL CHECK (expenses > 0.0)
);