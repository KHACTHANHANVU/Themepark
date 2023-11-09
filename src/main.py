import http.server
import socketserver
import os

PORT = 8000

class ThemeParkHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/'):
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

        elif (self.path == '/connect.html'):
            print('green')
        elif (self.path == '/feature.html'):
            print('red')
        elif (self.path == '/Entertainment.html'):
            print('blue')
        elif (self.path == '/styles.css'):
            print('here')
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()

            file = b""
            try:
                file = open("../public/styles.css", "rb").read()
            finally:
                ...
            self.wfile.write(file)


        
        #return super().do_GET()
    
    def do_HEAD(self):
        return super().do_HEAD()


with socketserver.TCPServer(("", PORT), ThemeParkHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
