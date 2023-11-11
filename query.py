
import mysql.connector

mysql.connector

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
    cursor = mydb.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM novapark.customer AS c WHERE c.username == %s AND c.password == %s", (username, password))
    result=cursor.fetchone() != 0

    if result:
        ...
    else:
        cursor.execute("SELECT COUNT(*) FROM novapark.staff AS s WHERE s.username == %s AND s.password == %s", (username, password))
        result1=cursor.fetchone() > 0
    
        if result1:
            cursor.execute("SELECT COUNT(*) FROM novapark.staff AS s WHERE (s.username == %s AND s.password == %s) AND (s.job == \"manager\" OR s.job == \"supervisor\")", (username, password))
            result2=cursor.fetchone() > 0
            if result2:
                # manager/admin
                ...
            else:
                # staff 
                ...
        else:
            ...

    val = cursor.fetchone()
    print(val)
    if username == 'kevin' and password == 'qwerty':
        return True
    else:
        return False
