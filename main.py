import http.server
import socketserver
from urllib import parse 
import re
from src.login import *
import json
from http.cookies import SimpleCookie
from string import Template
from datetime import datetime

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
            
            with open("public/carousel.html", 'r') as file:
                html = file.read()
                self.wfile.write(html.encode())
        elif (urlinfo.path == '/buyticket'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open("public/buy_ticket.html", 'r') as file:
                html = file.read()
                self.wfile.write(html.encode())   
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
            updated_html = template_html.substitute(staff_id=staff_id, first_name=first_name, last_name=last_name, phone_num = phone_num, 
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
            for staff_tuple in staff_info:
                for value in staff_tuple:
                    if (type(value) == str):
                        value = value.replace("%40", "@")
                    formated_info += f'<td>{value}</td>'
                formated_info += '<td><a href="/editprofilestaff?'+ str(staff_id) +'">Edit</a></td>'
            
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
            auth_level_pair = [pair for pair in info if pair.startswith('authorization_level=')]
            auth_level = auth_level_pair[0].split("=")[1]
            print(staff_id)

            staff_info = view_hours_worked(staff_id)
            print(staff_info)
                        

            if auth_level == 'M':
                formated_info = ''
                for hours_tuple in staff_info:
                    formated_info += "<tr>"
                    for value in hours_tuple:
                        formated_info += f'<td>{value}</td>'
                    
                    formated_info += "<td><a href='/edithours?" + str(hours_tuple[0]).replace("-","_") + "'>Edit</a></td>"
                    #formated_info += "<td><a href='/delhours?" + str(hours_tuple[0]).replace("-","_") + "'>Delete</a></td></tr>"
                
                print(formated_info)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('public/skeleton/viewhoursworkedmgr.html', 'r') as file:
                    html = file.read()
            else:
                formated_info = ''
                for hours_tuple in staff_info:
                    formated_info += "<tr>"
                    for value in hours_tuple:
                        formated_info += f'<td>{value}</td>'
                    formated_info += "</tr>"
                
                print(formated_info)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('public/skeleton/viewhoursworked.html', 'r') as file:
                    html = file.read()


            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/delhours'):
            date = urlinfo.query
            info = self.headers['Cookie'].split("; ")
            staff_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_pair[0].split('=')[1]
            del_hours(date, staff_id)
            
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == '/viewbday'):
            bday_info = load_bday()
            
            formated_info = ''
            for b_tuple in bday_info:
                formated_info += "<tr>"
                for value in b_tuple:
                    formated_info += f'<td>{value}</td>'

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewbday.html', 'r') as file:
                html = file.read()

            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())    
        elif (urlinfo.path == '/editbday'):
            bday_info = edit_bday(urlinfo.query)
            
            b_date = bday_info[0][0]
            revenue = bday_info[0][1]
            expenses = bday_info[0][2]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/editbday.html', 'r') as file:
                html = file.read()
                
            template_html = Template(html)
            updated_html = template_html.substitute(b_date=b_date, revenue=revenue, expenses=expenses)
            self.wfile.write(updated_html.encode())           
            
        elif (urlinfo.path == '/edithours'):
            date = urlinfo.query
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])
            
            staff_id = cookie["staff_id"].output().split("=")[1]
            staff_info = load_hours_worked(staff_id, date)

            hours_worked = staff_info[0][0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('public/skeleton/edithours.html', 'r') as file:
                html = file.read()
                template_html = Template(html)
                updated_html = template_html.substitute(date = date, hours_worked = hours_worked)
                self.wfile.write(updated_html.encode())
            
        elif (urlinfo.path == '/loghours'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/loghours.html', 'r') as file:
                html = file.read()
                self.wfile.write(html.encode())
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
        elif (urlinfo.path == '/newbday'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/skeleton/newbday.html", "rb").read()
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
        elif (urlinfo.path == '/rides_repair'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/skeleton/rides_repair.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/rides_report'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/rides_report.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/revenue_report'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/revenue_report.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/event_report'):
            event_info = get_events()

            formated_info = ''
            for tuple in event_info:
                    formated_info += f'<option value={tuple[0]}>{tuple[1]}</option>'

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/event_report.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())       
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

            with open('public/skeleton/viewprofile.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/viewrepairlogs'):
            reapir_info = load_repair_logs()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            formated_info = ''
            for repair_tuple in reapir_info:
                formated_info += '<tr>'
                for value in repair_tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/editrepairlog?"+str(repair_tuple[0])+"&"+str(repair_tuple[1])+"'>Edit</a></td>"

            with open('public/skeleton/viewrepairlogs.html', 'r') as file:
                html = file.read()

            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/editrepairlog'):
            repair_info = load_repair_log_edit(urlinfo.query.split("&")[0],
                                               parse.unquote(urlinfo.query.split("&")[1]))
            print(repair_info[0])
            repair_date = repair_info[0][0]
            repair_cost = repair_info[0][1]        
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/editrepairlog.html', 'r') as file:
                html = file.read()
            
            template_html = Template(html)
            updated_html = template_html.substitute(ride_no=urlinfo.query.split("&")[0], date_of_issue=urlinfo.query.split("&")[1],
                                                    repair_date=repair_date, repair_cost=repair_cost,)
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
                formated_info += "<td><a href='/editevent?"+str(event_tuple[1])+"'>Edit</a></td>"
                formated_info += "<td><a href='/delevent?"+str(event_tuple[1])+"'>Delete</a></td></tr>"
                tuple_number += 1
                
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewevents.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/editevent'):
            event = load_event_edit(urlinfo.query)
            print(event[0])

            event_no = event[0][0]
            manager_id = event[0][1]
            e_name = event[0][2]
            e_descrip = event[0][3]
            start_date = event[0][4]
            end_date = event[0][5]


            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/editevent.html', 'r') as file:
                html = file.read()

            template_html = Template(html)
            updated_html = template_html.substitute(event_no=event_no, manager_id=manager_id, e_name=e_name, e_descrip=e_descrip,
                                                    start_date=start_date, end_date=end_date)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/delevent'):
            print(urlinfo.query)
            del_event(urlinfo.query)
            
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == '/vieweventsstaff'):
            event_info = load_events_cust()

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
        elif (urlinfo.path == '/delstaff'):
            del_staff(urlinfo.query)
            
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == '/viewcustomers'):
            cust_info = load_customers()
            print(cust_info)

            formated_info = ''
            tuple_number = 0
            for cust_tuple in cust_info:
                formated_info += "<tr>"
                for value in cust_tuple:
                    if type(value) == str:
                        value = value.replace("%40", "@")
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/editcust?"+str(cust_tuple[2])+"'>Edit</a></td>"
                formated_info += "<td><a href='/delcust?"+str(cust_tuple[2])+"'>Delete</a></td></tr>"

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('public/skeleton/viewcustomers.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/editcust'):
            customer = load_customers_edit(urlinfo.query)
            print(customer)
            
            first_name = customer[0][0]
            last_name = customer[0][1]
            email = customer[0][2].replace("%40", "@") # urlinfo.query
            pswrd = customer[0][3]
            phone_num = customer[0][4]
                        
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/editcust.html', 'r') as file:
                html = file.read()

            template_html = Template(html)
            updated_html = template_html.substitute(first_name=first_name, last_name=last_name, pswrd=pswrd, email=email,
                                                    phone_num=phone_num)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/delcust'):
            print(urlinfo.query)
            del_customer(urlinfo.query)
            
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/viewrides"):
            ride_info = load_rides()

            formated_info = ''
            tuple_number = 0
            for ride_tuple in ride_info:
                formated_info += "<tr>"
                for value in ride_tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "<td><a href='/editride?"+str(ride_tuple[1])+"'>Edit</a></td>"
                formated_info += "<td><a href='/delride?"+str(ride_tuple[1])+"'>Delete</a></td></tr>"
                tuple_number += 1
            
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            with open('public/skeleton/viewrides.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == "/editride"):
            ride = load_rides_edit(urlinfo.query)
            print(ride)
            
            ride_name = ride[0][0]
            is_working = ride[0][1]
            date_of_last_repair = ride[0][2]
            

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/editride.html', 'r') as file:
                html = file.read()
            
            template_html = Template(html)
            updated_html = template_html.substitute(ride_no=urlinfo.query, ride_name=ride_name,
                                                    date_of_last_repair=date_of_last_repair)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == "/delride"):
            del_ride(urlinfo.query)
            
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/customerviewrides"):
            ride_info = load_rides_cust()

            formated_info = ''
            for ride_tuple in ride_info:
                formated_info += "<tr>"
                for value in ride_tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "</tr>"
            
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            with open('public/skeleton/customerviewrides.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())
        elif (urlinfo.path == "/customerviewevents"):
            event_info = load_events_cust()

            formated_info = ''
            for event_tuple in event_info:
                formated_info += "<tr>"
                for value in event_tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "</tr>"

            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            with open('public/skeleton/customerviewevents.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode())           
        elif (urlinfo.path == "/viewmgrprofile"):
            info = self.headers['Cookie'].split("; ")
            staff_pair = [pair for pair in info if pair.startswith('staff_id=')]
            staff_id = staff_pair[0].split('=')[1]
            staff_info = load_staff_profile(staff_id)

            formated_info = ''
            for tuple in staff_info:
                for value in tuple:
                    formated_info += f'<td>{value}</td>'
            
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
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('public/skeleton/viewstaffprofile.html', 'r') as file:
                html = file.read()
            
            updated_html = html.replace('<!-- InsertTableHere -->', formated_info)  
            self.wfile.write(updated_html.encode())          
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
        elif (urlinfo.path == '/revenue_style.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("public/revenue_style.css", "rb").read()
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
            rides = rides_report(content['startDate'], content['endDate'])
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
        elif (urlinfo.path == '/addrepairlog'):
            info = self.headers['Cookie'].split("; ")
            auth_level_pair = [pair for pair in info if pair.startswith('authorization_level=')]
            auth_level = auth_level_pair[0].split('=')[1]

            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            ride_no = re.split("=", split_data[0])[1]
            date_of_issue_str = re.split("=", split_data[1])[1]
            repair_date_str = re.split("=", split_data[2])[1]
            repair_cost = re.split("=", split_data[3])[1]

            date_of_issue = datetime.strptime(parse.unquote(date_of_issue_str), '%Y-%m-%dT%H:%M')
            repair_date = datetime.strptime(parse.unquote(repair_date_str), '%Y-%m-%dT%H:%M')

            add_repair_log(ride_no, date_of_issue, repair_date, repair_cost)
            self.send_response(302)
            if (auth_level == "S"):
                self.send_header("Location", '/staff_portal')
            elif (auth_level == "M"):
                self.send_header("Location", '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == '/addride'):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            ride_name = re.split("=", split_data[0])[1]
            ride_name = ride_name.replace("+", " ")
            print(ride_name)

            add_ride(ride_name)
            self.send_response(302)
            self.send_header("Location", '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/addevent"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            event_name = re.split("=", split_data[0])[1]
            event_descrip = re.split("=", split_data[1])[1]
            start_date = re.split("=", split_data[2])[1]
            end_date = re.split("=", split_data[3])[1]

            event_name = event_name.replace("+", " ")
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
        elif (urlinfo.path == "/addbday"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            date = re.split("=", split_data[0])[1]
            revenue = re.split("=", split_data[1])[1]
            expenses = re.split("=", split_data[2])[1]
            print(date, revenue, expenses)

            add_bday(date, revenue, expenses)
            self.send_response(302)
            self.send_header("Location", '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == '/gen_revenue_report'):
            self.send_response(200)
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8") 
            print(data)
            
            split_data = re.split("&", data)
            start_date = re.split("=", split_data[0])[1]
            end_date = re.split("=", split_data[1])[1]
            
            print(start_date)
            print(end_date)
            
            result1, result2, result3, wage_expenses = revenue_report(start_date, end_date)
            print(result1)
            print(result2)
            print(result3)
            print(wage_expenses)
            
            
            park_rev = result1[0][0] if result1[0][0] else 0
            park_exp = result1[0][1] if result1[0][1] else 0
            ticket_rev = result2[0][0] if result2[0][0] else 0
            ticket_rev = float(ticket_rev)
            wage_expenses = float(wage_expenses)
            ticket_exp = 0
            repair_rev = 0
            repair_exp = result3[0][0] if result3[0][0] else 0
            total_revenue = ticket_rev + park_rev
            total_expenses = repair_exp + park_exp + wage_expenses
            total_income = total_revenue - total_expenses
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/genrevenuereport.html', 'r') as file:
                html = file.read()
                template_html = Template(html)
                updated_html = template_html.substitute(ticket_revenue=ticket_rev, ticket_income=(ticket_rev-ticket_exp),
                                                        repair_costs=repair_exp, repair_income=(repair_rev-repair_exp),
                                                        park_revenue=park_rev, park_expenses=park_exp, park_income=(park_rev-park_exp),
                                                        wage_expenses = wage_expenses, total_revenue=total_revenue, 
                                                        total_expenses=total_expenses,
                                                        total_income=total_income)
                self.wfile.write(updated_html.encode())
        elif (urlinfo.path == '/gen_rides_report'):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            start_date = re.split("=", split_data[0])[1]
            end_date = re.split("=", split_data[1])[1]
            print(start_date, end_date)

            rides_info = rides_report(start_date, end_date)


            formated_info = ''
            for tuple in rides_info:
                formated_info += "<tr>"
                for value in tuple:
                    formated_info += f'<td>{value}</td>'
                formated_info += "</tr>"

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/genridesreport.html', 'r') as file:
                html = file.read()
                template_html = Template(html)
                updated_html = html.replace('<!-- InsertTableHere -->', formated_info)
            self.wfile.write(updated_html.encode()) 
        elif (urlinfo.path == '/gen_event_report'):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            event_num = re.split("=", split_data[0])[1]
            print(event_num)
            
            result1, result2, result3, result4, result5, result6 = events_report(event_num)

            event_name = result1[0][0]
            mgr_id = result1[0][1]
            start_date = result1[0][2]
            end_date = result1[0][3]

            num_silver = result2[0][0] if result2[0][0] else 0
            silver_revenue = result2[0][1] if result2[0][1] else 0

            num_gold = result3[0][0] if result3[0][0] else 0
            gold_revenue = result3[0][1] if result3[0][1] else 0

            num_platinum = result4[0][0] if result4[0][0] else 0
            platinum_revenue = result4[0][1] if result4[0][1] else 0

            mgr_name = result5[0][0].capitalize() + " " + result5[0][1].capitalize()

            park_revenue = result6[0][0] if result6[0][0] else 0

            total_tickets = float(num_silver) + float(num_gold) + float(num_platinum)
            total_revenue = float(silver_revenue) + float(gold_revenue) + float(platinum_revenue) + float(park_revenue)

            print(event_name, mgr_id, mgr_name, start_date, end_date)
            print(num_silver, num_gold, num_platinum)


            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('public/skeleton/geneventreport.html', 'r') as file:
                html = file.read()
                template_html = Template(html)
                updated_html = template_html.substitute(event_name = event_name, manager_id = mgr_id, start_date = start_date, 
                                                        end_date = end_date, num_silver = num_silver, silver_revenue = silver_revenue,
                                                        num_gold = num_gold, gold_revenue = gold_revenue, num_platinum = num_platinum,
                                                        platinum_revenue = platinum_revenue, manager_name = mgr_name,
                                                        park_revenue = park_revenue, total_tickets = total_tickets, total_revenue =
                                                        total_revenue)
            self.wfile.write(updated_html.encode())             
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
        elif (urlinfo.path == "/updatebday"):
            ##
            ##  WORK IN PROGRESS
            ##
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            b_date = re.split("=", split_data[0])[1] if re.split("=", split_data[0])[1] else "NULL"
            revenue = re.split("=", split_data[1])[1] if re.split("=", split_data[1])[1] else 0
            expenses = re.split("=", split_data[2])[1] if re.split("=", split_data[2])[1] else 0
            
            update_bday(b_date, revenue, expenses)

            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/updatecust"):
            ##
            ##  WORK IN PROGRESS
            ##
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1] if re.split("=", split_data[0])[1] else "NULL"
            last_name = re.split("=", split_data[1])[1] if re.split("=", split_data[1])[1] else "NULL"
            password = re.split("=", split_data[2])[1] if re.split("=", split_data[2])[1] else "NULL"
            phone_num = re.split("=", split_data[3])[1] if re.split("=", split_data[3])[1] else "NULL"
            phone_num = phone_num.replace("-","")
            email = urlinfo.query.replace("@", "%40")
            
            update_customer(email, first_name, last_name, phone_num, password)

            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/updateevent"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            event_name = re.split("=", split_data[0])[1].replace("+", " ")
            manager_id = re.split("=", split_data[1])[1]
            event_num = urlinfo.query # re.split("=", split_data[2])[1]
            event_descrip = re.split("=", split_data[2])[1].replace("+", " ")
            start_date = re.split("=", split_data[3])[1]
            end_date = re.split("=", split_data[4])[1]
            
            update_event(event_num, event_name, event_descrip, manager_id, start_date, end_date)

            self.send_response(302)
            self.send_header('Location', '/viewevents')
            self.end_headers()
        elif (urlinfo.path == "/updatehours"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])
            
            staff_id = cookie["staff_id"].output().split("=")[1]
            date = urlinfo.query
            hours_worked = re.split("=", data)[1]            
            print(staff_id, date, hours_worked)

            update_hours_worked(staff_id, hours_worked, date)
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/updateprofile"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)

            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1]
            last_name = re.split("=", split_data[1])[1]
            phone_num = re.split("=", split_data[2])[1]
            password = re.split("=", split_data[3])[1]
            
            phone_num = phone_num.replace("-", "")
            print(first_name, last_name, phone_num, password)

            info = self.headers['Cookie'].split("; ")
            email_pair = [pair for pair in info if pair.startswith('email=')]
            email = email_pair[0].split('=')[1]          

            update_profile(email, first_name, last_name, phone_num, password)
            self.send_response(302)
            self.send_header('Location', '/portal')
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
        elif (urlinfo.path == "/updaterepairlog"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)
            
            split_data = re.split("&", data)
            repair_date = re.split("=", split_data[0])[1]
            repair_cost =  re.split("=", split_data[1])[1]

            ride_no = urlinfo.query.split("&")[0]
            date_of_issue = urlinfo.query.split("&")[1]
            
            print(parse.unquote(date_of_issue))
            print(parse.unquote(repair_date))
            
            date_of_issue = datetime.strptime(parse.unquote(date_of_issue), '%Y-%m-%d %H:%M:%S')
            repair_date = datetime.strptime(parse.unquote(repair_date), '%Y-%m-%dT%H:%M')
            
            update_repair_log(ride_no, date_of_issue, repair_date, repair_cost)
            
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
            
        elif (urlinfo.path == "/updateride"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)
            
            split_data = re.split("&", data)
            ride_name = re.split("=", split_data[0])[1]
            is_working = 1 if re.split("=", split_data[1])[1] == "true" else 0
            date_of_last_repair = re.split("=", split_data[2])[1]

            date_of_last_repair = datetime.strptime(parse.unquote(date_of_last_repair), '%Y-%m-%dT%H:%M')
            ride_no = urlinfo.query
            ride_name = ride_name.replace("+", " ")

            update_ride(ride_no, ride_name, is_working, date_of_last_repair)
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/updatestaff"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)
            
            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1]
            last_name = re.split("=", split_data[1])[1]
            sup_id = re.split("=", split_data[2])[1]
            job = re.split("=", split_data[3])[1]
            hourly_wage = re.split("=", split_data[4])[1]

            staff_id = urlinfo.query

            update_staff_level(staff_id, first_name, last_name, sup_id, job, hourly_wage)
            self.send_response(302)
            self.send_header('Location', '/manager_portal')
            self.end_headers()
        elif (urlinfo.path == "/updatestaffprofile"):
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
            print(data)
            
            split_data = re.split("&", data)
            first_name = re.split("=", split_data[0])[1]
            last_name = re.split("=", split_data[1])[1]
            phone_num = re.split("=", split_data[2])[1]
            address = re.split("=", split_data[3])[1]
            password = re.split("=", split_data[4])[1]
            phone_num = phone_num.replace("-","")
            address = address.replace("+", " ")
            
            staff_id = urlinfo.query

            update_staff_profile(staff_id, first_name, last_name, phone_num, address, password)
            self.send_response(302)
            self.send_header('Location', '/staff_portal')
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