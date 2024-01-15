from flask import Blueprint, request
import response as resp
import Services.Token.Token as Token
import Services.UserAccess.UserAccess as UserAccess
import Services.Bulletin.Bulletin as Bulletin

router = Blueprint('bulletin', __name__, url_prefix='/bulletin')

@router.route('/add', methods=['POST'])
def addBulletin():
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    if UserAccess.getAccess(data["username"], UserAccess.ACCESSES_KEYS["addBulletin"]):
        title = request.get_json().get('title')
        content = request.get_json().get('content')
        if title == None or content == None:
            return resp.sendResponse(resp.FORBIDDEN, "No title or content provided")
        result = Bulletin.appendBulletin(title, content, data["id"])
        if result[0]:
            return resp.sendResponse(resp.SUCCESS, "Bulletin added", data=result[1])
        else:
            return resp.sendResponse(resp.FORBIDDEN, "Failed to add bulletin")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "You don't have permission to add bulletin")
    
@router.route('/getLatest', methods=['POST'])
def getLatestBulletin():
    result = Bulletin.getBulletin()
    if result[0]:
        return resp.sendResponse(resp.SUCCESS, "Bulletin found", data=result[1][-1])
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Bulletin not found")

@router.route('/getAll', methods=['POST'])
def getAllBulletin():
    result = Bulletin.getBulletin()
    if result[0]:
        return resp.sendResponse(resp.SUCCESS, "Bulletin found", data=result[1])
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Bulletin not found")
    
@router.route('/remove', methods=['POST'])
def removeBulletin():
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    if UserAccess.getAccess(data["username"], UserAccess.ACCESSES_KEYS["removeBulletin"]):
        targetID = request.get_json().get('id')
        if targetID == None:
            return resp.sendResponse(resp.FORBIDDEN, "No id provided")
        if Bulletin.removeBulletin(targetID):
            return resp.sendResponse(resp.SUCCESS, "Bulletin removed")
        else:
            return resp.sendResponse(resp.FORBIDDEN, "Failed to remove bulletin")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "You don't have permission to remove bulletin")
