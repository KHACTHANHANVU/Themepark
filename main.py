import http.server
import socketserver
from urllib import parse 
import re
from src import *
from src.login import *
import json
from http.cookies import SimpleCookie
from string import Template

PORT = 8000

class ThemeParkHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """
        This function handles GET requests from the browser.
        
        When the client first logs in, it sends a request to the root. Take the carousel.html and send it right back
        Link to different pages depending on whether the client is a customer, a staff member, or a manager.
        
        Template html files are used for displaying results. Link these template files with the information from the queries
        to send a "compiled" html file which contains everything the client was looking for.
        """
        urlinfo = parse.urlparse(self.path)
        urlinfo.path
        
        if (urlinfo.path == '/'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/carousel.html", "rb").read()
            finally:
                ...
            # print(file)
            self.wfile.write(file)
        elif (urlinfo.path == '/buyticket'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/buy_ticket.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/connect'):
            print(self.headers['Cookie'])
            # cookie = json.loads(self.rfile.read(length))
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/connect.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/editprofile'):
            info = self.headers['Cookie'].split("; ")
            email_pair = [pair for pair in info if pair.startswith('email=')]
            email = email_pair[0].split('=')[1]
            print(email)
            profile_info = load_profile_edit(email)
            print(profile_info)
            email = email.replace("%40", "@")
            
            first_name = profile_info[0][0]
            last_name = profile_info[0][1]
            phone = profile_info[0][2]
            password = profile_info[0][3]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/editprofile.html', 'r') as file:
                html = file.read()
                
            template_html = Template(html)

            updated_html = template_html.substitute(first_name=first_name, last_name=last_name, phone_num = phone, password = password) # .format(first_name = first_name, last_name = last_name, phone_num = phone, password = password)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == "/editprofilemgr"):
            info = self.headers['Cookie'].split("; ")
            staff_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_id_pair[0].split("=")[1]
            print(staff_id)

            staff_info = load_mgr_edit(staff_id)
            print(staff_info)

            first_name = staff_info[0][0]
            last_name = staff_info[0][1]
            password = staff_info[0][2]
            phone_num = staff_info[0][3]
            address = staff_info[0][4]
            sup_id = staff_info[0][5]
            hourly_wage = staff_info[0][6]
            dob = staff_info[0][7]
            job = staff_info[0][8]
            phone_num = phone_num[0:3] + "-" + phone_num[3:6] + "-" + phone_num[6:]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/editprofilemgr.html', 'r') as file:
                html = file.read()
            
            template_html = Template(html)
            updated_html = template_html.substitute(first_name=first_name, last_name=last_name, phone_num = phone_num, dob = dob, job = job,
                                                    password = password, address = address, sup_id = sup_id, hourly_wage = hourly_wage)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == "/editprofilestaff"):
            info = self.headers['Cookie'].split("; ")
            staff_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_id_pair[0].split("=")[1]
            print(staff_id)

            staff_info = load_staff_edit(staff_id)
            print(staff_info)

            first_name = staff_info[0][0]
            last_name = staff_info[0][1]
            password = staff_info[0][2]
            phone_num = staff_info[0][3]
            address = staff_info[0][4]
            phone_num = phone_num[0:3] + "-" + phone_num[3:6] + "-" + phone_num[6:]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/editprofilestaff.html', 'r') as file:
                html = file.read()
            
            template_html = Template(html)
            updated_html = template_html.substitute(first_name=first_name, last_name=last_name, phone_num = phone_num, 
                                                    password = password, address = address)
            self.wfile.write(updated_html.encode())            
        elif (urlinfo.path == "/viewprofilestaff"):
            info = self.headers['Cookie'].split("; ")
            staff_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_id_pair[0].split("=")[1]
            print(staff_id)

            staff_info = load_staff_profile(staff_id)
            print(staff_info)
            
            formated_info = ''
            for tuple in staff_info:
                for value in tuple:
                    if (type(value) == str):
                        value = value.replace("%40", "@")
                    formated_info += f'<td>{value}</td>'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewstaffprofile.html', 'r') as file:
                html = file.read()

            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode()) 
        elif (urlinfo.path == '/viewhoursworked'):
            info = self.headers['Cookie'].split("; ")
            staff_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_id_pair[0].split("=")[1]
            print(staff_id)

            staff_info = view_hours_worked(staff_id)
            print(staff_info)
            
            formated_info = ''
            tuple_number = 0
            for tuple in staff_info:
                formated_info += "<tr>"
                print(tuple[0])
                for value in tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/edithours?" + str(tuple[0]) + "'>Edit</a></td>"
                formated_info += "<td><a href='/delhours?" + str(tuple[0]) + "'>Delete</a></td></tr>"
                tuple_number += 1

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewhoursworked.html', 'r') as file:
                html = file.read()

            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())             
        elif (urlinfo.path == '/editstaff'):
            staff_info = load_mgr_edit_staff(urlinfo.query)
            print(staff_info[0])
            
            first_name = staff_info[0][0]
            last_name = staff_info[0][1]
            sup_id = staff_info[0][2]
            hourly_wage = staff_info[0][3]
            job = staff_info[0][4]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/editstaff.html', 'r') as file:
                html = file.read()
            
            template_html = Template(html)
            updated_html = template_html.substitute(first_name=first_name, last_name=last_name, job = job, staff_id=urlinfo.query,
                                                    sup_id = sup_id, hourly_wage = hourly_wage)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/edithours'):
            date = urlinfo.query
            info = self.headers['Cookie'].split("; ")
            staff_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_pair[0].split('=')[1]
            staff_info = load_hours_worked(staff_id, date)

            hours_worked = staff_info[0][0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            with open('public/skeleton/edithours.html', 'r') as file:
                html = file.read()

            template_html = Template(html)
            updated_html = template_html.substitute(date = date, hours_worked = hours_worked)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/Entertainment'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/Entertainment.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/feature'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/feature.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/loghours'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/skeleton/loghours.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/manager_portal'):
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])
            
            if cookie["authorization_level"].output().split("=")[1] != "M":
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                file = b""
                try:
                    file = open("public/skeleton/forbidden.html", "rb").read()
                finally:
                    ...
                self.wfile.write(file)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                file = b""
                try:
                    file = open("public/skeleton/manager_portal.html", "rb").read()
                finally:
                    ...
                self.wfile.write(file)
        elif (urlinfo.path == "/staff_portal"):
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])

            if cookie["authorization_level"].output().split("=")[1] != "S":
                self.send_response(403)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                file = b""
                try:
                    file = open("public/skeleton/forbidden.html", "rb").read()
                finally:
                    ...
                self.wfile.write(file)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                file = b""
                try:
                    file = open("public/skeleton/staff_portal.html", "rb").read()
                finally:
                    ...
                self.wfile.write(file)
        elif (urlinfo.path == '/new_event'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/skeleton/new_event.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/new_rides'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/skeleton/new_ride.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/new_staff'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/skeleton/new_staff.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/portal'):
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])
            if cookie["authorization_level"].output().split("=")[1] != "V":
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                file = b""
                try:
                    file = open("public/skeleton/forbidden.html", "rb").read()
                finally:
                    ...
                self.wfile.write(file)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                template_file = b""
                try:
                    template_file = open("public/portal.html", "rb").read()
                finally:
                    ...

                template_file = Template(template_file.decode('utf-8'))
                info = self.headers['Cookie'].split("; ")
                name_pair = [pair for pair in info if pair.startswith('first_name=')]
                first_name = name_pair[0].split('=')[1]
                file = template_file.substitute(name=first_name.capitalize()).encode('utf-8')
                self.wfile.write(file)

        elif (urlinfo.path == '/pricing'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/pricing.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/reservation'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/reservation.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/rides_repair'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/repair log.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/rides_report'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/rides.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/sales_report'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/sales_report.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/sales'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/sales.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/staff_portal'):
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])
            
            if cookie["authorization_level"].output().split("=")[1] != "S":
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                file = b""
                try:
                    file = open("public/skeleton/forbidden.html", "rb").read()
                finally:
                    ...
                self.wfile.write(file)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                file = b""
                try:
                    file = open("public/skeleton/staff_portal.html", "rb").read()
                finally:
                    ...
                self.wfile.write(file)
                
        elif (urlinfo.path == '/viewprofile'):
            info = self.headers['Cookie'].split("; ")
            email_pair = [pair for pair in info if pair.startswith('email=')]
            email = email_pair[0].split('=')[1]
            print(email)
            profile_info = load_profile(email)
            print(profile_info)

            formated_info = ''
            for tuple in profile_info:
                for value in tuple:
                    if (type(value) == str):
                        value = value.replace("%40", "@")
                    formated_info += f'<td>{value}</td>'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/viewprofile.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/viewtickets'):
            info = self.headers['Cookie'].split("; ")
            email_pair = [pair for pair in info if pair.startswith('email=')]
            email = email_pair[0].split('=')[1]
            print(email)
            num_silver, num_gold, num_platinum = view_tickets(email)
            print(num_silver, num_gold, num_platinum)

            formated_info = "<tr> <td> Silver Tickets </td> <td> {} </td> </tr>".format(num_silver)
            formated_info += "<tr> <td> Gold Tickets </td> <td> {} </td> </tr>".format(num_gold)
            formated_info += "<tr> <td> Platinum Tickets </td> <td> {} </td> </tr>".format(num_platinum)

            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewtickets.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == "/viewevents"):
            event_info = load_events()

            formated_info = ''
            tuple_number = 0
            for event_tuple in event_info:
                formated_info += "<tr>"
                print(event_tuple)
                for value in event_tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/editevent?$"+str(tuple_number)+"'>Edit</a></td>"
                formated_info += "<td><a href='/delevent?$"+str(tuple_number)+"'>Delete</a></td></tr>"
                tuple_number += 1
                
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewevents.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/vieweventsstaff'):
            event_info = load_events()

            formated_info = ''
            for event_tuple in event_info:
                formated_info += "<tr>"
                for value in event_tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += '</tr>'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/vieweventsstaff.html', 'r') as file:
                html = file.read()

            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/viewstaff'):
            staff_info = load_staff()
                
            formated_info = ''
            for staff_tuple in staff_info:
                formated_info += "<tr>"
                for value in staff_tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/editstaff?"+str(staff_tuple[2])+"'>Edit</a></td>"
                formated_info += "<td><a href='/delstaff?"+str(staff_tuple[2])+"'>Delete</a></td></tr>"
                
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('public/skeleton/viewstaff.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/viewcustomers'):
            cust_info = load_customers()

            formated_info = ''
            tuple_number = 0
            for tuple in cust_info:
                formated_info += "<tr>"
                for value in tuple:
                    if type(value) == str:
                        value = value.replace("%40", "@")
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/editcust?$tuple"+str(tuple_number)+"'>Edit</a></td>"
                formated_info += "<td><a href='/delcust?$tuple"+str(tuple_number)+"'>Delete</a></td></tr>"
                tuple_number += 1

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('public/skeleton/viewcustomers.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())        
        elif (urlinfo.path == "/viewrides"):
            ride_info = load_rides()

            formated_info = ''
            tuple_number = 0
            for tuple in ride_info:
                formated_info += "<tr>"
                for value in tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/editride?$tuple"+str(tuple_number)+"'>Edit</a></td>"
                formated_info += "<td><a href='/delride?$tuple"+str(tuple_number)+"'>Delete</a></td></tr>"
                tuple_number += 1
            
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            with open('public/skeleton/viewrides.html', 'r') as file:
                html = file.read()
        elif (urlinfo.path == "/viewmgrprofile"):
            info = self.headers['Cookie'].split("; ")
            staff_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_pair[0].split('=')[1]
            staff_info = load_staff_profile(staff_id)

            formated_info = ''
            for tuple in staff_info:
                for value in tuple:
                    formated_info += f'<td>{value}</td>'
            
            print(formated_info)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewmgrprofile.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == "/viewstaffprofile"):
            info = self.headers["Cookie"].split("; ")
            staff_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_pair[0].split('=')[1]
            staff_info = load_staff_profile(staff_id)

            formated_info = ''
            for tuple in staff_info:
                for value in tuple:
                    formated_info += f'<td>{value}</td>'
            
            print(formated_info)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewstaffprofile.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)            
        elif (urlinfo.path == '/rides_style.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("public/rides_style.css", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/sales_style.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("public/sales_style.css", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/styles.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("public/styles.css", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/src/connect.js'):
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()

            file = b""
            try:
                file = open("src/connect.js", "rb").read()
            finally:
                ...
            self.wfile.write(file)

        elif (urlinfo.path == '/src/rides_script.js'):
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()

            file = b""
            try:
                file = open("src/rides_script.js", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/src/sales_script.js'):
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()

            file = b""
            try:
                file = open("src/sales_script.js", "rb").read()
            finally:
                ...
            self.wfile.write(file)       
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/carousel.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
            # print(self.path)

        
        
        #return super().do_GET()



    
    def do_POST(self):
        urlinfo = parse.urlparse(self.path)
        urlinfo.path

        if (urlinfo.path == '/data'):
            print('received')
        elif (urlinfo.path == '/rides'):
            length = int(self.headers['Content-length'])
            content = json.loads(self.rfile.read(length))
            # rides_script.generate_report(content['startDate'], content['endDate'])
            print(content['startDate'])
            print(content['endDate'])
            rides = ride_report(content['startDate'], content['endDate'])
            print(rides)
        elif (urlinfo.path == '/login'):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8") 
            print(data)

            user_pssd = re.split("&", data)
            user = re.split("=", user_pssd[0])[1]
            pssd = re.split("=", user_pssd[1])[1]

            cookie = check_login_cred(user, pssd)
            if cookie["authorization_level"].value == "V":
                print("login successful")
                self.send_response(302)
                self.send_header('Location', '/portal')

                for morsel in cookie.values():
                    self.send_header("Set-Cookie", morsel.OutputString())
            elif cookie["authorization_level"].value == "S":
                print("login successful")
                self.send_response(302)
                self.send_header('Location', '/staff_portal')

                for morsel in cookie.values():
                    self.send_header("Set-Cookie", morsel.OutputString())
            elif cookie["authorization_level"].value == "M":
                print("login successful")
                self.send_response(302)
                self.send_header('Location', '/manager_portal')
                
                for morsel in cookie.values():
                    self.send_header("Set-Cookie", morsel.OutputString())
            elif cookie["authorization_level"].value == "N":
                print("login failed")
                self.send_response(302)
                self.send_header('Location', '/connect')
            else:
                raise Exception()
            self.end_headers()
        elif(urlinfo.path == "/logout"):
            self.send_response(302)
            self.send_header("Set-Cookie", "authorization_level=N")
            self.send_header('Location', '/')
            self.end_headers()
        elif (urlinfo.path == "/addstaff"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1]
            last_name = re.split("=", split_data[1])[1]
            password = re.split("=", split_data[2])[1]
            phone_num = re.split("=", split_data[3])[1]
            phone_num = phone_num.replace("-", "")
            address = re.split("=", split_data[4])[1]
            dob = re.split("=", split_data[5])[1]
            job = re.split("=", split_data[6])[1]
            hourly_wage = re.split("=", split_data[7])[1]
            print(first_name, last_name, password, phone_num, address, dob, job, hourly_wage)

            info = self.headers['Cookie'].split("; ")
            sup_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            sup_id = sup_id_pair[0].split('=')[1]
            print(sup_id)

            add_staff(sup_id, first_name, last_name, password, phone_num, address, dob, job, hourly_wage)


            self.send_response(302)
            self.send_header("Location", '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == '/addride'):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            ride_name = re.split("&", split_data[0])[1]
            print(ride_name)

            add_ride(ride_name)
            self.send_response(302)
            self.send_header("Location", '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/addevent"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            event_name = re.split("&", split_data[0])[1]
            event_descrip = re.split("&", split_data[1])[1]
            start_date = re.split("&", split_data[2])[1]
            end_date = re.split("&", split_data[3])[1]
            event_descrip = event_descrip.replace("+", " ")
            print(event_name, event_descrip, start_date, end_date)

            info = self.headers['Cookie'].split("; ")
            sup_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            sup_id = sup_id_pair[0].split('=')[1]
            print(sup_id)

            add_event(sup_id, event_name, event_descrip, start_date, end_date)
            self.send_response(302)
            self.send_header("Location", '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/addhours"):
            info = self.headers['Cookie'].split("; ")
            auth_level_pair = [pair for pair in info if pair.startswith('authorization_level=')]
            auth_level = auth_level_pair[0].split('=')[1]
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            print(split_data)
            hours = re.split("=", split_data[0])[1]
            date = re.split("=", split_data[1])[1]
            print(hours, date)

            info = self.headers['Cookie'].split("; ")
            staff_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_id_pair[0].split('=')[1]
            print(staff_id)
            print(auth_level)
            add_hours(staff_id, hours, date)
            self.send_response(302)
            if (auth_level == "S"):
                self.send_header("Location", '/staff_portal')
            elif (auth_level == "M"):
                self.send_header("Location", '/manager_portal')
            self.end_headers()            
        elif (urlinfo.path == '/signup'):
            self.send_response(302)
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8") 
            print(data)
            
            split_data = re.split("&", data)
            fname = re.split("=", split_data[0])[1]
            lname = re.split("=", split_data[1])[1]
            phone = re.split("=", split_data[2])[1]
            email = re.split("=", split_data[3])[1]
            pswrd = re.split("=", split_data[4])[1]

            phone = phone.replace("-", "")
            
            cookie = sign_up(fname, lname, phone, email, pswrd)
            
            
            for morsel in cookie.values():
                self.send_header("Set-Cookie", morsel.OutputString())
            
            self.send_header('Location', '/portal')
            self.end_headers()
        elif (urlinfo.path == "/ticketpurchase"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            ticket_type = re.split("=", split_data[0])[1]
            num_tickets = int(re.split("=", split_data[1])[1])
            card_first_name = re.split("=", split_data[2])[1]
            card_last_name = re.split("=", split_data[3])[1]
            card_number = re.split("=", split_data[4])[1]
            cvv = re.split("=", split_data[5])[1]
            exp_month = re.split("=", split_data[6])[1]
            exp_year = re.split("=", split_data[7])[1]
            card_number = card_number.replace("-","")
            print(card_first_name, card_last_name, ticket_type, card_number, cvv, exp_month, exp_year, num_tickets)

            info = self.headers['Cookie'].split("; ")
            email_pair = [pair for pair in info if pair.startswith('email=')]
            email = email_pair[0].split('=')[1]

            insert_ticket_purchase(card_first_name, card_last_name, ticket_type, card_number, cvv, exp_month, exp_year[2:4], email, num_tickets)
            self.send_response(302)
            self.send_header('Location', '/portal')
            self.end_headers()
        elif (urlinfo.path == "/updateprofile"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1]
            last_name = re.split("=", split_data[1])[1]
            phone_num = re.split("=", split_data[2])[1]
            password = re.split("=", split_data[3])[1]
            phone_num = phone_num.replace("-","")
            print(first_name, last_name, phone_num, password)

            info = self.headers['Cookie'].split("; ")
            email_pair = [pair for pair in info if pair.startswith('email=')]
            email = email_pair[0].split('=')[1]          

            update_profile(email, first_name, last_name, phone_num, password)
            self.send_response(302)
            self.send_header('Location', '/profile')
            self.end_headers()
        elif (urlinfo.path == "/updatemgr"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            
            
            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1]
            last_name = re.split("=", split_data[1])[1]
            phone_num = re.split("=", split_data[2])[1]
            address = re.split("=", split_data[3])[1]
            sup_id = re.split("=", split_data[4])[1]
            dob = re.split("=", split_data[5])[1]
            job = re.split("=", split_data[6])[1]
            hourly_wage = re.split("=", split_data[7])[1]
            password = re.split("=", split_data[8])[1]

            address = address.replace("+", " ")
            phone_num = phone_num.replace("-", "")

            info = self.headers['Cookie'].split("; ")
            staff_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_id_pair[0].split('=')[1]     

            update_mgr_level(staff_id, first_name, last_name, phone_num, address, sup_id, password, hourly_wage, dob, job)
            self.send_response(302)
            self.send_header('Location', '/viewmgrprofile')
            self.end_headers()
        elif (urlinfo.path == "/updatestaff"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            
            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1]
            last_name = re.split("=", split_data[1])[1]
            phone_num = re.split("=", split_data[2])[1]
            address = re.split("=", split_data[3])[1]
            password = re.split("=", split_data[4])[1]

            address = address.replace("+", " ")
            phone_num = phone_num.replace('-', "")

            info = self.headers['Cookie'].split("; ")
            staff_id_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_id_pair[0].split('=')[1]     

            update_staff_level(staff_id, first_name, last_name, phone_num, address, password)
            self.send_response(302)
            self.send_header('Location', '/viewprofilestaff')
            self.end_headers()            


            


httpd = socketserver.TCPServer(("", PORT), ThemeParkHandler)
try:
    print("starting up server")
    httpd.serve_forever()
    print("server up")
except:
    print("closing")
finally:
    httpd.server_close()

print("server shut down")