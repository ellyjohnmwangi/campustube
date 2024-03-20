from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
from urllib.parse import urlparse, parse_qs


# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )


# Video upload handler
class VideoUploadHandler(BaseHTTPRequestHandler):
    def do_post(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = parse_qs(body.decode())

        title = params['title'][0]
        description = params['description'][0]
        category_id = int(params['category'][0])

        # Save the video file to a specified directory
        file_data = self.rfile.read(int(self.headers['Content-Length']))
        file_path = 'uploads/' + self.path.split('/')[-1]
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Store video information in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Videos (title, description, file_path, category_id) VALUES (%s, %s, %s, %s)",
                       (title, description, file_path, category_id))
        conn.commit()
        conn.close()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Video uploaded successfully')


# Server configuration
def run_server():
    PORT = 8000
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, VideoUploadHandler)
    print("Server running on port", PORT)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()