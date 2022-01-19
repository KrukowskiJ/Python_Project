import os
from flask import  Blueprint, render_template, request,  url_for, redirect, session
from flaskr import app
from flaskr.models import Product,Newsletter
from flask_login import login_user, current_user,logout_user
from flaskr import db

def AddNewDict(a,b):
    if isinstance(a,list) and isinstance(b,list):
        return a+b
    elif isinstance(a,dict) and isinstance(b,dict):
        return dict(list(a.items())+list(b.items()))
    return False

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_name')
        quantity = 1
        product = Product.query.filter_by(name=product_id).first()

        if product_id and product and request.method == 'POST':
            NewProduct = {product_id : { 'price': product.price, 'image': product.url, 'quantity': quantity, 'description': product.desc}}
            if 'cart' in session:
                if product_id in session['cart']:
                    for key, item in session['cart'].items():
                        if key == product_id:
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['cart'] = AddNewDict(session['cart'], NewProduct)
            else:
                session['cart'] = NewProduct
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

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

@app.route('/<sex>/lookbook', methods=['GET', 'POST'])
def lookbook(sex):  # put application's code here
    return render_template('lookbook.html', sex=sex, items=1)


@app.route('/<sex>/<items>', methods=['GET', 'POST'])
def itemspage(sex, items):  # put application's code here
    data = Product.query.filter((Product.sex == sex) & (Product.category == items))
    return render_template('items.html', sex=sex, items=items,items_table=data)

@app.route('/cart')
def cart():

    if 'cart' in session:
        cart = session['cart']
        return render_template('cart.html',  sex='men', cart=cart,quantity=0, suma=0)
    else:
        return render_template('cart.html', sex='men')

@app.route('/cartdelete')
def cartdelete():
    session.pop('cart',None)
    return redirect("/cart")




# TODO
# KOSZYK ODEJMOWANIE DODAWANIE PRODUKTOW - ZWIEKSZANIE ILOSCI W KOSZYKU
# KOSZYK CZYSCZENIE PRZY WYLOGOWYWANIU - ZAPISANIE W BAZIE DANYCH       !!!!!!!
# HISTORIA ZAMOWIEN - BAZA DANYCH
# FAVOURITES ITEMS
# LUPKA DO SZUKANIA

#kody rabatowe

# WYGLAD WSZYSTKIEGO
# WYSWIETLANIE PROFILU UZYTKOWNIKA
# STOPKA NA DOLE
# NEWSLETTER FORMSY