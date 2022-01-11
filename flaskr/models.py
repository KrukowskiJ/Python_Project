from flaskr import db
from flask_login import UserMixin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    sex = db.Column(db.String(10),  nullable=False)
    category = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(120))
    desc = db.Column(db.String(420))
    price = db.Column(db.Integer)

    def __repr__(self):
        return f"Product('{self.name}', '{self.sex}' , '{self.category}')"

class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Color('{self.name}')"

class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"Size('{self.name}')"

class Available_Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

