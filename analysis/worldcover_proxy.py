"""Local proxy for entry 08: lets the analysis page in a browser read ESA WorldCover tiles.
ESA publishes WorldCover as cloud-optimised GeoTIFFs on a public S3 bucket, but the bucket does not send the
CORS header a browser needs. This forwards range requests to that one bucket only and adds the header.
Run it alongside `python3 -m http.server 5179`:  python3 analysis/worldcover_proxy.py   (listens on 5181)"""
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/"
PASS = ("Content-Length", "Content-Range", "Content-Type", "Accept-Ranges", "ETag", "Last-Modified")


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Range")
        self.send_header("Access-Control-Expose-Headers", ", ".join(PASS))

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def _forward(self, method):
        path = self.path.lstrip("/")
        if not path.startswith("v200/") or ".." in path:   # WorldCover v200 files only
            self.send_response(404); self._cors(); self.end_headers(); return
        req = urllib.request.Request(UPSTREAM + path, method=method)
        if self.headers.get("Range"):
            req.add_header("Range", self.headers["Range"])
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read() if method == "GET" else b""
                self.send_response(r.status)
                for h in PASS:
                    if r.headers.get(h): self.send_header(h, r.headers[h])
                self._cors(); self.end_headers(); self.wfile.write(body)
        except urllib.error.HTTPError as e:
            self.send_response(e.code); self._cors(); self.end_headers()

    def do_GET(self): self._forward("GET")
    def do_HEAD(self): self._forward("HEAD")
    def log_message(self, *a): pass


ThreadingHTTPServer(("127.0.0.1", 5181), H).serve_forever()
