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

