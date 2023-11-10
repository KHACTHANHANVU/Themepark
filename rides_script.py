import mysql.connector

def validate_dates():
  return

def generate_report(start_date, end_date):
  db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="mydatabase"
  )

  cursor = db.cursor()
  
  # Q1: get the total number of riders for each ride
  cursor.execute("SELECT ar.ride_name, SUM(dr.num_of_rides) AS total_riders FROM novapark.amusement_ride AS ar, novapark.daily_rides AS dr WHERE ar.ride_no = dr.ride_no AND dr._date BETWEEN %s AND %s", (start_date, end_date))

  # Q2: get the average number of daily riders per ride
  cursor.execute("SELECT ar.ride_name, AVG(dr.num_of_rides) AS avg_daily_riders FROM novapark.amusement_ride AS ar, novapark.daily_rides AS dr WHERE ar.ride_no = dr.ride_no AND dr._date BETWEEN %s AND %s", (start_date, end_date))

  # Q3: the number of times each ride has been repaired
  cursor.execute("SELECT ar.ride_name, COUNT(ar.ride_no) AS repair_count FROM navapark.amusement_ride AS ar, novapark.ride_repair AS rr WHERE ar.ride_no = rr.ride_no AND rr.repair_date BETWEEN %s AND %s", (start_date, end_date))

  # Q4: total cost of repairing each ride
  cursor.execute("SELECT ar.ride_name, SUM(rr.cost) AS total_repair_cost FROM navapark.amusement_ride AS ar, novapark.ride_repair AS rr WHERE ar.ride_no = rr.ride_no AND rr.repair_date BETWEEN %s AND %s", (start_date, end_date))
