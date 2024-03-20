from http.server import BaseHTTPRequestHandler
from db_connector import Database


class VideoViewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        db = Database()
        conn = db.connect()

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT title, description, file_path, category_name FROM Videos INNER JOIN Categories ON Videos.category_id = Categories.category_id")
        videos = cursor.fetchall()
        conn.close()

        # Start building HTML response
        html_response = "<!DOCTYPE html>"
        html_response += "<html lang='en'>"
        html_response += "<head>"
        html_response += "<meta charset='UTF-8'>"
        html_response += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
        html_response += "<title>View Videos</title>"
        html_response += "</head>"
        html_response += "<body>"
        html_response += "<h1>View Videos</h1>"
        html_response += "<ul>"

        # Iterate through videos and construct HTML for each video
        for video in videos:
            html_response += "<li>"
            html_response += "<h2>{}</h2>".format(video['title'])
            html_response += "<p>{}</p>".format(video['description'])
            html_response += "<p>Category: {}</p>".format(video['category_name'])
            html_response += "<video width='320' height='240' controls>"
            html_response += "<source src='{}' type='video/mp4'>".format(video['file_path'])
            html_response += "Your browser does not support the video tag."
            html_response += "</video>"
            html_response += "</li>"

        html_response += "</ul>"
        html_response += "</body>"
        html_response += "</html>"

        # Send HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_response.encode('utf-8'))
