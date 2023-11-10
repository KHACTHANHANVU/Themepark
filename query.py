
import mysql.connector

mydb = mysql.connector.connect(
  host="themeparkproject.mysql.database.azure.com",
  user="team3",
  password="Password1",
  database="novapark"
)

cursor = mydb.cursor()
cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)
