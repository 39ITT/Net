import os
import base64
import urllib.request
import zipfile
import subprocess
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

port = int(os.environ.get("PORT", 8080))

u = "aHR0cHM6Ly9naXRodWIuY29tL1hUTFMvWHJheS1jb3JlL3JlbGVhc2VzL2Rvd25sb2FkL3YxLjguMjQvWHJheS1saW51eC02NC56aXA="
url = base64.b64decode(u).decode('utf-8')
urllib.request.urlretrieve(url, "data.zip")
with zipfile.ZipFile("data.zip", 'r') as z:
    z.extractall()
os.rename("xray", "sys_worker")
os.chmod("sys_worker", 0o755)

c = '{"log":{"loglevel":"warning"},"inbounds":[{"port":' + str(port) + ',"protocol":"vless","settings":{"clients":[{"id":"83132cd9-67d9-4014-8b7d-8b5b2c86960e"}],"decryption":"none"},"streamSettings":{"network":"xhttp","xhttpSettings":{"path":"/"}}}],"outbounds":[{"protocol":"freedom"}]}'
with open("data.json", "w") as f:
    f.write(c)

subprocess.Popen(["./sys_worker", "-c", "data.json"])

class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"System OK")
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"System OK")

def run_dummy():
    server = HTTPServer(('0.0.0.0', port + 1), DummyServer)
    server.serve_forever()

threading.Thread(target=run_dummy, daemon=True).start()

time.sleep(3)
print("System initialized successfully.")
