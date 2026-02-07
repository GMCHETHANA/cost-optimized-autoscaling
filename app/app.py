from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello from pod: {socket.gethostname()}"

app.run(host="0.0.0.0", port=80)

@app.route("/load")
def cpu_load():
    x = 0
    for i in range(10_000_000):
        x += i*i
    return f"CPU load done: {x}"

