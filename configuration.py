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
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Prod(Config):
    PS_HOST = os.environ.get('POSTGRE_HOST')
    PS_DB = os.environ.get('POSTGRE_DB')
    PS_PSW = os.environ.get('POSTGRE_PASSWORD')
    PS_PORT = os.environ.get('POSTGRE_PORT')
    SQLALCHEMY_DATABASE_URI = f"""postgresql://postgres:{PS_PSW}@{PS_HOST}:{PS_PORT}/{PS_DB}"""
    DEBUG = False


class Dev(Config):
    SQLALCHEMY_DATABASE_URI = f"""sqlite:///data.db"""
    

# Creating the configuration object 
config = {
    'Dev':Dev,
    'Prod':Prod
}