from flask import Flask, render_template, jsonify
import time
import threading

app = Flask(__name__)

# Timer variables
start_time = None
elapsed_time = 0
running = False

def timer_thread():
    global elapsed_time, running, start_time
    while True:
        if running and start_time:
            elapsed_time = time.time() - start_time
        time.sleep(0.1)

# Start the timer thread
threading.Thread(target=timer_thread, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global running, start_time
    if not running:
        running = True
        start_time = time.time() - elapsed_time
    return jsonify({"status": "started", "elapsed_time": elapsed_time})

@app.route("/stop", methods=["POST"])
def stop():
    global running
    running = False
    return jsonify({"status": "stopped", "elapsed_time": elapsed_time})

@app.route("/reset", methods=["POST"])
def reset():
    global running, start_time, elapsed_time
    running = False
    start_time = None
    elapsed_time = 0
    return jsonify({"status": "reset", "elapsed_time": elapsed_time})

@app.route("/elapsed", methods=["GET"])
def get_elapsed():
    return jsonify({"elapsed_time": elapsed_time})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

