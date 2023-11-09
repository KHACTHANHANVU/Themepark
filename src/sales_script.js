function validateDates() {
    const startDateStr = document.getElementById('startDate').value;
    const endDateStr = document.getElementById('endDate').value;

    // Define the date pattern (MM/DD/YYYY)
    const datePattern = /^\d{2}\/\d{2}\/\d{4}$/;

    if (!datePattern.test(startDateStr) || !datePattern.test(endDateStr)) {
        document.getElementById('message').textContent = 'Please enter dates in the MM/DD/YYYY format.';
        return; // Exit the function if the format is incorrect
    }

    // Parse the entered dates
    const startDate = new Date(startDateStr);
    const endDate = new Date(endDateStr);

    // Check if the parsed dates are valid
    if (isNaN(startDate)) {
        document.getElementById('message').textContent = 'Please enter valid start date.';
    } 
    else if (isNaN(endDate)) {
      document.getElementById('message').textContent = 'Please enter valid end date.';
    }
    else {
        document.getElementById('message').textContent = `Start Date: ${startDate.toLocaleDateString()}, End Date: ${endDate.toLocaleDateString()}`;
        generate_report(startDate, startDate)
    }
}


function generate_report(startDate, endDate) {
  const mysql = require('mysql');


  const connection = mysql.createConnection({
    host: 'your_mysql_host',
    user: 'your_mysql_user',
    password: 'your_mysql_password',
    database: 'your_database_name',
  });


  connection.connect((err) => {
    if (err) {
      console.error('Error connecting to the database: ' + err.stack);
      return;
    }
    console.log('Connected to the database');
  });

  // Query 1: Get the total revenue of all departments
  connection.query(
    `SELECT SUM(ride_revenue + vendor_revenue + resort_revenue + restaurant_revenue) AS total_revenue
     FROM novapark.business_day
     WHERE b_date BETWEEN ? AND ?`,
    [start_date, end_date],
    (error, results, fields) => {
      if (error) throw error;
      console.log('Total Revenue: ', results[0].total_revenue);
    }
  );

  // Query 2: Get total money spent (expenses)
  connection.query(
    `SELECT SUM(vendor_expenses + resort_expenses + restaurant_expenses) AS total_expenses
     FROM novapark.business_day
     WHERE b_date BETWEEN ? AND ?`,
    [start_date, end_date],
    (error, results, fields) => {
      if (error) throw error;
      console.log('Total Expenses: ', results[0].total_expenses);
    }
  );

  // Query 3: Get total income (revenue - expenses)
  connection.query(
    `SELECT (total_money_earned - total_expenses) AS total_income
     FROM (SELECT SUM(ride_revenue + vendor_revenue + resort_revenue + restaurant_revenue) AS total_money_earned
           FROM novapark.business_day
           WHERE b_date BETWEEN ? AND ?) AS total_revenue_subquery, 
          (SELECT SUM(vendor_expenses + resort_expenses + restaurant_expenses) AS total_expenses
           FROM novapark.business_day
           WHERE b_date BETWEEN ? AND ?) AS total_expenses_subquery`,
    [start_date, end_date, start_date, end_date],
    (error, results, fields) => {
      if (error) throw error;
      console.log('Total Income: ', results[0].total_income);
    }
  );

  // Query 4: Get total revenue for each department during the time frame
  connection.query(
    `SELECT SUM(vendor_revenue) AS total_vendor_revenue, SUM(ride_revenue) AS total_ride_revenue, SUM(resort_revenue) AS total_resort_revenue
     FROM novapark.business_day
     WHERE b_date BETWEEN ? AND ?`,
    [start_date, end_date],
    (error, results, fields) => {
      if (error) throw error;
      console.log('Total Vendor Revenue: ', results[0].total_vendor_revenue);
      console.log('Total Ride Revenue: ', results[0].total_ride_revenue);
      console.log('Total Resort Revenue: ', results[0].total_resort_revenue);
    }
  );

  // Query 5: Number of items refunded and the total money refunded
  connection.query(
    `SELECT COUNT(ticket_no) AS num_of_refunds, SUM(amount) AS total_refunds
     FROM novapark.refund
     WHERE _time BETWEEN ? AND ?`,
    [start_date, end_date],
    (error, results, fields) => {
      if (error) throw error;
      console.log('Number of Refunds: ', results[0].num_of_refunds);
      console.log('Total Refund Amount: ', results[0].total_refunds);
    }
  );

  // Query 6: Get total expenses per department
  connection.query(
    `SELECT SUM(vendor_expenses) AS total_vendor_expenses, SUM(resort_expenses) AS total_resort_expenses, SUM(restaurant_expenses) AS total_restaurant_expenses
     FROM novapark.business_day
     WHERE b_date BETWEEN ? AND ?`,
    [start_date, end_date],
    (error, results, fields) => {
      if (error) throw error;
      console.log('Total Vendor Expenses: ', results[0].total_vendor_expenses);
      console.log('Total Resort Expenses: ', results[0].total_resort_expenses);
      console.log('Total Restaurant Expenses: ', results[0].total_restaurant_expenses);
    }
  );

  // Query 7: Get income for each department
  connection.query(
    `SELECT (total_vendor_revenue - total_vendor_expenses) AS total_vendor_income, 
            (total_resort_revenue - total_resort_expenses) AS total_resort_income, 
            (total_resaurant_revenue - total_restaurant_expenses) AS total_restaurant_income
     FROM (SELECT SUM(vendor_revenue) AS total_vendor_revenue, SUM(ride_revenue) AS total_ride_revenue, SUM(resort_revenue) AS total_resort_revenue
           FROM novapark.business_day
           WHERE b_date BETWEEN ? AND ?) AS total_revenue_subquery, 
          (SELECT SUM(vendor_expenses) AS total_vendor_expenses, SUM(resort_expenses) AS total_resort_expenses, SUM(restaurant_expenses) AS total_restaurant_expenses
           FROM novapark.business_day
           WHERE b_date BETWEEN ? AND ?) AS total_expenses_subquery`,
    [start_date, end_date, start_date, end_date],
    (error, results, fields) => {
      if (error) throw error;
      console.log('Total Vendor Income: ', results[0].total_vendor_income);
      console.log('Total Resort Income: ', results[0].total_resort_income);
      console.log('Total Restaurant Income: ', results[0].total_restaurant_income);
    }
  );

  connection.end((err) => {
    if (err) {
      console.error('Error closing the database connection: ' + err.stack);
      return;
    }
    console.log('Connection closed');
  });

}