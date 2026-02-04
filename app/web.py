from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "index.html"


class ReviewManagerHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/", "/index.html"):
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return

        content = TEMPLATE_PATH.read_text(encoding="utf-8")
        encoded = content.encode("utf-8")

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    server = HTTPServer(("0.0.0.0", 8000), ReviewManagerHandler)
    print("Review Manager web UI running on http://localhost:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
