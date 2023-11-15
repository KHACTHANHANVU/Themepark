function validateDates() {
	const startDateStr = document.getElementById('startDate').value;
	const endDateStr = document.getElementById('endDate').value;

	console.log(startDateStr);
	console.log(endDateStr);

	// Define the date pattern (YYYY/MM/DD)
  	const datePattern = /^\d{4}-\d{2}-\d{2}$/;

  	if (!datePattern.test(startDateStr) || !datePattern.test(endDateStr)) {
    	document.getElementById('message').textContent = 'Please enter dates in the MM/DD/YYYY format.';
    	return; // Exit the function if the format is incorrect
  	}

  	// Parse the entered dates
  	const startDate = new Date(startDateStr);
  	const endDate = new Date(endDateStr);

  	// Check if the parsed dates are valid
  	if (isNaN(startDate)) {
    	alert('please enter a valid start date');
    	document.getElementById('message').textContent = 'Please enter valid start date.';
  	} else if (isNaN(endDate)) {
    	alert('Please enter a valid end date');
    	document.getElementById('message').textContent = 'Please enter valid end date.';
  	} else {
    	json = {
    		startDate: startDate,
      		endDate: endDate
    	};
    	document.getElementById('message').textContent = `Start Date: ${startDate.toLocaleDateString()}, End Date: ${endDate.toLocaleDateString()}`;
    	fetch("/rides", {
			method: "POST",
      		headers: {"Content-Type": "application/json"},
			body: JSON.stringify(json)
    	});
  	}
}