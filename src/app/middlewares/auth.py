from functools import wraps
from flask import request, jsonify
from src.app.utils import verify_token


def has_logged():
    def jwt_required(function_current):
        @wraps(function_current)
        def wrapper(*args, **kwargs):
            token = None
            token = request.args.get("token")
            if token:
                check = verify_token(token)
                print('CHECK', check)
                if check:
                    return function_current(*args, **kwargs)
            else:
                return jsonify({"error": "Ops, you must login!"}), 403
        return wrapper
    return jwt_required