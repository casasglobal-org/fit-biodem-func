""" Creates sql tables for use by flask
https://betterprogramming.pub/flask-mysql-and-aws-a-complicated-love-triangle-8ea5588e40ac
 """

from datetime import datetime

from app import db  # Not sure what this does


class testDB(db.Model):
    """testDB extends db.Model class, or creates a database from
        db.Model class


       Columns
         string_column  : column with strings
         integer_column : column with integers
         date_column    : column with dates, default is current date

    """

    # String Column
    #
    # This is the primary key of the database
    # It is of type = string with max characters = 140
    string_column = db.Column(db.String(140), primary_key=True)
    # Integer Column
    integer_column = db.Column(db.Integer)
    # Date Column
    date_column = db.Column(db.DateTime, default=datetime.utcnow)
