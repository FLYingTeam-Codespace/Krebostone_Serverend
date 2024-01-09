
from flask import Blueprint, request
import Services.Users.Users as Users
import response as resp

router = Blueprint('users', __name__, url_prefix='/users')

@router.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    loginResult = Users.login(username, password)
    if loginResult[0]:
        return resp.sendResponse(resp.SUCCESS, data={"token": loginResult[1]})
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid username or password")