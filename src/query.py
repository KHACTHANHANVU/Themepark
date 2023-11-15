
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
    cookies = SimpleCookie() #os.getenv("HTTP_COOKIE") inside constructor
    cursor = mydb.cursor()
    
    #cursor.execute("SELECT COUNT(*) FROM novapark.customer AS c WHERE c.username == %s AND c.password == %s;", (username, password,))
    cursor.execute("""SELECT COUNT(*)
                        FROM novapark.visitor AS c 
                        WHERE c.first_name = '%s' AND c.last_name = '%s';""" % (username, password,))
    result=cursor.fetchone() != 0
    print(result)

    if result:
        cookies["login"] = "true"
        cookies["access_level"] = "customer"
        cookies["username"] = username
        cookies["password"] = password
    else:
        cursor.execute("SELECT COUNT(*) FROM novapark.staff AS s WHERE s.username == %s AND s.password == %s;", (username, password))
        result1=cursor.fetchone() != 0
    
        if result1:
            cursor.execute("SELECT COUNT(*) FROM novapark.staff AS s WHERE (s.username == %s AND s.password == %s) AND (s.job == \"manager\" OR s.job == \"supervisor\");", (username, password))
            result2=cursor.fetchone() != 0
            if result2:
                # manager/admin
                cookies["login"] = "true"
                cookies["access_level"] = "manager"
                cookies["username"] = username
                cookies["password"] = password
            else:
                # staff 
                cookies["login"] = "true"
                cookies["access_level"] = "staff"
                cookies["username"] = username
                cookies["password"] = password
        else:
            # not customer or staff member
            cookies["login"] = "false"
            cookies["access_level"] = "none"

    return True
