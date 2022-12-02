from flask import Blueprint
from bson import json_util
from flask.wrappers import Response
from src.app.services import main
from src.app import mongo_client
from src.app.middlewares.auth import has_logged


people = Blueprint("people", __name__, url_prefix="/people")

@people.route("/", methods=['GET'])
@has_logged()
def create_personal_info():
    try:
        user_info = main()
        user = user_info['profile']
        user_data = {
            'name': user['name'],
            'email': user['email']
        }
        contacts = user_info['contacts']
        user_exists = mongo_client.users.find_one({'email': user['email']})
        if not user_exists:
            mongo_client.users.insert_one(user_data)
            user_created = mongo_client.users.find_one({'email': user['email']})
            contacts_info = {
                'user_id': user_created['_id'],
                'contacts': contacts
                }
            mongo_client.contacts.insert_one(contacts_info)
        else:
            contacts_info = {
                'user_id': user_exists['_id'],
                'contacts': contacts
                }
            mongo_client.contacts.insert_one(contacts_info)
        return Response(
            response=json_util.dumps(user_info),
            status=200,
            mimetype="application/json")
    except Exception as e:
        print(e)
        return {'error': 'Something went wrong...'}, 500


