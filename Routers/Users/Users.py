
from flask import Blueprint, request
import Services.Users.Users as Users
import response as resp
import Services.Token.Token as Token

router = Blueprint('users', __name__, url_prefix='/users')

@router.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    loginResult = Users.login(username, password)
    if loginResult[0]:
        return resp.sendResponse(resp.SUCCESS, data={"token": loginResult[1], "needReset": loginResult[2]})
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid username or password")

@router.route('/loginWithToken', methods=['POST'])
def loginWithToken():
    token = request.headers.get('Authorization')
    if Users.loginWithToken(token):
        return resp.sendResponse(resp.SUCCESS, "Login success")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    pass

@router.route('/changePassword', methods=['POST'])
def changePassword():
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    username = data["username"]
    newPassword = request.get_json().get('newPassword')
    if Users.changePassword(username, newPassword)[0]:
        return resp.sendResponse(resp.SUCCESS, "Password changed", data={"token": Users.changePassword(username, newPassword)[1]})
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid username")
    pass

@router.route('/getUserInfo', methods=['POST'])
def getUserInfo():
    data = Token.parseToken(request.headers.get('Authorization'))
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    username = data["username"]
    userInfo = Users.getUserInfo(username)
    if userInfo != None:
        return resp.sendResponse(resp.SUCCESS, data=userInfo)
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid username")
    pass

@router.route('/changeNickname', methods=['POST'])
def changeNickname():
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    username = data["username"]
    newNickname = request.get_json().get('newNickname')
    if Users.changeNickname(username, newNickname):
        return resp.sendResponse(resp.SUCCESS, "Nickname changed")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid username")
    pass

@router.route('/getUserInfoWithID', methods=['POST'])
def getUserInfoWithID():
    data = Token.parseToken(request.headers.get('Authorization'))
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    userID = data["id"]
    userInfo = Users.getUserInfoWithID(userID)
    if userInfo != None:
        return resp.sendResponse(resp.SUCCESS, data=userInfo)
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid id")