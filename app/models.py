# models.py

from flask_login import UserMixin
from . import db
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    photo = db.Column(db.String(100))
 

class Messages(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(100), unique=True)
    course_name = db.Column(db.String(100), nullable=False, default='DCU - GDWT')    # setting a default course for this project
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=False)

 
    def __repr__(self):
        return '(%r,)' % self.id