import http.server
import socketserver
import os
from urllib import parse 
import re
#from src import rides_script
from src.query import check_login_cred
import json

PORT = 8000

class ThemeParkHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        urlinfo = parse.urlparse(self.path)
        urlinfo.path
        
        if (urlinfo.path == '/addingitem.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/addingitem.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/carousel.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/connect.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/connect.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)


        elif (urlinfo.path == '/Entertainment.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/Entertainment.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/feature.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/feature.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/portal.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/portal.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/pricing.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/pricing.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/repair%20log.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/repair log.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/reservation.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/reservation.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
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
        elif (urlinfo.path == '/rides.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/rides.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/sales_report.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/sales_report.html", "rb").read()
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
        elif (urlinfo.path == '/sales.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/sales.html", "rb").read()
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
        elif (urlinfo.path == '/visitor.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("public/visitor.css", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (urlinfo.path == '/visitor.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("public/visitor.html", "rb").read()
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
        print(urlinfo)

        if (urlinfo.path == '/data'):
            print('received')
        elif (urlinfo.path == '/rides'):
            length = int(self.headers['Content-length'])
            content = json.loads(self.rfile.read(length))
            rides_script.generate_report(content['startDate'], content['endDate'])
            print(content['startDate'])
            print(content['endDate'])
        elif (urlinfo.path == '/login'):
            self.send_response(200)
            data = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8") 
            print(data)

            user_pssd = re.split("&", data)
            user = re.split("=", user_pssd[0])[1]
            pssd = re.split("=", user_pssd[1])[1]

            print(user)
            print(pssd)

            if check_login_cred(user, pssd):
                print("login successful")
            else:
                print("login failed")


            self.send_header('Location', 'google.com')
            self.end_headers()

    def redirect(self):
        self.send_response(200)
        self.send_header('Location', 'google.com')
        self.end_headers()


with socketserver.TCPServer(("", PORT), ThemeParkHandler) as httpd:
    print("serving at port", PORT)
    try:
        httpd.serve_forever()
    except:
        print("closing")
