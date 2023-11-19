
import mysql.connector
import json
import os
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
    
    #cursor.execute("SELECT COUNT(*) FROM novapark.customer AS c WHERE c.username == %s AND c.password == %s;", (username, password,))
    cursor.execute("""SELECT COUNT(*)
                      FROM novapark.customer AS c 
                      WHERE c.email = '%s' AND c.pswrd = '%s';""" % (username, password,))
    result = cursor.fetchall()
    
    cookie = SimpleCookie()
    
    print(result)

    if (result[0][0]):
        cookie["authorization_level"] = "V" # V: visitor level credentials
    else:
        cursor.execute("""SELECT COUNT(*), IF(s.job = "manager", 1, 0)
                          FROM novapark.staff AS s 
                          WHERE s.staff_id = '%s' AND s.pswrd = '%s';""" % (username, password,))
        result = cursor.fetchall()
        if (result[0][0]):
            creds = result[0][1]
            if(creds):
                cookie["authorization_level"] = "M" # M: manager/supervisor level credentials
            else:
                cookie["authorization_level"] = "S" # S: staff level credentials
        else:        
            cookie["authorization_level"] = "N" # N: not in database
    return cookie
    
def sign_up(first_name, last_name, phone_num, username, password):
    cursor = mydb.cursor()
    cursor.execute("""INSERT INTO novapark.customer (first_name, last_name, pswrd, email, phone, pass_credits, num_passes)
                      VALUES ('%s', '%s', '%s', '%s', '%s', 0, 0);""" % (first_name, last_name, password, username, phone_num))
    mydb.commit()
    cursor.execute("""SELECT * FROM novapark.customer;""")
    result = cursor.fetchall()
    print(result)
    return "yay"