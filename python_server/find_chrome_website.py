from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import logging

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Initialize a global variable to store the current URL
curURL = ""
curURL_lock = threading.Lock()  # Lock to synchronize access to curURL


@app.route("/receive_url", methods=["POST"])
def receive_url():
    global curURL  # Declare the variable as global to modify it
    data = request.get_json()
    url = data.get("url")
    with curURL_lock:
        curURL = url
        print(f"Received URL: {curURL}")

    return jsonify({"status": "success"}), 200


def get_current_url():
    with curURL_lock:
        return curURL


# Function to run the server in a separate thread
def start_flask_server():
    def run_server():
        # Suppress messages from Flask Server for debugging
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.CRITICAL)
        app.run(port=5000, debug=False)

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    return server_thread


# Function to stop the server
def stop_flask_server(server_thread):
    # Stop the thread
    if server_thread.is_alive():
        server_thread.join(timeout=0.25)
