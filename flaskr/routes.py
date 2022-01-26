import os
from flask import Blueprint, render_template, request,  url_for, redirect, session
from flaskr import app, db
from flaskr.models import Product,Newsletter, RabatCode, CustomerOrders
from flask_login import login_user, current_user,logout_user
import secrets
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
    return render_template('index.html', sex=sex, cart=cart)

@app.route('/<sex>/lookbook', methods=['GET', 'POST'])
def lookbook(sex):  # put application's code here
    return render_template('lookbook.html', sex=sex, items=1)


@app.route('/<sex>/<items>/<subcategory>', methods=['GET', 'POST'])
def itemspage(sex, items, subcategory):  # put application's code here
    data = Product.query.filter((Product.sex == sex) & (Product.category == items) & (Product.subcategory == subcategory))
    return render_template('items.html', sex=sex, items=items, subcategory=subcategory, items_table=data)

@app.route('/cart', methods=['POST','GET'])
def cart():
    promo = None
    if request.method == 'POST':
        code = request.form['code']
        rabat = RabatCode.query.filter((RabatCode.code == code))
        for el in rabat:
            if el.active_status == 1:
                promo = el.value/100
    total = 0
    quantity = 0
    if 'cart' in session:
        for key, el in session['cart'].items():
            total += el['price']*el['quantity']
            quantity += el['quantity']
        cart = session['cart']
        if promo:
            total = total * ( 1  - promo)
        return render_template('cart.html',  sex='men', cart=cart,quantity=quantity, total=total)
    else:
        return render_template('cart.html', sex='men')

@app.route('/cartdelete', methods=['POST','GET'])
def cartdelete():
    session.pop('cart', None)
    return redirect("/cart")

@app.route('/deleteitem', methods=['POST','GET'])
def deleteitem():
    id = request.form.get('product_id')
    print(id)
    if 'cart' not in session or len(session['cart']) <= 0:
        return redirect(url_for('redirectx'))
    try:
        session.modified = True
        for key, item in session['cart'].items():
            if key == id:
                session['cart'].pop(key, None)
    except Exception as e:
        print(e)
        return redirect(url_for('cart'))

@app.route('/order', methods=['POST','GET'])
def order():
    if 'cart' not in session or len(session['cart']) <= 0:
        return redirect(url_for('redirectx'))
    try:
        user_id = current_user.id
        invoice = secrets.token_hex(5)
        cart = session['cart']
        total = request.form.get('total_price')
        order = CustomerOrders(invoice=invoice, user_id=user_id, orders=session['cart'])
        db.session.add(order)
        db.session.commit()
        session.pop('cart',None)
        return render_template('order.html', sex='men', cart=cart, total=total)
    except Exception as e:
        print(e)
        return redirect(url_for('cart'))


@app.route('/invoice', methods=['POST', 'GET'])
def invoice():
    try:
        fv_id = request.form.get('fv_id')
        order_data = CustomerOrders.query.filter_by(invoice=fv_id).first()
        return render_template('order.html', sex='men', data=order_data)
    except Exception as e:
        print(e)
        return redirect(url_for('cart'))


@app.route('/changestatus', methods=['POST', 'GET'])
def changestatus():
    try:
        fv_id = request.form.get('fv_id')
        type = request.form.get('type')
        fv = CustomerOrders.query.filter_by(invoice=fv_id).first()
        if type == "Confirmed":
            fv.status = "Confirmed"
        elif type == "Canceled":
            fv.status = "Canceled"
        else:
            fv.status = "Sent"

        db.session.commit()
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        return redirect(request.referrer)



# TODO
# save orders to database
# KOSZYK CZYSCZENIE PRZY WYLOGOWYWANIU - ZAPISANIE W BAZIE DANYCH       !!!!!!!
# HISTORIA ZAMOWIEN - BAZA DANYCH
# FAVOURITES ITEMS
# LUPKA DO SZUKANIA