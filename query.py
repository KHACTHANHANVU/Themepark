
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
    if username == 'kevin' and password == 'qwerty':
        return True
    else:
        return False