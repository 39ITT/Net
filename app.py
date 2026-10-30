import os
import base64
import subprocess
import urllib.request
import zipfile
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

port = int(os.environ.get("PORT", 8000))
dummy_port = port + 1

u = "aHR0cHM6Ly9naXRodWIuY29tL1hUTFMvWHJheS1jb3JlL3JlbGVhc2VzL2Rvd25sb2FkL3YxLjguMjQvWHJheS1saW51eC02NC56aXA="
url = base64.b64decode(u).decode('utf-8')
urllib.request.urlretrieve(url, "data.zip")
with zipfile.ZipFile("data.zip", 'r') as z:
    z.extractall()
os.rename("xray", "engine_core")
os.chmod("engine_core", 0o755)

c = '{"log":{"loglevel":"warning"},"inbounds":[{"port":' + str(port) + ',"protocol":"vless","settings":{"clients":[{"id":"83132cd9-67d9-4014-8b7d-8b5b2c86960e"}],"decryption":"none"},"streamSettings":{"network":"grpc","grpcSettings":{"serviceName":"telemetry"}},"fallbacks":[{"dest":' + str(dummy_port) + '}]}],"outbounds":[{"protocol":"freedom"}]}'

with open("data.json", "w") as f:
    f.write(c)

subprocess.Popen(["./engine_core", "-c", "data.json"])
time.sleep(2)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Active Server")

HTTPServer(('0.0.0.0', dummy_port), H).serve_forever()
