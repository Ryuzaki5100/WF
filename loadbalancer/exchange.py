import time
import socketio
import threading
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
s = SocketIO(app)

flask_servers = [
    "http://localhost:8001",
    "http://localhost:8002",
    # "http://localhost:8003",
    # "http://localhost:8004",
    # "http://localhost:8005",
]

sio_clients = [socketio.Client() for _ in flask_servers]

for i in range(2):
    sio_clients[i].connect(flask_servers[i], transports=["websocket"])


def update_exchange_values():
    while True:
        # Emit an event to each Flask server to trigger task processing
        print("New value")
        for sio_client in sio_clients:
            sio_client.emit("cache change")
        time.sleep(10)  # Run the update every 10 seconds


if __name__ == "__main__":
    thread = threading.Thread(target=update_exchange_values)
    thread.start()
    s.run(app, host="localhost", port=3000, debug=True)
