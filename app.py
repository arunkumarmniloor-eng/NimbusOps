from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Backend Running 🚀"

@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/hostname")
def hostname():
    return {"hostname": socket.gethostname()}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)