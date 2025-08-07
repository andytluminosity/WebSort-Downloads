from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

curURL_lock = threading.Lock()  # Lock to synchronize access to curURL
prevURL = ""


@app.route("/receive_url", methods=["POST"])
def update_url():
    global cur_website_name, prevURL  # Declare the variable as global to modify it
    data = request.get_json()
    url = data.get("url")
    with curURL_lock:
        if url != prevURL:
            cur_website_name = url
            prevURL = url
            print(f"Received URL: {url}")

    return jsonify({"status": "success"}), 200


# Function to run the server in a separate thread
def start_flask_server():
    def run_server():
        app.run(port=5000, debug=True, use_reloader=False)

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    return server_thread


# Function to stop the server
def stop_flask_server(server_thread):
    # Stop the thread
    if server_thread.is_alive():
        server_thread.join(timeout=0.25)
