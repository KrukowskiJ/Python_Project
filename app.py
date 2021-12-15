import os
from flask import Flask, render_template, request,  url_for, json
app = Flask(__name__)



sex = "Men"
@app.route("/", methods=['GET', 'POST'])
def index():
    global sex
    if request.method == 'POST':
        if request.form.get('action1') == 'Men':
            sex = request.form.get('action1')
        elif request.form.get('action2') == 'Women':
            sex = request.form.get('action2')
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html', sex=sex)

@app.route('/<x>', methods=['GET', 'POST'])
def hello_world(x):  # put application's code here
    global sex
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data = json.load(open(os.path.join(SITE_ROOT, "static", "data\data.json"), "r"))
    if request.method == 'POST':
        if request.form.get('action1') == 'Men':
            sex = request.form.get('action1')
        elif request.form.get('action2') == 'Women':
            sex = request.form.get('action2')
        return render_template('items.html', sex=sex, items=x,items_table=data)
    else:
        return render_template('items.html', sex=sex, items=x,items_table=data)

if __name__ == '__main__':
    app.run()
