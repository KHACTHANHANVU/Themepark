import http.server
import socketserver
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

PORT = 8000

class ThemeParkHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/addingitem.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/addingitem.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/'):
            print('here')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/carousel.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/connect.html'):
            print('green')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/connect.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/Entertainment.html'):
            print('blue')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/Entertainment.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/feature.html'):
            print('red')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/feature.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)

        elif (self.path == '/repair%20log.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/repair log.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/sales_report.html'):
            print('yellow')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/sales_report.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/sales_style.css'):
            print('yellow')
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("../public/sales_style.css", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/sales.html'):
            print('yellow')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            file = b""
            try:
                file = open("../public/sales.html", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        elif (self.path == '/styles.css'):
            print('black')
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("../public/styles.css", "rb").read()
            finally:
                ...
            self.wfile.write(file)
        else:
            print(self.path)


        
        #return super().do_GET()
    
    def do_HEAD(self):
        return super().do_HEAD()


with socketserver.TCPServer(("", PORT), ThemeParkHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
