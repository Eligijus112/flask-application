# Managing paths
import os

# Data wrangling 
import pandas as pd

# Reading model files
import pickle

# Flask related packages
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# Importing both db connection and the application
from app import app, db

# Importing the configuration dict 
from configuration import config

# Importing model to store the logistic regression model 
from models.LogisticModel import LogisticModel

app.config.from_object(config[os.environ['ENV']])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# Adding a manager command to store logistic regression model in db 
@manager.command 
def add_model(version):
    """
    Ads a model with a specific version to the database
    """
    # Reading the model file 
    if os.path.isfile(f"LRmodels/model_{version}.sav"):
        model = pickle.load(open(f"LRmodels/model_{version}.sav", 'rb'))

        # Extracting the coefficient values 
        coefs = [model.intercept_[0]] + [x for x in model.coef_[0]]

        # Extracting the feature names 
        feature_names = ['intercept'] + model.feature_names

        # Creating a dataframe to write the coefficients in 
        modelDf = pd.DataFrame({
            'version': version, 
            'feature': feature_names,
            'coef': coefs 
        })

        # Checking if the current version of model exists
        if LogisticModel.query.filter_by(version=version).first() is not None:
            LogisticModel.query.filter_by(version=version).delete()

        for _, row in modelDf.iterrows():
            obj = LogisticModel(version, row['feature'], row['coef'])
            obj.add_to_db()

if __name__ == '__main__':
    manager.run()