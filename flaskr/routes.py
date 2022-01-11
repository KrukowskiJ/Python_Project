import os
from flask import  Blueprint, render_template, request,  url_for, redirect
from flaskr import app
from flaskr.models import Product


class Cart:
  def __init__(self, count, sum, items):
    self.count = count
    self.sum = sum
    self.items = [items]

global_cart = Cart(0,0,'')
@app.route('/addcart', methods=['POST'])
def AddCart():
    product_name =request.form.get('product_name')
    product_price = int(request.form.get('product_price'))
    global_cart.sum += product_price
    global_cart.items.append(product_name)
    global_cart.count += 1
    return redirect("/cart")

@app.route('/')
def redirectx():
    return redirect("/men")

@app.route('/<x>/profile')
def profile(x):
    return render_template('profile.html')

@app.route("/<sex>", methods=['GET', 'POST'])
def start(sex):
    return render_template('index.html', sex=sex)

@app.route('/<sex>/<items>', methods=['GET', 'POST'])
def itemspage(sex, items):  # put application's code here
    data = Product.query.filter((Product.sex == sex) & (Product.category == items))
    return render_template('items.html', sex=sex, items=items,items_table=data)

@app.route('/cart')
def cart():
    return render_template('cart.html',cart=global_cart,items=1)

@app.route('/user',methods = ['POST', 'GET'])
def user():
    return render_template('profile.html')

@app.route('/panel',methods = ['POST', 'GET'])
def panel():
    return render_template('loginpanel.html')