""" Sets sqlalchemy uri variable to value specified in .env file
https://betterprogramming.pub/flask-mysql-and-aws-a-complicated-love-triangle-8ea5588e40ac
 """

import os
from dotenv import load_dotenv

# Absolute directory path
basedir = os.path.abspath(os.path.dirname(__file__))

# Looks for and loads .env file
# Can access env variables using os.environ.get(<VARNAME>)
load_dotenv(os.path.join(basedir, '.env'))


# Create config object
class Config(object):
    # Migration repository
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
 ```   

The `.env` file configuration is below. Our local repository is using sqlite, as it's a bit annoying to setup a MySQL server locally on your computer. You will need to insert the path to your local database. I save mine in a local folder in my flask app, but you can do it where ever you want.

```python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# File: .env
# 
# Environmental file to hold environmental variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

DATABASE_URL="sqlite:///path/to/local/temp.db"