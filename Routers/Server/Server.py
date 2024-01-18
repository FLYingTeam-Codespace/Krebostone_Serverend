
from flask import Blueprint, request
import response as resp
import Services.Token.Token as Token
import Services.Server.Server as Server

router = Blueprint('server', __name__, url_prefix='/server')

@router.route('/getAll', methods=['POST'])
def getFullServerInfo():
    # Check user token first
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    # Return server info
    return resp.sendResponse(resp.SUCCESS, data=Server.getFullServerInfo())