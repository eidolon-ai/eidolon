import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class OAuth2CallbackHandler(BaseHTTPRequestHandler):
    oauth2_uri = None
    response_value = None  # Add this line

    def do_GET(self):
        if self.path.startswith('/auth'):
            OAuth2CallbackHandler.oauth2_uri = "https://localhost" + self.path

        # Respond to the browser
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        response_content = "Authorization complete. You may now close this window." if self.oauth2_uri else "No authorization code found."
        self.wfile.write(response_content.encode())

        self.response_value = response_content  # Add this line

    def log_message(self, format, *args):
        return


class AuthWebserver:
    server: HTTPServer
    port: int

    # noinspection PyMethodMayBeStatic,PyTypeChecker
    def start_local_server(self):
        self.server = HTTPServer(('localhost', 0), OAuth2CallbackHandler)
        self.port = self.server.server_port
        thread = threading.Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()

    # noinspection PyMethodMayBeStatic
    def stop_local_server(self):
        self.server.shutdown()
        self.server.server_close()

    def wait_for_token(self):
        while not OAuth2CallbackHandler.oauth2_uri:
            time.sleep(0.01)
        self.stop_local_server()
        return OAuth2CallbackHandler.oauth2_uri
