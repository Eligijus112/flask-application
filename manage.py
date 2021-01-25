# Managing paths
import os

# Flask related packages
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# Importing both db connection and the application
from app import app, db

# Importing the configuration dict 
from configuration import config

app.config.from_object(config[os.environ['ENV']])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()