create database if not exists novapark;
use novapark;

create table novapark.ticket (
	t_no char(7) primary key,
    price numeric(4,2) not null check(price > 0.5),
    t_type enum('silver', 'gold', 'platinum') default 'gold'
);

create table novapark.visitor (
	first_name varchar(15) not null,
    last_name varchar(15) not null,
    ticket_no char(7) primary key,
    phone char(10),
    is_present bool default true,
    age int not null,
    num_of_visitations int default 0
);

alter table novapark.visitor modify num_of_visitations smallint default 0;


create table novapark.department (
	d_name varchar(6) not null,
    d_no tinyint primary key auto_increment,
    manager_no smallint not null,
    weekly_budget numeric(8,2) default 5400
    -- weekly_expenses numeric(7,2)
    
);


create table novapark.staff (
	staff_no smallint primary key auto_increment,
    phone_no char(10),
    address varchar(35),
    supervisor_id char(7),
    hours_work char(3),
    week_wage numeric(8,2) not null check(week_wage > 300 and week_wage < 850),
    dob date not null,
    job enum('supervisor', 'manager', 'sales', 'security', 'domestic') not null,
    dept_no tinyint not null,
    foreign key(dept_no) references novapark.department(d_no)
);

alter table novapark.department add foreign key (manager_no) references novapark.staff(staff_no); 

create table novapark.amusement_ride (
	ride_name varchar(12) not null,
    ride_no smallint primary key auto_increment,
    num_of_riders smallint default 0,
    daily_runs smallint default 0,
    is_working bool default true,
    date_of_last_repair date,
    max_capacity smallint not null
);

create table novapark.ride_repair (
	ride_no smallint,
    repairer_no smallint,
    repair_date date not null,
    cost double not null,
    foreign key (ride_no) references novapark.amusement_ride(ride_no),
    foreign key (repairer_no) references novapark.staff(staff_no)
);

create table novapark.business_day (
	num_of_visitors smallint not null check(num_of_visitors > -1),
    num_of_rainouts tinyint default 0 check(num_of_rainouts > -1),
    b_date date primary key,
    ride_revenue numeric(8,2) not null check(ride_revenue > 0.0),
    vendor_revenue numeric(8,2) not null check(vendor_revenue > 0.0),
    resort_revenue numeric(8,2) not null check(resort_revenue > 0.0),
    restaurant_revenue numeric(8,2) not null check(restaurant_revenue > 0.0),
    vendor_expenses numeric(8,2) not null check(vendor_expenses > 0.0),
    resort_expenses numeric(8,2) not null check(resort_expenses > 0.0),
    restaurant_expenses numeric(8,2) not null check(restaurant_expenses > 0.0)
    
);

create table novapark.daily_rides (
	ride_no smallint not null,
    num_of_rides smallint default 0,
    _date date not null,
    foreign key (ride_no) references novapark.amusement_ride(ride_no)
);

-- create table novapark.dept_daily_expenses(
-- 	d_no tinyint not null,
--     amount numeric(8,2) not null,
--     _date date primary key
-- );

create table novapark.sale (
	-- receipt_prefix char(7) auto_increment, 
    discount_applied_percent numeric(3,1) default 0.0 check(discount_applied_percent >= 0.0),
    sale_time datetime primary key,
    ticket_no char(7) not null,
    dept_no tinyint not null,
    foreign key(ticket_no) references novapark.ticket(t_no),
    foreign key(dept_no) references novapark.department(d_no)
);

create table novapark.variable (
	ticket_price numeric(4,2) check(ticket_price > 0.0),
    max_refund numeric(4,2) check(max_refund > 0.0),
    max_discount_percent numeric(3,1) check(max_discount_percent >= 0.0),
    -- min_restaurant_capacity smallint,
    default_capacity smallint check(default_capacity > 0),
    start_date date
    -- expected_min_restaurant_revenue numeric
);

create table novapark.refund (
	ticket_no char(7) not null,
    amount numeric(5,2) not null check(amount > 0.0),
    _time datetime not null,
    reason varchar(60),
    foreign key(ticket_no) references novapark.ticket(t_no)
);

create table novapark.resort_reservation (
	ticket_no char(7) not null,
    room_no smallint not null,
    foreign key(ticket_no) references novapark.ticket(t_no)
);

create table novapark.restaurant_reservation (
	ticket_no char(7) not null,
    restaurant_no tinyint not null,
    foreign key(ticket_no) references novapark.ticket(t_no)
);

create table novapark.restaurant (
	_name varchar(15) not null,
    _no tinyint primary key auto_increment,
    menu_no tinyint not null default 1,
     thumbnail varchar(75),
    capacity smallint default 50 check(capacity > 0)
);

create table novapark.meal (
	restaurant_no tinyint not null,
    _name varchar(22) not null,
    price smallint not null,
    calories smallint not null,
     thumbnail varchar(75),
    foreign key (restaurant_no) references novapark.restaurant(_no)
);

create table novapark.event_hall (
	hall_no tinyint not null,
    capacity smallint not null,
    address varchar(45) default 'Not Specified',
    thumbnail varchar(75),
    manager_no smallint,
    phone char(10),
    foreign key (manager_no) references novapark.staff(staff_no)
);

create table novapark.theme_event (
	event_no smallint primary key auto_increment,
    hall_no tinyint not null,
    _name varchar(22) not null,
    thumbnail_path varchar(45)
);

create table novapark.feedback (
	cust_name varchar(30) not null,
    _comment varchar(120),
    _date date primary key
);



describe novapark.ticket;
alter table novapark.visitor modify num_of_visitations int default 1;
describe novapark.visitor;

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
