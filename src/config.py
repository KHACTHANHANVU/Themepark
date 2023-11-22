
import mysql.connector
import json
import os
from http.cookies import SimpleCookie



mydb = mysql.connector.connect(
    host="themeparkproject.mysql.database.azure.com",
    user="team3",
    password="Password1",
    database="novapark"
)

