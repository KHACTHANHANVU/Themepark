import mysql.connector
from datetime import datetime

def generate_report(dept_name, fname, lname, min_wage, max_wage):
    db = mysql.connector.connect(
        host="themeparkproject.mysql.database.azure.com",
        user="team3",
        password="Password1",
        database="novapark"
    )

    cursor = db.cursor()

    # reformat dates for mysql
    query = ""
    if(fname == "" or lname == ""):
      # Q1: wihtout name
      query = cursor.execute("SELECT s.fname AS first_name, s.lname AS last_name, s.staff_no AS staff_number, s.address, s.week_wage AS weekly_wage, s.job, d.d_name AS dept_name, d.d_no AS dept_num FROM novapark.department AS d, novapark.staff AS s WHERE d.d_name == %s AND d.d_no == s.d_no AND s.week_wage BETWEEN %s AND %s GROUP BY d.d_name;", (dept_name, min_wage, max_wage))
    elif(min_wage == 0 and max_wage == 0):
      # Q2: wihtout wage
      query = cursor.execute("SELECT s.fname AS first_name, s.lname AS last_name, s.staff_no AS staff_number, s.address, s.job, d.d_name AS dept_name, d.d_no AS dept_num FROM novapark.department AS d, novapark.staff AS s WHERE d.d_name == %s AND d.d_no == s.d_no AND s.fname == %s AND s.lname == %s GROUP BY d.d_name;", (dept_name, fname, lname))
    else:
      # Q3: all params
      query = cursor.execute("SELECT s.fname AS first_name, s.lname AS last_name, s.staff_no AS staff_number, s.address, s.week_wage AS weekly_wage, s.job, d.d_name AS dept_name, d.d_no AS dept_num FROM novapark.department AS d, novapark.staff AS s WHERE d.d_name == %s AND d.d_no == s.d_no AND s.fname == %s AND s.lname == %s AND s.week_wage BETWEEN %s AND %s GROUP BY d.d_name;", (dept_name, fname, lname, min_wage, max_wage))