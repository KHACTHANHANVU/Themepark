
import mysql.connector
import json
import os
import datetime
from http.cookies import SimpleCookie

#cookies = SimpleCookie(os.getenv("HTTP_COOKIE"))

mydb = mysql.connector.connect(
    host="themeparkproject.mysql.database.azure.com",
    user="team3",
    password="Password1",
    database="novapark"
)

def check_login_cred(username, password):
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, email
                      FROM novapark.customer AS c 
                      WHERE c.email = '%s' AND c.pswrd = '%s';""" % (username, password))
    result = cursor.fetchall()    
    cookie = SimpleCookie()
            
    if (len(result) != 0):
        cookie["first_name"] = result[0][0]
        cookie["email"] = result[0][1]
        cookie["authorization_level"] = "V" # V: visitor level credentials
    else:
        cursor.execute("""SELECT staff_id, IF(s.job = "manager", 1, 0)
                          FROM novapark.staff AS s 
                          WHERE s.staff_id = '%s' AND s.pswrd = '%s';""" % (username, password,))
        result = cursor.fetchall()
        if (len(result) != 0):
            cookie["staff_id"] = result[0][0]
            if result[0][1] == 1:
                cookie["authorization_level"] = "M" # M: manager/supervisor level credentials
            else:
                cookie["authorization_level"] = "S" # S: staff level credentials
        else:        
            cookie["authorization_level"] = "N" # N: not in database
    return cookie
    
def sign_up(first_name, last_name, phone_num, username, password):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.customer (first_name, last_name, pswrd, email, phone, pass_credits)
                      VALUES ('%s', '%s', '%s', '%s', '%s', 0);""" % (first_name, last_name, password, username, phone_num))
    mydb.commit()
    cursor.execute("""SELECT * FROM novapark.customer;""")
    result = cursor.fetchall()
    print(result)
    
    cookie = SimpleCookie()
    cookie["first_name"] = first_name
    cookie["email"] = username
    cookie["authorization_level"] = "V"
    
    return cookie

def load_profile(username):
    print(username)
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, email, phone, pass_credits
                      FROM novapark.customer as c
                      WHERE c.email = '%s';""" % (username,))
    result = cursor.fetchall()
    
    return result


def load_event_edit(event_no):
    cursor = mydb.cursor()
    cursor.execute("""SELECT event_no, manager_id, e_name, e_descrip, start_date, end_date
                      FROM novapark.events as e
                      WHERE e.event_no = %s;""" % (event_no,))
    result = cursor.fetchall()
    return result

def load_profile_edit(username):
    print(username)
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, phone, pswrd
                      FROM novapark.customer as c
                      WHERE email = '%s';""" % (username,))
    result = cursor.fetchall()
    return result

def load_staff_profile(username):
    print(username)
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, staff_id, pswrd, phone_no, addrs, supervisor_id, dob, hourly_wage, job
                      FROM novapark.staff
                      WHERE staff_id = %s;""" % (username,))
    result = cursor.fetchall()
    return result

def load_mgr_edit(username):
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, pswrd, phone_no, addrs, supervisor_id, hourly_wage, dob, job                      
                      FROM novapark.staff
                      WHERE staff_id = %s;""" % (username,))
    result = cursor.fetchall()
    return result

def load_mgr_edit_staff(username):
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, supervisor_id, hourly_wage, job
                      FROM novapark.staff
                      WHERE staff_id = %s;""" % (username,) )
    result = cursor.fetchall()
    return result

def load_staff_edit(username):
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, pswrd, phone_no, addrs
                      FROM novapark.staff
                      WHERE staff_id = %s;""" % (username,) )
    result = cursor.fetchall()
    return result

def load_events():
    cursor = mydb.cursor()
    cursor.execute("""SELECT e_name, e_descrip, manager_id, start_date, end_date, event_no
                      FROM novapark.events;""")
    result = cursor.fetchall()
    return result

def load_staff():
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, staff_id, pswrd, phone_no, addrs, dob, supervisor_id, job, hourly_wage
                      FROM novapark.staff;""")
    result = cursor.fetchall()
    return result

def load_customers():
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, email, pswrd, phone, pass_credits
                      FROM novapark.customer;""")
    result = cursor.fetchall()
    return result


