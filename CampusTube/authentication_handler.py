from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
from db_connector import Database  # Importing the Database class


# Function to authenticate user login
# Function to authenticate user login
def authenticate_user(username, password):
    db = Database()
    query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    user = db.execute_query(query, (username, password))
    return user[0] if user else None


# Request handler for user login
class LoginHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = parse_qs(body.decode())

        username = params['username'][0]
        password = params['password'][0]

        user = authenticate_user(username, password)

        if user:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Login successful', 'user_id': user[0]}).encode())
        else:
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Invalid username or password'}).encode())


# Request handler for user signup
class SignupHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = parse_qs(body.decode())

        username = params['username'][0]
        password = params['password'][0]

        db = Database()
        query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        db.execute_insert(query, (username, password))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'User signed up successfully'}).encode())
