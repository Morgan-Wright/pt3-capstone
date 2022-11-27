from .extensions import db
from flask_login import UserMixin

user_city = db.Table('user_city',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('city_id', db.Integer, db.ForeignKey('city.id'))
)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<City %r>' % self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    cities = db.relationship('City', secondary=user_city, backref='users')
    
    def __repr__(self):
        return '<User %r>' % self.email