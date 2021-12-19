import os
from flask import Flask, render_template, request,  url_for, json,redirect
app = Flask(__name__)

class Cart:
  def __init__(self, count, sum,items):
    self.count = count
    self.sum = sum
    self.items = items

@app.route('/')
def redirect():
    return redirect("/men", code=302)

@app.route("/<sex>", methods=['GET', 'POST'])
def start(sex):
    return render_template('index.html', sex=sex)

@app.route('/<sex>/<items>', methods=['GET', 'POST'])
def itemspage(sex,items):  # put application's code here
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data = json.load(open(os.path.join(SITE_ROOT, "static", "data\data.json"), "r"))
    return render_template('items.html', sex=sex, items=items,items_table=data)

@app.route('/cart')
def cart():
    c1 = Cart(0,0,0)
    return render_template('cart.html',cart=c1,items=1)


if __name__ == '__main__':
    app.run()