def load_customers_edit(email):
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, email, pswrd, phone, pass_credits
                      FROM novapark.customer
                      WHERE email = '%s';""" % (email,))
    result = cursor.fetchall()
    return result

def load_rides():
    cursor = mydb.cursor()
    cursor.execute("""SELECT ride_name, ride_no, IF (is_working, "TRUE", "FALSE"), date_of_last_repair
                      FROM novapark.amusement_ride;""")
    result = cursor.fetchall()
    return result

def load_rides_cust():
    cursor = mydb.cursor()
    cursor.execute("""SELECT ride_name, ride_no
                      FROM novapark.amusement_ride
                      WHERE is_working = 1;""")
    result = cursor.fetchall()
    return result

def load_hours_worked(staff_id, date):
    print(date)
    cursor = mydb.cursor()
    cursor.execute("""SELECT num_hours
                      FROM novapark.hours_worked
                      WHERE staff_id = %s AND cur_date = '%s';""" % (staff_id, date))
    result = cursor.fetchall()
    return result

def load_bday():
    cursor = mydb.cursor()
    cursor.execute("""SELECT *
                      FROM novapark.business_day
                      ORDER BY b_date DESC;""")
    result = cursor.fetchall()
    return result

def update_customer(email, first_name, last_name, phone_num, password, last_pass_credit_date):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.customer
                      SET first_name = '%s', last_name = '%s', pswrd = '%s', phone = '%s',
                      last_pass_credit_date = '%s'
                      WHERE email = '%s';""" % (first_name, last_name, password, phone_num, last_pass_credit_date, email))
    mydb.commit()


def update_profile(email, first_name, last_name, phone_num, password):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.customer
                      SET first_name = '%s', last_name = '%s', phone = '%s',
                      pswrd = '%s'
                      WHERE email = '%s';""" % (first_name, last_name, phone_num, password, email))
    mydb.commit()

def update_mgr_level(staff_id, first_name, last_name, phone_num, address, sup_id, password, hourly_wage, dob, job):
    cursor = mydb.cursor()
    print(staff_id, first_name, last_name, phone_num, address, password, hourly_wage, dob, job)

    cursor.execute("""UPDATE novapark.staff
                      SET first_name = '%s', last_name = '%s', pswrd = '%s', phone_no = '%s', addrs = '%s', supervisor_id = %s, 
                      hourly_wage = %s, dob = '%s', job = '%s'
                      WHERE staff_id = '%s';""" % (first_name, last_name, password, phone_num, address, sup_id, hourly_wage, dob, job, staff_id))
    mydb.commit()

def update_staff_profile(staff_id, first_name, last_name, phone_num, address, password):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.staff
                      SET first_name = '%s', last_name = '%s', phone_no = '%s', addrs = '%s', pswrd = '%s'
                      WHERE staff_id = '%s';""" % (first_name, last_name, phone_num, address, password, staff_id))
    mydb.commit()

def update_staff_level(staff_id, first_name, last_name, sup_id, job, hourly_wage):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.staff
                      SET first_name = '%s', last_name = '%s', supervisor_id = %s, job = '%s', hourly_wage = %s
                      WHERE staff_id = %s;""" % (first_name, last_name, sup_id, job, hourly_wage, staff_id))
    mydb.commit()

def update_hours_worked(staff_id, hours_worked):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.hours_worked
                      SET num_hours = %s
                      WHERE staff_id = %s;""" % (hours_worked, staff_id))
    mydb.commit()

def update_repair_log(ride_no, date_of_issue, repair_date, repair_cost):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.repair_log
                      SET repair_date = '%s', repair_cost = %s
                      WHERE ride_no = %s AND date_of_issue = '%s';""" % (repair_date, repair_cost, ride_no, date_of_issue))
    mydb.commit()

def update_ride(ride_no, ride_name, is_working, date_of_last_repair):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.amusement_ride
                      SET ride_name = '%s', is_working = %s, date_of_last_repair = '%s'
                      WHERE ride_no = %s;""" % (ride_name, is_working, date_of_last_repair, ride_no))
    mydb.commit()

