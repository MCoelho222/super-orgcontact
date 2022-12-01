import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    SECRET_KEY = os.getenv('SECRET_KEY')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    BACKEND_URL = os.getenv('BACKEND_URL')
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    MONGO_URI = os.getenv("MONGO_URI")

class Development(Config):
    TESTING = False 
    DEBUG = True
    DATABASE = os.getenv('MONGO_DATABASE_DEV')
    MONGO_URI = Config.MONGO_URI + DATABASE

class Production(Config):
    TESTING = False 
    DEBUG = False
    DATABASE = os.getenv('MONGO_DATABASE_PROD')
    MONGO_DB = f"{Config.MONGO_URI}{DATABASE}"
   
class Testing(Config):
    DEBUG = False
    TESTING = True
    DATABASE = os.getenv('MONGO_DATABASE_TEST')
    MONGO_DB = f"{Config.MONGO_URI}{DATABASE}"

   
app_config = {
    "development": Development,
    "production": Production,
    "testing": Testing
}