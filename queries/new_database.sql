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
    is_working bool default true,
    date_of_last_repair date,
);

create table novapark.ride_repair (
	ride_no smallint,
    date_of_issue datetime NOT NULL,
    repair_date datetime NOT NULL,
    repair_cost FLOAT not null,
    foreign key (ride_no) references novapark.amusement_ride(ride_no),
);

create table novapark.events (
	event_no smallint primary key auto_increment,
    e_name varchar(22) not null,
    start_date date,
    end_date date
);

create table novapark.business_day (
	num_of_visitors smallint not null check(num_of_visitors > -1),
    b_date date primary key,
    revenue numeric(8,2) not null check (revenue > 0.0),
    expenses numeric(8,2) not null check (expenses > 0.0)    
);


describe novapark.ticket;
alter table novapark.visitor modify num_of_visitations int default 1;
describe novapark.visitor;

CREATE TRIGGER TRIGGER_ON_SIGNUP BEFORE INSERT ON novapark.

DELIMITER //
CREATE TRIGGER trigger_Employee_inserthour BEFORE UPDATE ON novapark.staff
FOR EACH ROW
BEGIN
    DECLARE rowCount INT;
    
    SELECT COUNT(*) INTO rowCount FROM novapark.staff;
    
    IF rowCount = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Table Staff does not have any data';
    END IF;

    IF NEW.hours_work > 40 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Table staff cannot be updated';
    END IF;
    
    IF NEW.hours_work > 40 THEN
        UPDATE week_wage
        SET week_wage = week_wage * 1.5 * NEW.hours_work
        WHERE staff_no = NEW.staff_no;
    END IF;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER trigger_visitor_ispresent BEFORE UPDATE ON novapark.visitor
FOR EACH ROW
BEGIN
    DECLARE rowCount INT;
    
    SELECT COUNT(*) INTO rowCount FROM novapark.visitor;
    
    IF rowCount = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Table Visitor does not have any data';
    END IF;

    IF NEW.ticket_no IS NOT NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You are qualified for coupons';
    END IF;
    
    IF NEW.is_present = TRUE THEN
        UPDATE novapark.price
        SET price = price * 0.75;
    END IF;
END;
//
DELIMITER ;
