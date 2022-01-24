from flaskr import db
from flask_login import UserMixin
from datetime import datetime
import json
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
    subcategory = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(120))
    desc = db.Column(db.String(420))
    price = db.Column(db.Integer)

    def __repr__(self):
        return f"Product('{self.name}', '{self.sex}' , '{self.category}')"

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), nullable=False,unique=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class RabatCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    code = db.Column(db.String(20),  nullable=False)
    value = db.Column(db.Integer, nullable=False)
    active_status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.code}' , '{self.value}')"

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice