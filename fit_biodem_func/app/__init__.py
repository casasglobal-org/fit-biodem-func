""" Initializes database objects and creates method to launch flask application
https://betterprogramming.pub/flask-mysql-and-aws-a-complicated-love-triangle-8ea5588e40ac
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import database schemas
from app import models

# Databases
db = SQLAlchemy()    # <-Initialize database object
migrate = Migrate()  # <-Initialize migration object


def create_app():
    """Construct core application"""
    application = Flask(__name__)

    # Pull from config file
    application.config.from_object('config.Config')

    # Initailize database
    db.init_app(application)           # <- Gets called in our models.py file
    migrate.init_app(application, db)  # <- Migration directory

    # If this was a real flask app, you'd probably
    # add some routes to pages here
    # See https://hackersandslackers.com/flask-sqlalchemy-database-models/

    return(application)
