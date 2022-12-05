import os
import json
import requests
from bson import json_util
from flask import Blueprint
from flask.wrappers import Response
from flask import request, current_app
from flask.globals import session
from google import auth
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from werkzeug.utils import redirect
from datetime import datetime, timedelta
from src.app.utils import verify_token
from src.app.utils import generate_jwt


CLIENT_SECRETS_FILENAME = os.environ['GOOGLE_CLIENT_SECRETS']
BACKEND_URL_STR = os.getenv('BACKEND_URL')
SCOPES = [
    'https://www.googleapis.com/auth/contacts.readonly',
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email"
]

users = Blueprint("users", __name__,  url_prefix="/users")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_config(
    client_config=json.loads(CLIENT_SECRETS_FILENAME), 
    scopes=SCOPES, 
    redirect_uri="https://superorgcontact-3fufpf5spq-rj.a.run.app/users/callbacks"
)


@users.route("/auth/google", methods=["POST"])
def auth_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return Response(
          response=json.dumps({"url": authorization_url}),
          status=200,
          mimetype="application/json",
    )


@users.route("/callbacks", methods=["GET"])
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    with open('token.json', 'w') as token:
        credJson = credentials.to_json()
        credObj = json.loads(credJson)
        credObj['refresh_token'] = None
        credJson = json.dumps(credObj)
        token.write(credJson)
    
    request_session = requests.session()
    token_google = auth.transport.requests.Request(session=request_session)

    user_google_dict = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_google,
        audience=current_app.config["GOOGLE_CLIENT_ID"],
        clock_skew_in_seconds=2
    )
    session["google_id"] = user_google_dict.get("sub")
    del user_google_dict["aud"]
    del user_google_dict["azp"]
    user_google_dict['exp'] = datetime.utcnow() + timedelta(days=1)

    token = generate_jwt(user_google_dict)

    return redirect(f"{current_app.config['FRONTEND_URL']}/#/people/contacts/{token}")


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
