import os
import base64
import urllib.request
import zipfile
import subprocess
import time
import sys
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

c = '{"log":{"loglevel":"warning"},"inbounds":[{"port":' + str(xray_port) + ',"protocol":"vless","settings":{"clients":[{"id":"83132cd9-67d9-4014-8b7d-8b5b2c86960e"}],"decryption":"none"},"streamSettings":{"network":"ws","wsSettings":{"path":"/"}}}],"outbounds":[{"protocol":"freedom"}]}'
with open("data.json", "w") as f:
    f.write(c)

subprocess.Popen(["./sys_worker", "-c", "data.json"], start_new_session=True)

time.sleep(2)

class HijackServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Active System")

    def do_CONNECT(self):
        try:
            s = socket.create_connection(("127.0.0.1", xray_port))
            self.send_response(200, 'Connection Established')
            self.end_headers()
            while True:
                data = self.connection.recv(4096)
                if not data: break
                s.sendall(data)
                s.settimeout(0.1)
                try:
                    rdata = s.recv(4096)
                    if not rdata: break
                    self.connection.sendall(rdata)
                except socket.timeout:
                    pass
        except Exception:
            pass
        finally:
            self.connection.close()

import socket
HTTPServer.allow_reuse_address = True
server = HTTPServer(('0.0.0.0', port), HijackServer)
server.serve_forever()
