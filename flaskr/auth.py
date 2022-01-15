from flask import  Blueprint,render_template, request,  url_for, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models import User
from flaskr import db
from flask_login import login_user, current_user,logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('auth/login.html',sex="men")

@auth.route('/signup')
def signup():
    return render_template('auth/register.html',sex="men")

@auth.route('/logout')
def logout():
    session.pop('email', None)
    logout_user()
    return redirect('panel')

@auth.route('/user',methods = ['POST', 'GET'])
def user():
    user = current_user
    return render_template('profile.html',sex='men',user=user)

@auth.route('/panel',methods = ['POST', 'GET'])
def panel():
    return render_template('loginpanel.html',sex='men')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists, take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    print(current_user)
    return redirect('user')