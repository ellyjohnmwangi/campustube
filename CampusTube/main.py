from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
from db_connector import Database  # Importing the Database class
from video_view import VideoViewHandler


class Main(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.db = Database()

    def do_GET(self):
        routes = {
            '/': self.handle_home,
            '/login': self.handle_login,
            '/upload': self.handle_upload,
            '/index': self.handle_index,
        }
        if self.path in routes:
            routes[self.path]()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_home(self):
        # Redirect to login page
        self.send_response(302)
        self.send_header('Location', '/login')
        self.end_headers()

    def handle_login(self):
        # Serve login.html page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('login.html', 'rb') as f:
            self.wfile.write(f.read())

    def handle_upload(self):
        # Serve upload.html page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('upload.html', 'rb') as f:
            self.wfile.write(f.read())

    def handle_index(self):
        # Serve index.html page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('index.html', 'rb') as f:
            self.wfile.write(f.read())


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = parse_qs(body.decode())

        # Your authentication logic here

        # For demonstration purposes, just returning a success message
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Login successful'}).encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    main = HTTPServer(server_address, Main)
    print("Server running on port", server_address[1])
    try:
        main.serve_forever()
    except KeyboardInterrupt:
        main.server_close()
        print("Server stopped.")
