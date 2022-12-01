__version__ = '0.1.0'

import os
from flask import Flask
from flask_cors import CORS
from src.app.config import app_config
from src.app.utils import mongo
from src.app.models.contact import create_collection_contacts
from src.app.models.user import create_collection_users

app = Flask(__name__)
env = os.getenv('FLASK_ENV')
app.config.from_object(app_config[env])
CORS(app)

mongo_client = mongo[os.getenv('MONGO_DATABASE_DEV')]

create_collection_contacts(mongo_client=mongo_client)
create_collection_users(mongo_client=mongo_client)