def update_event(event_num, event_name, event_descrip, sup_id, start_date, end_date):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.events
                      SET e_name = '%s', e_descrip = '%s', manager_id = %s, start_date = '%s', end_date = '%s'
                      WHERE event_no = %s;""" % (event_name, event_descrip, sup_id, start_date, end_date, event_num))
    mydb.commit()

def update_bday(date, revenue, expenses):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.business_day
                      SET revenue = %s, expenses = %s
                      WHERE b_date = '%s';""" % (revenue, expenses, date))

def rides_report(start_date, end_date):
    cursor = mydb.cursor()
    cursor.execute("""SELECT ar.ride_name, ar.ride_no, ar.date_of_last_repair, 
                      repair_count, total_repair_cost
                      AS total_cost_of_repairs, IF(ar.is_working = 1, 'Yes', 'No') AS operational
                      FROM novapark.amusement_ride ar
                      LEFT JOIN (
                          SELECT ride_no, COUNT(*) AS repair_count, SUM(repair_cost) AS 
                          total_repair_cost
                          FROM novapark.ride_repair
                          WHERE repair_date BETWEEN '%s' AND '%s'
                          GROUP BY ride_no
                      ) rr ON ar.ride_no = rr.ride_no
                      ORDER BY ar.ride_name;""" % (start_date, end_date))
    result = cursor.fetchall()
    return result

def employee_wages(start_date, end_date):
    cursor = mydb.cursor()
    # Q1: get list of all staff ids
    cursor.execute("""SELECT staff_id, hourly_wage
                      FROM novapark.staff;""")
    staff_ids = cursor.fetchall()

    wage_expenses = 0
    for tuple in staff_ids:
        # Q2: get number of hours worked in time frame for each employee
        cursor.execute("""SELECT SUM(num_hours)
                            FROM novapark.hours_worked
                            WHERE staff_id = %s AND cur_date BETWEEN '%s' AND '%s';""" % (tuple[0], start_date, end_date)) 
        num_hours = cursor.fetchall()
        num_hours = num_hours[0][0] if num_hours[0][0] else 0
        wage_expenses = tuple[1] * num_hours
    return wage_expenses

def revenue_report(start_date, end_date):
    cursor = mydb.cursor()

    # Q1: get the total revenue and expenses from business day
    cursor.execute("""SELECT SUM(revenue), SUM(expenses)
                      FROM novapark.business_day as b
                      WHERE b.b_date BETWEEN '%s' AND '%s';""" % (start_date, end_date))
    result1 = cursor.fetchall()

    # Q2: get total ticket revenue
    cursor.execute("""SELECT SUM(sale_cost)
                      FROM novapark.park_pass as p
                      WHERE p.date_bought BETWEEN '%s' AND '%s';""" % (start_date, end_date))
    result2 = cursor.fetchall()

    # Q3: get total expenses from repairs
    cursor.execute("""SELECT SUM(repair_cost)
                      FROM novapark.ride_repair as r
                      WHERE r.date_of_issue BETWEEN '%s' AND '%s';""" % (start_date, end_date))
    result3 = cursor.fetchall()

    wage_expenses = employee_wages(start_date, end_date)
    
    return result1, result2, result3, wage_expenses

def insert_ticket_purchase(card_first_name, card_last_name, ticket_type, card_number, cvv, exp_month, exp_year, email, num_tickets):
    cost = 0
    ticket_type = ticket_type.capitalize()
    cur_time = datetime.datetime.now()
    print(cost)

    if ticket_type == "Silver":
        cost = int(num_tickets) * 20
    elif ticket_type == "Gold":
        cost = int(num_tickets) * 30
    else:
        cost = int(num_tickets) * 60
        
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.park_pass (cust_email, num_passes, sale_cost, 
                      pass_type, date_bought, card_fname, card_lname, card_num, cvv, exp_month,
                      exp_year)
                      VALUES ('%s', %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" 
                      % (email, num_tickets, cost, ticket_type, cur_time, card_first_name, card_last_name, card_number, cvv, exp_month, exp_year))
    mydb.commit()
    return "Yay!"

