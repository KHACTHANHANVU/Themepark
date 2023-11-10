function validateDates() {
  alert('can you even see me')
  const startDateStr = document.getElementById('startDate').value;
  const endDateStr = document.getElementById('endDate').value;

  console.log(startDate);
  console.log(endDate);

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
    alert("first error");
    document.getElementById('message').textContent = 'Please enter valid start date.';
  } 
  else if (isNaN(endDate)) {
    alert("second error");
    document.getElementById('message').textContent = 'Please enter valid end date.';
  }
  else {
    alert("somehow success?");
    json = {
      startDate: startDate,
      endDate: endDate
    };
    document.getElementById('message').textContent = `Start Date: ${startDate.toLocaleDateString()}, End Date: ${endDate.toLocaleDateString()}`;
    fetch("/rides", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(json)
    });
    generate_report(startDate, startDate)
  }
}


function generate_report(start_date, end_date) {
  // Query 1: Get the total number of riders for each ride
  const query1 = `
    SELECT
        ar.ride_name,
        SUM(dr.num_of_rides) AS total_riders
    FROM
        novapark.amusement_ride ar
    LEFT JOIN
        novapark.daily_rides dr ON ar.ride_no = dr.ride_no
    GROUP BY
        ar.ride_name;
  `;

  // Query 2: Get the average number of daily riders per ride
  const query2 = `
    SELECT
        ar.ride_name,
        AVG(dr.num_of_rides) AS avg_daily_riders
    FROM
        novapark.amusement_ride ar
    LEFT JOIN
        novapark.daily_rides dr ON ar.ride_no = dr.ride_no
    GROUP BY
        ar.ride_name;
  `;

  // Query 3: Get the number of times each ride has been repaired
  const query3 = `
    SELECT
        ar.ride_name,
        COUNT(rr.ride_no) AS repair_count
    FROM
        novapark.amusement_ride ar
    LEFT JOIN
        novapark.ride_repair rr ON ar.ride_no = rr.ride_no
    GROUP BY
        ar.ride_name;
  `;

  // Query 4: Get the total cost of repairing each ride
  const query4 = `
    SELECT
        ar.ride_name,
        SUM(rr.cost) AS total_repair_cost
    FROM
        novapark.amusement_ride ar
    LEFT JOIN
        novapark.ride_repair rr ON ar.ride_no = rr.ride_no
    GROUP BY
        ar.ride_name;
  `;

  connection.query(query1, (err, results1) => {
    if (err) {
      console.error('Error executing query 1:', err);
    } else {
      console.log('Query 1 results:', results1);
    }
  });

  connection.query(query2, (err, results2) => {
    if (err) {
      console.error('Error executing query 2:', err);
    } else {
      console.log('Query 2 results:', results2);
    }
  });

  connection.query(query3, (err, results3) => {
    if (err) {
      console.error('Error executing query 3:', err);
    } else {
      console.log('Query 3 results:', results3);
    }
  });

  connection.query(query4, (err, results4) => {
    if (err) {
      console.error('Error executing query 4:', err);
    } else {
      console.log('Query 4 results:', results4);
    }
  });
}