def create_collection_contacts(mongo_client):
    contacts_validator = {
        '$jsonSchema': {
            'bsonType': 'object',
            'title': "Contacts validation",
            'required': [
                'user_id',
                'contacts',
            ],
            'properties': {
                'user_id': {
                'bsonType': "objectId",
                'description': "The object id of the authenticated user."
                },
                'contacts': {
                'bsonType': 'object',
                'description': "The Object with user's contacts separated by domain."
                },
            },
        }
    }
    try:
        mongo_client.create_collection('contacts')
    except Exception as e:
        print(e)
        return {"error": "Collection exists."}
    
    mongo_client.command('collMod', 'contacts', validator=contacts_validator)