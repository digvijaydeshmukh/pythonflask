from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from settings import app
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
db = SQLAlchemy(app)
from datetime import datetime
from flask.json import JSONEncoder

class User(db.Model):
    __tablename__ = "User"
    UserId = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    BirthDate =db.Column(db.DateTime,nullable=False)

    def __repr__(self):
        return str({
            'UserName': self.UserName,
            'Password': self.Password,
            'BirthDate':self.BirthDate
        })

    def json(self):
        return {'UserName': self.UserName, 'Password': self.Password,'BirthDate': self.BirthDate}

    def username_pass_match(_username, _password):
        user = User.query.filter_by(UserName=_username).filter_by(Password=_password).first()
        if user is None:
            return False
        else:
            return True

    def getAllUser(self):
        return [User.json(emp) for emp in User.query.all()]
        # return jsonify(User.query.all())

    def createNew(_username, _password):
        newuser = User(UserName=_username, Password=_password)
        db.session.add(newuser)
        db.session.commit()
