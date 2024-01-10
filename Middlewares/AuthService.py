from functools import wraps
from flask import request, jsonify
import Services.Token.Token as Token
import response as resp
import logger

__log = logger.Logger("MCServer|AuthService", True)

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            __log.printwarning("Blocked unauthorized access to API: No token provided")
            return resp.sendResponse(resp.UNAUTHORIZED, "No token provided")
        if Token.verifyToken(token) == False:
            __log.printwarning("Blocked unauthorized access to API: Invalid token")
            return resp.sendResponse(resp.UNAUTHORIZED, "Invalid token")
    return decorated_function

def tokenBlocker():
    token = request.headers.get('Authorization')
    if token is None:
        __log.printwarning("Blocked unauthorized access to API: No token provided")
        return resp.sendResponse(resp.UNAUTHORIZED, "No token provided")
    if Token.verifyToken(token) == False:
        __log.printwarning("Blocked unauthorized access to API: Invalid token")
        return resp.sendResponse(resp.UNAUTHORIZED, "Invalid token")