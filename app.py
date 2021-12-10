from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/new')
@app.route('/sales')
@app.route('/shoes')
@app.route('/accessories')
@app.route('/lookbook')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/clothes')
def hello_world1():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
