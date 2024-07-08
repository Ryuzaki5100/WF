from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def home():
    print("Home")


@socketio.on("connect")
def connect_event():
    print(request.sid + " connected to me")


@socketio.on("Hi Server")
def hander(data):
    print(data)


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=8000, debug=True)
