# Directory wrangling
import os 

# Importing FLASK packages
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# SQL alchemy connector 
from flask_sqlalchemy import SQLAlchemy

# Reading the .env file
from dotenv import load_dotenv

# Importing the configuration dict 
from configuration import config

# Importing resources
from resources.Users import UserRegister, User
from resources.LogisticModel import GetPrediction

# Import database connetion
from db import db

# Loading .env to memory
load_dotenv('.env')

# Initiating the application
app = Flask(__name__)

# Enabling CORS
CORS(app)

# Loading configuration 
app.config.from_object(config[os.environ['ENV']])

# Wrapping the RESTfull API around our app
api = Api(app)

# Initializing the application
db.init_app(app)

# Registering resources 
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(GetPrediction, '/<string:version>/predict')

# Running the application 
if __name__ == '__main__':
    app.run(
        host=os.environ['HOST'],
        port=os.environ['PORT']
        )