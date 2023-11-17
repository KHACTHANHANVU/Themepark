
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
                      FROM novapark.visitor AS c 
                      WHERE c.first_name = '%s' AND c.last_name = '%s';""" % (username, password,))
    result = cursor.fetchall()

    if (result[0][0]):
        return "V" # V: visitor level credentials
    else:
        cursor.execute("""  SELECT COUNT(*), IF((s.job = "manager" OR s.job = "supervisor"), 1, 0)
                            FROM novapark.staff AS s 
                            WHERE s.staff_id = '%s' AND s.pswd = '%s';""" % (username, password,))
        result = cursor.fetchall()
    if (result[0][0]):
        creds = result[0][1]
        if(creds):
            return "M" # M: manager/supervisor level credentials
        else:
            return "S" # S: staff level credentials
    return "N" # N: not in database
    