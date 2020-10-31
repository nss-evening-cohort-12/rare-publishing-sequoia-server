from http.server import BaseHTTPRequestHandler, HTTPServer
from users import create_user
import json


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # ['email', 'jenna@solis.com']
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # no query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had a trailing slash: /animals/

            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == 'posts':
                response1 = {'data': 'Not here... yet'}
                response = json.dumps(response1)

        elif len(parsed) == 3:
            (resource, key, value) = parsed

        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_entry = None

        if resource == 'register':
            print('POST to "register" endpoint')
            new_entry = create_user(post_body)
        elif resource == 'posts':
            print('POST to "posts" endpoint')

        self.wfile.write(f"{new_entry}".encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type')
        self.end_headers()


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()