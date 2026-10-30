import os
import base64
import urllib.request
import zipfile
import subprocess
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

port = int(os.environ.get("PORT", 8080))
dummy_port = port + 1

u = "aHR0cHM6Ly9naXRodWIuY29tL1hUTFMvWHJheS1jb3JlL3JlbGVhc2VzL2Rvd25sb2FkL3YxLjguMjQvWHJheS1saW51eC02NC56aXA="
url = base64.b64decode(u).decode('utf-8')
urllib.request.urlretrieve(url, "data.zip")
with zipfile.ZipFile("data.zip", 'r') as z:
    z.extractall()
os.rename("xray", "sys_worker")
os.chmod("sys_worker", 0o755)

c = '{"log":{"loglevel":"warning"},"inbounds":[{"port":' + str(port) + ',"protocol":"vless","settings":{"clients":[{"id":"83132cd9-67d9-4014-8b7d-8b5b2c86960e"}],"decryption":"none"},"streamSettings":{"network":"ws","wsSettings":{"path":"/api/v1/stream"}},"fallbacks":[{"dest":' + str(dummy_port) + '}]}],"outbounds":[{"protocol":"freedom"}]}'
with open("data.json", "w") as f:
    f.write(c)

subprocess.Popen(["./sys_worker", "-c", "data.json"], start_new_session=True)
time.sleep(2)

class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Active System")
    def do_HEAD(self):
        self.do_GET()

def run_dummy():
    try:
        server = HTTPServer(('0.0.0.0', dummy_port), DummyServer)
        server.serve_forever()
    except Exception:
        pass

threading.Thread(target=run_dummy, daemon=True).start()

print("System running...")
while True:
    time.sleep(10)
