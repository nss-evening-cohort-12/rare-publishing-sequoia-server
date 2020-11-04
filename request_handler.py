from http.server import BaseHTTPRequestHandler, HTTPServer
from post_tags import tag_post
from tags import create_tag, get_all_tags
from users import login_user, register_user
from posts import create_post, get_all_posts, get_posts_by_user
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
                response = get_all_posts()
            elif resource == 'tags':
                response = get_all_tags()

        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "user_id" and resource == "posts":
                response = get_posts_by_user(value)

        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        response = None

        if resource == 'register':
            response = register_user(post_body)
        elif resource == 'login':
            response = login_user(post_body)
        elif resource == 'posts':
            response = create_post(post_body)
        elif resource == 'tags':
            response = create_tag(post_body)
        elif resource == 'newposttag':
            response = tag_post(post_body)

        self.wfile.write(f"{response}".encode())

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
