"""
Enkel HTTP-server for Director Task-eksperimentet.
- Serverer statiske filer frå same mappe (som python -m http.server)
- POST /save  → lagrar CSV i C:\ProgramData\DirectorTask\data\  (Windows)
              eller  ~/DirectorTask/data/  (andre OS)
"""
import http.server
import os
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/save":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body)
            filename = payload["filename"]
            content = payload["content"]
            # Tillat berre enkle filnamn, ingen mappetraversering
            filename = os.path.basename(filename)
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "w", encoding="utf-8-sig") as f:
                f.write(content)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self.send_error(500, str(e))

    def log_message(self, format, *args):
        # Stillegjer logg-spam for statiske filer
        if self.path.startswith("/save") or "error" in format.lower():
            super().log_message(format, *args)


if __name__ == "__main__":
    PORT = 8080
    os.chdir(os.path.dirname(__file__))
    with http.server.ThreadingHTTPServer(("", PORT), Handler) as httpd:
        print(f"Server kjører på http://localhost:{PORT}")
        print("Trykk Ctrl+C for å stoppe.")
        httpd.serve_forever()
