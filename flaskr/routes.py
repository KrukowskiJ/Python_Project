import os
from flask import  Blueprint, render_template, request,  url_for, redirect
from flaskr import app
from flaskr.models import Product,Newsletter
from flask_login import login_user, current_user,logout_user
from flaskr import db
class Cart:
  def __init__(self, count, sum, items):
    self.count = count
    self.sum = sum
    self.items = [items]

global_cart = Cart(0,0,'')
@app.route('/addcart', methods=['POST'])
def AddCart():
    product_name = request.form.get('product_name')
    product_price = int(request.form.get('product_price'))
    global_cart.sum += product_price
    global_cart.items.append(product_name)
    global_cart.count += 1
    return redirect("/cart")

@app.route('/')
def redirectx():
    return redirect("/men")

@app.route('/newsletter', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if request.form.get('subscribe'):
            new_subscriber = Newsletter(email=email, name=name)
            db.session.add(new_subscriber)
            db.session.commit()
        elif request.form.get('unsubscribe'):
            to_delete = Newsletter.query.filter(Newsletter.email == email)
            if to_delete[0]:
                db.session.delete(to_delete[0])
                db.session.commit()
    return redirect("/men")

@app.route("/<sex>", methods=['GET', 'POST'])
def start(sex):
    return render_template('index.html', sex=sex)

@app.route('/<sex>/<items>', methods=['GET', 'POST'])
def itemspage(sex, items):  # put application's code here
    data = Product.query.filter((Product.sex == sex) & (Product.category == items))
    return render_template('items.html', sex=sex, items=items,items_table=data)

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=global_cart,  sex='men')




# TODO
# KOSZYK ODEJMOWANIE DODAWANIE PRODUKTOW - ZWIEKSZANIE ILOSCI W KOSZYKU
# WYSWIETLANIE PROFILU UZYTKOWNIKA
# WYGLAD WSZYSTKIEGO
# NEWSLETTER FORMSY
# STOPKA NA DOLE
# KOSZYK CZYSCZENIE PRZY WYLOGOWYWANIU - ZAPISANIE W BAZIE DANYCH
# HISTORIA ZAMOWIEN - BAZA DANYCH
# FAVOURITES ITEMS
# LUPKA DO SZUKANIA