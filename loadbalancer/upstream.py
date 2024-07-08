# server.py
from flask import Flask, request
from flask_socketio import SocketIO, emit
import sys

app = Flask(__name__)
socketio = SocketIO(app)

active_users = {}


def add_user(user_data):
    active_users[user_data["id"]] = user_data["name"]


def remove_user(user_data):
    user_id = user_data["id"]
    if user_id in active_users:
        del active_users[user_id]


@socketio.on("add_user")
def handle_add_user(data):
    add_user(data)
    emit("user_added", {"status": "success"})


@socketio.on("remove_user")
def handle_remove_user(data):
    remove_user(data)
    emit("user_removed", {"status": "success"})


@socketio.on("cache change")
def run_process():
    for user in list(active_users.keys()):
        print("Processing for user " + user)
    socketio.sleep(2)


if __name__ == "__main__":
    # task_thread = threading.Thread(target=process_tasks)
    # task_thread.start()
    socketio.run(app, host="localhost", port=int(sys.argv[1]))
