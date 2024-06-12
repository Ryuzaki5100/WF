import json
from flask import Response,redirect

class ApiResponse:
    def __init__(self,data=None,message=None,statusCode=200):
        self.data = data
        self.message = message
        self.statusCode = statusCode
    def to_json(self):
        responseDictionary = {
            'data':self.data,
            'message':self.message,
            'statusCode':self.statusCode
        }
        return json.dumps(responseDictionary)
    
def API_Response(data=None,message='',statusCode=200):
    return Response(response=ApiResponse(data=data,message=message,statusCode=statusCode).to_json())
    
