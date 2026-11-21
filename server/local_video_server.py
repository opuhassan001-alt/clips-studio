import http.server
import socketserver
import os
import sys

PORT = 8766
DIRECTORY = r"E:\work station\gta 6\data\clips\speed_gta6_viral"

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        super().end_headers()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', PORT), CORSHandler) as httpd:
        print(f"Serving {DIRECTORY} at http://127.0.0.1:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
