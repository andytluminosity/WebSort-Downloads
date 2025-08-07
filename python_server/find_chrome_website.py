from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

curUrl = ""
curURL_lock = threading.Lock()  # Lock to synchronize access to curURL
prevURL = ""


@app.route("/update_url", methods=["POST"])
def update_url():
    global curUrl, prevURL  # Declare the variables as global to modify it
    data = request.get_json()
    url = data.get("url")
    with curURL_lock:
        if url != prevURL:
            # Only get the main website name
            components = url.split("/")
            for comp in components:
                if "." in comp:  # The website name will have at least 1 "." from the domain name
                    if len(comp) >= 5:  # Ensure that the starting "www." is removed
                        if "www." in comp:
                            curUrl = comp[4:]
                            break
                    curUrl = comp
                    break
                curUrl = url
                prevURL = url
                print(f"Received URL: {curUrl}")

    return jsonify({"status": "success"}), 200

def get_cur_url():
    global curUrl
    return curUrl

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
