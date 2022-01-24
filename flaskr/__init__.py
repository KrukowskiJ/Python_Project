from flask import Flask, render_template, request,  url_for, json, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)


from flaskr.models import User, Product, Newsletter, RabatCode, CustomerOrders

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.create_all()
db.session.commit()
admin = Admin(app, name='FLASK SQUAD SHOP - ADMINISTRATION PANEL', template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Newsletter, db.session))
admin.add_view(ModelView(RabatCode, db.session))
admin.add_view(ModelView(CustomerOrders, db.session))

# blueprint for auth routes in our app
from flaskr.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from flaskr import routes, models