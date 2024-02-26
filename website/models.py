from .db import db
from flask_login import UserMixin
from sqlalchemy.sql import func

engine = db.create_engine('sqlite:///database.db')
# Models
class Advertisement(db.Model):
    advertisementID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(60), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.categoryID'))
    available = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text(1000))
    price = db.Column(db.Integer, nullable=False)

class User(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
    
    def get_id(self):
        return self.userID
    def __init__(self, email, username, password, is_admin=False):
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = is_admin

class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    advertisementID = db.Column(db.Integer, db.ForeignKey('advertisement.advertisementID'))
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('User', backref='comments', foreign_keys=[userID])
    
class Category(db.Model):
    categoryID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
     
    def __init__(self, name):
         self.name = name