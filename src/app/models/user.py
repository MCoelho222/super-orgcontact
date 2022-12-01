def create_collection_users(mongo_client):
    users_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'title': "User validation",
            'required': [
                'name',
                'email',
            ],
            'properties': {
                'name': {
                'bsonType': "string",
                'description': "The name of the authenticated user."
                },
                'email': {
                'bsonType': 'string',
                'description': "The email of the authenticated user."
                },
            },
        }
    }
    try:
        mongo_client.create_collection('users')
    except Exception as e:
        print(e)
        return {"error": "Collection exists."}
    
    mongo_client.command('collMod', 'users', validator=users_validator)