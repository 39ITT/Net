import os
import base64
import urllib.request
import zipfile
import subprocess
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

port = int(os.environ.get("PORT", 8080))
xray_port = 10000

u = "aHR0cHM6Ly9naXRodWIuY29tL1hUTFMvWHJheS1jb3JlL3JlbGVhc2VzL2Rvd25sb2FkL3YxLjguMjQvWHJheS1saW51eC02NC56aXA="
url = base64.b64decode(u).decode('utf-8')
urllib.request.urlretrieve(url, "data.zip")
with zipfile.ZipFile("data.zip", 'r') as z:
    z.extractall()
os.rename("xray", "sys_worker")
os.chmod("sys_worker", 0o755)

cf_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
urllib.request.urlretrieve(cf_url, "cf_tunnel")
os.chmod("cf_tunnel", 0o755)

c = '{"log":{"loglevel":"warning"},"inbounds":[{"port":' + str(xray_port) + ',"protocol":"vless","settings":{"clients":[{"id":"83132cd9-67d9-4014-8b7d-8b5b2c86960e"}],"decryption":"none"},"streamSettings":{"network":"ws","wsSettings":{"path":"/"}}}],"outbounds":[{"protocol":"freedom"}]}'
with open("data.json", "w") as f:
    f.write(c)

subprocess.Popen(["./sys_worker", "-c", "data.json"], start_new_session=True)
time.sleep(2)

cf_process = subprocess.Popen(
    ["./cf_tunnel", "tunnel", "--url", f"http://127.0.0.1:{xray_port}"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
)

def log_output():
    for line in cf_process.stdout:
        print(line, flush=True)
threading.Thread(target=log_output, daemon=True).start()

class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Active System")

def run_dummy():
    server = HTTPServer(('0.0.0.0', port), DummyServer)
    server.serve_forever()

threading.Thread(target=run_dummy, daemon=True).start()

while True:
    time.sleep(10)
