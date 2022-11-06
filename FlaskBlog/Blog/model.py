from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    body = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', foreign_keys=[user_id])


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    age = db.Column(db.Integer())
    username = db.Column(db.String(255), unique=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    gender = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref= 'user')
    
