from flask import Flask
from flask.templating import render_template

app = Flask(__name__)


@app.route('/base')
def base_index():
    return render_template('base.html')

@app.route('/')
def index():
    return "hello world!!"

if __name__ == '__main__':
    app.run(debug=False)
