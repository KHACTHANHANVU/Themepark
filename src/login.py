
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
                      FROM novapark.customer  
                      WHERE email = '%s';""" % (username,))
    result = cursor.fetchall()
    
    return result

def load_profile_edit(username):
    print(username)
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, phone, pswrd
                      FROM novapark.customer  
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

def load_staff_edit(username):
    cursor = mydb.crsor()
    cursor.execute("""SELECT first_name, last_name, pswrd, phone_no, addrs
                      FROM novapark.staff
                      WHERE staff_id = %s;""" % (username,) )

def load_events():
    cursor = mydb.cursor()
    cursor.execute("""SELECT e_name, e_descrip, manager_id, start_date, end_date
                      FROM novapark.events;""")
    result = cursor.fetchall()
    return result

def load_staff():
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, staff_id, phone_no, addrs, dob, supervisor_id, job, hourly_wage
                      FROM novapark.staff;""")
    result = cursor.fetchall()
    return result

def load_customers():
    cursor = mydb.cursor()
    cursor.execute("""SELECT first_name, last_name, email, pswrd, phone, pass_credits
                      FROM novapark.customer;""")
    result = cursor.fetchall()
    return result

def load_rides():
    cursor = mydb.cursor()
    cursor.execute("""SELECT ride_name, ride_no, is_working, date_of_last_repair
                      FROM novapark.amusement_ride;""")
    result = cursor.fetchall()
    return result

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

def update_staff_level(staff_id, first_name, last_name, phone_num, address, password):
    cursor = mydb.cursor()
    cursor.execute("""UPDATE novapark.staff
                      SET first_name = '%s', last_name = '%s', phone_no = '%s', addrs = '%s', pswrd = '%s'
                      WHERE staff_id = '%s';""" % (first_name, last_name, phone_num, address, password, staff_id))
    mydb.commit()

def ride_report(start_date, end_date):
    cursor = mydb.cursor()
    cursor.execute("""SELECT ar.ride_name, ar.ride_no, ar.date_of_last_repair, 
                      COALESCE(repair_count, 0) AS times_repaired, COALESCE(total_repair_cost, 0.0)
                      AS total_cost_of_repairs, ar.is_working
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

def insert_ticket_purchase(card_first_name, card_last_name, ticket_type, card_number, cvv, exp_month, exp_year, email, num_tickets):
    cost = 0
    ticket_type = ticket_type.capitalize()
    cur_time = datetime.datetime.now()
    if(ticket_type == "Silver"):
        cost = num_tickets * 20
    elif(ticket_type == "Gold"):
        cost = num_tickets * 30
    else:
        cost = num_tickets * 60
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.park_pass (cust_email, num_passes, sale_cost, 
                      pass_type, date_bought, card_fname, card_lname, card_num, cvv, exp_month,
                      exp_year)
                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" 
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

def add_staff(sup_id, first_name, last_name, password, phone_num, address, dob, job, hourly_wage):
    address = address.replace("+", " ")
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.staff (first_name, last_name, pswrd, phone, addrs, dob, job, hourly_wage, supervisor_id)
                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s);""" 
                      % (first_name, last_name, password, phone_num, address, dob, job, hourly_wage, sup_id))
    return "Yay"

def add_ride(ride_name):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.amusement_ride (ride_name, is_working)
                      VALUES ('%s', %s);""" % (ride_name, 1))
    return "Yay"

def add_event(sup_id, event_name, event_descrip, start_date, end_date):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.events (manager_id, e_name, e_descrip, start_date, end_date)
                      VALUES (%s, '%s', '%s', '%s', '%s');""" % (sup_id, event_name, event_descrip, start_date, end_date))
    return "Yay"

def del_staff(staff_id):
    cursor = mydb.cursor()
    #cursor.execute(""";""")
    return "Del"

def del_customer(email):
    cursor = mydb.cursor()
    #cursor.execute(""";""")
    return "Del"

def del_event(event_num):
    cursor = mydb.cursor()
    #cursor.execute(""";""")
    return "Del"


def del_ride(ride_no):
    cursor = mydb.cursor()
    #cursor.execute(""";""")
    return "Del"