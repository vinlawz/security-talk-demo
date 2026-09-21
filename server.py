# Demo local API mock
# Accepts a fake bearer token and returns fake customer data.
# Use this for a live security talk / demo.

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

ALLOWED_TOKENS = {
    "demo_live_key_do_not_use",
}


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/customers":
            auth = self.headers.get("Authorization", "")
            token = auth.replace("Bearer ", "", 1).strip() if auth.startswith("Bearer ") else ""

            if token in ALLOWED_TOKENS:
                body = {
                    "status": "authenticated",
                    "customers": [
                        {"id": "customer-001", "email": "alice@example.test"},
                        {"id": "customer-002", "email": "bob@example.test"},
                    ],
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(body).encode("utf-8"))
                return

            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "unauthorized"}).encode("utf-8"))
            return

        if parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            return

        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "not_found"}).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/revoke":
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = 0

            raw = self.rfile.read(length).decode("utf-8") if length else ""
            payload = json.loads(raw) if raw else {}
            token = payload.get("token", "")

            if token:
                ALLOWED_TOKENS.discard(token)
                response = {"status": "revoked", "token": token}
            else:
                response = {"error": "missing_token"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        self.send_response(405)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "method_not_allowed"}).encode("utf-8"))

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 9000
    server = HTTPServer((host, port), DemoHandler)
    print(f"Mock API running at http://{host}:{port}")
    print("Allowed token: demo_live_key_do_not_use")
    server.serve_forever()
