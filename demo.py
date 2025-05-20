# demo.py

import subprocess
import time
import http.client
import json
import os
import signal

# 1) Launch the microservice as a separate process
proc = subprocess.Popen(
    ["python", "sprint2.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)
time.sleep(2)  # give it time to start

def do_request(path):
    conn = http.client.HTTPConnection("127.0.0.1", 8080)
    print(f">>> REQUEST: GET {path}")
    conn.request("GET", path)
    res = conn.getresponse()
    print(f">>> STATUS: {res.status} {res.reason}")
    raw = res.read().decode()
    try:
        data = json.loads(raw)
        print(">>> JSON BODY:")
        print(json.dumps(data, indent=2))
    except Exception:
        print(">>> BODY:")
        print(raw)
        data = None
    print()
    conn.close()
    return data

# 2) Root
root = do_request("/")

# 3) Health
health = do_request("/health")

# 4) Songs since 2025‑05‑02
songs_only_since_0502 = do_request(
    "/activity?user_id=1234&week_start=2025-05-02&media_type=song"
)

# 5) Podcast‑only since 2025‑05‑01
podcast_only = do_request(
    "/activity?"
    "user_id=1234&week_start=2025-05-01&media_type=podcast"
)

# 6) All‑media since 2025‑05‑01 — should include the podcast plus songs
all_media = do_request("/activity?user_id=1234&week_start=2025-05-01")
count = len(all_media.get("recent_activity", []))
print(f"Detected {count} items in recent_activity")
if count <= 5:
    print("recent_activity correctly limited to 5 or fewer entries")
else:
    print("recent_activity returned more than 5 entries")

# 7) Shut down microservice
os.kill(proc.pid, signal.SIGINT)
proc.wait()