import os
import base64
import subprocess
import urllib.request
import zipfile
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

port = int(os.environ.get("PORT", 8000))

u = "aHR0cHM6Ly9naXRodWIuY29tL1hUTFMvWHJheS1jb3JlL3JlbGVhc2VzL2Rvd25sb2FkL3YxLjguMjQvWHJheS1saW51eC02NC56aXA="
url = base64.b64decode(u).decode('utf-8')
urllib.request.urlretrieve(url, "data.zip")
with zipfile.ZipFile("data.zip", 'r') as z:
    z.extractall()
os.rename("xray", "engine_core
