# Themepark (Python Branch)

This is the official repository for the COSC 3380 Team 3 project. We were asked to design a themepark, and we were able to implement some basic functions, such as customers buying tickets and seeing tickets bought, as well as staff being able to log hours, log repairs needed for rides, and [log possible injuries]. Finally, managers are able to log in to add new events, rides, and staff, as well as log in business expenses, and get reports for revenue and [...] Managers are also able to edit staff information, from password for logging in to the amount they are paid hourly.

To see this site, go to http://themeparkproject.azurewebsites.net/, or to run it locally, make sure you have Python 3.11 or greater downloaded. It also requires the mysql-connector-python module, which can be installed using pip3.

Run python3 main.py and the website should be up. Go to localhost:8000 to see the website hosted locally.

This branch used a Python backend rather than NodeJS. The reason why was that almost all examples of NodeJS online used the express framework, and given that we couldn't use any frameworks, the first example we found was one using Python.