
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

'''
cursor = mydb.cursor()
cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)
'''
def check_login_cred(username, password):
    cookies = SimpleCookie() #os.getenv("HTTP_COOKIE") inside constructor
    cursor = mydb.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM novapark.customer AS c WHERE c.username == '%s' AND c.password == '%s';", (username, password,))
    result=cursor.fetchone() != 0

    if result:
        cookies["login"] = "true"
        cookies["access_level"] = "customer"
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
                ...
            else:
                # staff 
                cookies["login"] = "true"
                cookies["access_level"] = "staff"
                ...
        else:
            # not customer or staff member
            cookies["login"] = "false"
            cookies["access_level"] = "none"

        return cookies
