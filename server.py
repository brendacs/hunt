import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from model.location_model import LocationModel

FUNCTION_ROUTING = {
    "pins": {
        "GET": LocationModel.get_pins,
        "POST": LocationModel.add_pin
    }
}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        self.handle_request("GET")
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(b'Hello, world!')

    def do_POST(self):
        self.handle_request("POST")
        # content_length = int(self.headers['Content-Length'])
        # body = self.rfile.read(content_length)
        # self.send_response(200)
        # self.end_headers()
        # response = BytesIO()
        # response.write(b'This is POST request. ')
        # response.write(b'Received: ')
        # response.write(body)
        # self.wfile.write(response.getvalue())

    def do_PUT(self):
        self.handle_request("PUT")

    def handle_request(self, method):
        endpoint_regex = r'(\/api\/)(\w+)'
        matched = re.match(endpoint_regex, self.path)
        if matched:
            endpoint = matched.group(2)
            func = FUNCTION_ROUTING.get(endpoint, {}).get(method)
            if func:
                response = func()
                if error in response:
                    self.send_error(response["code"])
                    self.wfile.write(response[error])
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response)
                return
        self.send_error(404)


if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
