import socketio
from flask import Flask, request, Response, jsonify
from flask_socketio import SocketIO


app = Flask(__name__)
s = SocketIO(app)
sio1 = socketio.Client()
sio2 = socketio.Client()


@app.route("/add/<id>/<name>")
def add(id, name):
    sio1.emit("add_user", {"id": id, "name": name})
    return jsonify(), 200


@app.route("/del/<id>/<name>")
def de(id, name):
    sio1.emit("remove_user", {"id": id, "name": name})
    return jsonify(), 200


if __name__ == "__main__":
    sio1.connect("http://localhost/", transports=["websocket"])
    sio2.connect("http://localhost/", transports=["websocket"])
    s.run(app, host="localhost", port=3001, debug=True)
