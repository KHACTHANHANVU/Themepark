import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def generate_report(start_date, end_date):
  db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="mydatabase"
  )

  cursor = db.cursor()
  
  # Q1: get the total number of runs for each ride, the avg number of times run daily, and wether the ride is running 
  #query_1 = cursor.execute("SELECT ar.ride_name, SUM(dr.num_of_rides) AS total_runs, AVG(dr.num_of_rides) AS avg_num_runs, ar.is_working AS ride_operational FROM novapark.amusement_ride AS ar, novapark.daily_rides AS dr, WHERE ar.ride_no = dr.ride_no AND dr._date BETWEEN %s AND %s GROUP BY ar.ride_name", (start_date, end_date))

  # Q2: the number of times each ride has been repaired during the time frame and the cost of those repairs
  #query_2 = cursor.execute("SELECT ar.ride_name, COUNT(ar.ride_no) AS repair_count, SUM(rr.cost) AS total_repair_cost FROM navapark.amusement_ride AS ar, novapark.ride_repair AS rr WHERE ar.ride_no = rr.ride_no AND rr.date_of_issue >= %s AND rr.repair_date <= %s GROUP BY ar.ride_name", (start_date, end_date))

  # combined queries 1 and 2
  query = cursor.execute("""SELECT ar.ride_name,
         SUM(dr.num_of_rides) AS total_runs,
         AVG(dr.num_of_rides) AS avg_num_runs,
         IF(ar.is_working, "Yes", "No") AS ride_operational,
         COUNT(rr.ride_no) AS repair_count,
         SUM(rr.cost) AS total_repair_cost
  FROM novapark.amusement_ride AS ar
  LEFT JOIN novapark.daily_rides AS dr ON ar.ride_no = dr.ride_no AND dr._date BETWEEN %s AND %s
  LEFT JOIN novapark.ride_repair AS rr ON ar.ride_no = rr.ride_no AND rr.date_of_issue >= %s AND rr.repair_date <= %s
  GROUP BY ar.ride_name""")
  
  c = canvas.Canvas("rides_report.pdf", pagesize=letter)
  c.setFont("Helvetica", 12)
  
  # Add table data (including headers)
  headers = ('Ride Name', 'Total Rides', 'Average Daily Riders', 'Number of Repairs', 'Total Cost of Repairs', 'Ride Operational')
  data = [headers]  
  
  # Extend data with rows of actual data (formatted as tuples)
  data.extend(query)
  
  # Create a table style
  table_style = TableStyle([
      ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  
      ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
      ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
      ('GRID', (0, 0), (-1, -1), 1, colors.black),  
  ])
  
  # Create the table
  table = Table(data)
  table.setStyle(table_style)
  
  table.wrapOn(c, 400, 600)
  table.drawOn(c, 50, 700)  
  
  # Save the PDF file if needed, replace with code to diplay if needed
  # c.save()
