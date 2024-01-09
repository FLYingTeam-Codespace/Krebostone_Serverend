
from flask import jsonify

SUCCESS = 2000
INTERNAL_SERVER_ERROR = 5000
BAD_REQUEST = 4000
NOT_FOUND = 4040
UNAUTHORIZED = 4010
FORBIDDEN = 4030

def sendResponse(statusCode, message="", data=None):
    return jsonify({
        "statusCode": statusCode,
        "message": message,
        "data": data
    })