def view_tickets(email):
    cursor = mydb.cursor()
    cursor.execute("""SELECT SUM(num_passes)
                      FROM novapark.park_pass
                      WHERE  cust_email = '%s' AND pass_type = '%s';""" % (email, 'Silver'))
    num_silver = cursor.fetchall()
    
    cursor.execute("""SElECT SUM(num_passes)
                      FROM novapark.park_pass
                      WHERE cust_email = '%s' AND pass_type = '%s';""" % (email, 'Gold'))
    num_gold = cursor.fetchall()
    
    cursor.execute("""SElECT SUM(num_passes)
                      FROM novapark.park_pass
                      WHERE cust_email = '%s' AND pass_type = '%s';""" % (email, 'Platinum'))
    num_platinum = cursor.fetchall()

    num_silver = num_silver[0][0] if num_silver[0][0] else 0
    num_gold = num_gold[0][0] if num_gold[0][0] else 0
    num_platinum = num_platinum[0][0] if num_platinum[0][0] else 0


    return num_silver, num_gold, num_platinum

def view_hours_worked(staff_id):
    cursor = mydb.cursor()
    cursor.execute("""SELECT cur_date, num_hours
                      FROM novapark.hours_worked
                      WHERE staff_id = %s
                      ORDER BY cur_date DESC;""" % (staff_id,))
    result = cursor.fetchall()
    return result

def add_staff(sup_id, first_name, last_name, password, phone_num, address, dob, job, hourly_wage):
    address = address.replace("+", " ")
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.staff (first_name, last_name, pswrd, phone_no, addrs, dob, job, hourly_wage, supervisor_id)
                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s);""" 
                      % (first_name, last_name, password, phone_num, address, dob, job, hourly_wage, sup_id))
    mydb.commit()
    return "Yay"

def add_repair_log(ride_no, date_of_issue, repair_date, repair_cost):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.ride_repair (ride_no, date_of_issue, repair_date, repair_cost)
                      VALUES (%s, '%s', '%s', %s);""" 
                      % (ride_no, date_of_issue, repair_date, repair_cost))
    mydb.commit()
    return "Yay"

def add_ride(ride_name):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.amusement_ride (ride_name, is_working)
                      VALUES ('%s', %s);""" % (ride_name, 1))
    mydb.commit()
    return "Yay"

def add_event(sup_id, event_name, event_descrip, start_date, end_date):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.events (manager_id, e_name, e_descrip, start_date, end_date)
                      VALUES (%s, '%s', '%s', '%s', '%s');""" % (sup_id, event_name, event_descrip, start_date, end_date))
    mydb.commit()
    return "Yay"

def add_hours(staff_id, hours, date):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.hours_worked (staff_id, num_hours, cur_date)
                      VALUES (%s, %s, '%s');""" % (staff_id, hours, date))
    mydb.commit()

def add_bday(date, revenue, expenses):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.business_day (b_date, revenue, expenses)
                      VALUES ('%s', %s, %s);""" % (date, revenue, expenses))
    mydb.commit()

def del_staff(staff_id):
    cursor = mydb.cursor()
    cursor.execute("""DELETE FROM novapark.staff
                      WHERE staff_id = %s;""" % (staff_id,))
    mydb.commit()
    return "Del"

def del_customer(email):
    cursor = mydb.cursor()
    cursor.execute("""DELETE FROM novpark.customer
                      WHERE email = '%s';""" % (email,))
    mydb.commit()
    return "Del"

def del_event(event_num):
    cursor = mydb.cursor()
    cursor.execute("""DELETE FROM novapark.events
                      WHERE event_no = %s;""" % (event_num,))
    mydb.commit()
    return "Del"


def del_ride(ride_no):
    cursor = mydb.cursor()
    cursor.execute("""DELETE FROM novapark.amusement_ride
                      WHERE ride_no = %s;""" % (ride_no,))
    mydb.commit()
    return "Del"

def del_bday(date):
    cursor = mydb.cursor()
    cursor.execute("""DELETE FROM novapark.business_day
                      WHERE b_date = '%s';""" % (date,))
    mydb.commit()

def del_hours(date):
    cursor = mydb.cursor()
    cursor.execute("""DELETE FROM novapark.hours_worked
                       WHERE cur_date = '%s';""" % (date,))
    mydb.commit()