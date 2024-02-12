from . import db
from flask_login import UserMixin

#Models
class Advertisement(db.Model):
    advertisementID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey)
    category = db.Column(db.String, nullable=False)
    available = db.Column(db.Boolean, default=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer(7), nullable=False)
    date = db.Column(db.Date)

    user = db.relationship('User', backref='advertisements', foreign_keys=[userID])


class User(db.Model, UserMixin):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    def get_id(self):
        return (self.userID)


class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey)
    advertisementID = db.Column(db.Integer, db.ForeignKey)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date)

    user = db.relationship('User', backref='comments', foreign_keys=[userID])
    advertisement = db.relationship('Advertisement', backref='comments', foreign_keys=[advertisementID])