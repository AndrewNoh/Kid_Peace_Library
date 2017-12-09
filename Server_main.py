from flask import Flask,redirect,url_for
from flask.templating import render_template

app = Flask(__name__)


@app.route('/base')
def base_index():
    return render_template('base.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Login')
def login_form():
    return render_template('login.html')

@app.route('/Sginup')
def signup_form():
    return render_template('signup.html')

@app.route('/Board')
def board_form():
    return render_template('board.html')

@app.route('/Write')
def write_form():
    return render_template('write.html')

@app.route('/backgroundimg1')
def backgroundimg1():
    return redirect(url_for('static', filename='img/Main_img1.jpg'))

@app.route('/backgroundimg2')
def backgroundimg2():
    return redirect(url_for('static', filename='img/Main_img2.png'))

@app.route('/backgroundimg3')
def backgroundimg3():
    return redirect(url_for('static', filename='img/Main_img3.jpg'))

if __name__ == '__main__':
    app.run(debug=True)
