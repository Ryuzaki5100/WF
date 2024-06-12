import bcrypt
import asyncio
from flask import Flask, Request, Response,redirect,request,make_response,url_for
from flask_socketio import SocketIO, emit
from userCache import ActiveUser
from ApiResponse import ApiResponse, API_Response
# pip install Flask[async]

app = Flask(__name__)
socketio = SocketIO(app)
frontend_URL = 'https://www.youtube.com/'

# Socket Events
@socketio.on('connect')
def connectClientEvent():
    wallet_id = request.cookies.get('wallet_id')
    socket_id = request.sid
    wallet_balance = None # Perform Database Query for Wallet Balance
    activeUser = ActiveUser(wallet_id=wallet_id,socket_id=socket_id,wallet_balance=wallet_balance)
    # Store activeUser in the cache
    emit('Script Connect',ApiResponse(message="Arbitrage Bot Connected",statusCode=200),room=socket_id)
    
# App Routes
@app.route("/login",methods=['POST'])
async def login():
    userData = request.get_json()
    username = userData.get('username')
    password = userData.get('password')
    user = None # Perform Database Query for Finding the User based on (username)
    if user is None:
        return API_Response(message="User doesn't exist",statusCode=404)
    hashedPassword = bcrypt.hashpw(password=password,salt=bcrypt.gensalt())
    if user.password != hashedPassword: # Replace user.password with according syntax
        return API_Response(message="Incorrect Password Entered!!",statusCode=401)
    response = API_Response(message="Log in Successfull",statusCode=200)
    response.set_cookie('wallet_id',user.wallet_id) # Replace user.wallet_id with according syntax
    return response
    
@app.route("/logout")
async def logout():
    response = API_Response(message="Log out Successfull",statusCode=200)
    response.delete_cookie('wallet_id')
    return redirect(location=frontend_URL)

@app.route("/signup",methods=['POST'])
async def signup():
    userData = request.get_json()
    wallet_id = userData.get('wallet_id')
    username = userData.get('username')
    password = userData.get('password')
    user = None # Perform Database Query for Finding the User based on (username or wallet_id)
    if user is not None:
        return API_Response(message="Credentials already taken!!",statusCode=409)
    response = API_Response(message="Sign up successfull",statusCode=200)
    
if __name__ == '__main__':
    socketio.run(app,host='localhost',port=5000)
    
# env variables
# frontend port address
