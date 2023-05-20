import os
from bson import json_util
from flask import Blueprint
from flask.wrappers import Response
from flask import request
from src.app.utils import verify_token


users = Blueprint("users", __name__,  url_prefix="/users")

@users.route("/verify/", methods=['GET'])
def auth_jwt():
    token = request.args.get('token')
    check_token = verify_token(token)
    if check_token:
        response = {'status': 'true'}
    else:
        response = {'status': 'false'}
    return Response(
        response=json_util.dumps(response),
        status=201,
        mimetype="application/json")


@users.route("/logout", methods=['GET'])
def user_logout():
    try:
        if os.path.exists('token.json'):
            os.remove('token.json')
            return {'success': 'Token removed.'}, 200
        else:
            return {'success': 'No token to be removed.'}, 200
    except Exception:
        return {"error": "Token could not be removed."}, 500
