import mysql.connector
from datetime import datetime

def generate_report(start_date, end_date):
    db = mysql.connector.connect(
       host="themeparkproject.mysql.database.azure.com",
       user="team3",
       password="Password1",
       database="novapark"
    )
  
    cursor = db.cursor()

    # reformat dates for mysql
    start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

    # Q1: total revenue of all sectors
    cursor.execute("SELECT SUM(ride_revenue + vendor_revenue +  resort_revenue + restaurant_revenue) AS total_revenue FROM novapark.business_day WHERE b_date BETWEEN %s AND %s", (start_date, end_date))

    # Q2: total expenses
    cursor.execute("SELECT SUM(vendor_expenses + resort_expenses + restauarant_expenses) AS total_expenses FROM novapark.business_day WHERE b_date BETWEEN %s AND %s", (start_date, end_date))

    # Q3: total income
    cursor.execute("SELECT (total_revenue - total_expenses) AS total_income")

    #Q4: get total revenue for each sector during the time frame
    cursor.execute("SELECT SUM(vendor_revenue) AS total_vendor_revenue, SUM(ride_revenue) AS total_ride_revenue), SUM(resort_revenue) AS total_resort_revenue) FROM novapark.business_day WHERE b_Date %s AND %s", (start_date, end_date))

    # Q5: number of items refunded and total money refuned
    cursor.execute("SELECT COUNT(ticket_no) AS num_of_refunds FROM novapark.refund WHERE _time BETWEEN %s AND %s", (start_date, end_date))

    #Q6: total expenses per department
    cursor.execute("SELECT SUM(vendor_expenses) AS total_vendor_expenses, SUM(resort_expenses) AS total_resort_expenses, SUM(restaurant_expenses) AS total_restaurant_expenses FROM novapark.business_day WHERE b_date BETWEEN %s AND %s", (start_date, end_date))

    # Q7: get income for each department
    cursor.execute("SELECT (total_vendor_revenue - total_vendor_expenses) AS total_vendor_income, (total_resort_revenue - total_resort_expenses) AS total_resort_income, (total_restaurant_revenue - total_restaurant_expenses) AS total_restaurant_income FROM novapark.business_day WHERE b_date BETWEEN %s AND %s", (start_date, end_date))

    # Q8: total income with refunds subtracted
    cursor.execute("SELECT (total_income - total_refunds) AS total_income_with_refunds FROM novapark.business_day WHERE b_date BETWEEN %s AND %s", (start_date, end_date))
