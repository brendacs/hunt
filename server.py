import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from model.location_model import LocationModel
from model.user_creation import User

ROUTING = {
    "pins": {
        "GET": (
            LocationModel.get_pins,
            {
                "latitude": float,
                "longitude": float,
                "parkId": str
            }
        ),
        "POST": (
            LocationModel.add_pin,
            {
                "parkId": str,
                "name": str,
                "latitude": float,
                "longitude": float
            }
        )
    },
    "park": {
        "GET": (
            LocationModel.get_closest_park,
            {
                "latitude": float,
                "longitude": float,
                "radius": float,
            }
        )
    },
    "user": {
        "POST": (
            User.register,
            {
                "username": str,
                "email": str,
                "password": str,
            }
        ),
        "PUT": (
            User.login,
            {
                "username": str,
                "password": str
            }
        )
    }
}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler): 
    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PUT(self):
        self.handle_request("PUT")

    def handle_request(self, method):
        endpoint_regex = r'(\/api\/)(\w+)'
        path = re.match(endpoint_regex, self.path)
        if path:
            endpoint = path.group(2)
            routes = ROUTING.get(endpoint, {}).get(method)
            if routes:
                func, args = routes
                try:
                    model_vars = self.payload_to_args(args)
                    response = func(model_vars) 
                except Exception as e:
                    response = {"code": 400, "error": "Invalid Payload."}
                if response:
                    if "error" in response:
                        self.send_error(response["code"], message=response["error"])
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.end_headers()
                return
        self.send_error(404)

    def payload_to_args(self, args):
        content_length = int(self.headers.get('Content-Length', 0))
        if not content_length:
            if args:
                raise RuntimeError
            return {}
        payload = json.loads(self.rfile.read(content_length))
        variables = {}
        for var_name, var_type in args.items():
            if var_name not in payload:
                raise RuntimeError
            variables[var_name] = var_type(payload[var_name])
        return variables


if __name__ == "__main__":
    httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
