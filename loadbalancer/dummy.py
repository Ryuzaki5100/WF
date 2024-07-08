import socketio

sio = socketio.Client()


@sio.on("connect")
def connect_event():
    print("Connected to Server")
    sio.emit("Hi Server", {"message": "Hello world"})


sio.connect("http://localhost:8000", transports=["websocket"])

while True:
    continue