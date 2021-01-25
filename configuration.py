# Directory traversal
import os 

# ENV variables
from dotenv import load_dotenv

# Loading the dotenv file
APP_ROOT = os.path.join(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# Defining the configuration classes
class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')


class Prod(Config):
    DEBUG = False


class Dev(Config):
    SQLALCHEMY_DATABASE_URI = f"""sqlite:///data.db"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Creating the configuration object 
config = {
    'Dev':Dev,
    'Prod':Prod
}