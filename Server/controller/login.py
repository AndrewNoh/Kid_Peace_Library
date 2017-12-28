# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request
from Server.app_blueprint import app
from Server.model.user import user
from Server.database import DB


def login_requied():
    if 'id' in session:
        USER = user(\
                    id = session['id'],
                    permission = session['permission'],
                    cell_phone = session['cell_phone'],
                    email = session['email'],
                    name = session['name'],
                    password = session['password'],
                    sponsor_status=session['sponsor_status'],
                    m_delete=session['m_delete'])
        return USER

@app.route('/')
def index():
    get_user = login_requied()
    if get_user:
        return render_template("index.html", name = get_user.name, permission = get_user.permission)
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        mydb = DB()
        user_buffer = mydb.login(id, password)
        del mydb

        if user_buffer:
            session['id'] = user_buffer.id
            session['password'] = user_buffer.password
            session['permission'] = user_buffer.permission
            session['cell_phone'] = user_buffer.cell_phone
            session['email'] = user_buffer.email
            session['name'] = user_buffer.name
            session['sponsor_status'] = user_buffer.sponsor_status
            session['m_delete'] = user_buffer.m_delete
            return redirect(url_for('app.index'))
        else:
            return render_template('alert_msg.html', msg="Login Fail! 등록되지 않았거나 아이디 혹은 비밀번호가 다릅니다.")
    else:
        return render_template('alert_msg.html', msg="POST Error!")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.index'))


@app.route('/userinf')
def userinf_form():
    return render_template('userinf.html')

@app.route('/backgroundimg1')
def backgroundimg1():
    return redirect(url_for('static', filename='img/Main_img1.jpg'))

@app.route('/backgroundimg2')
def backgroundimg2():
    return redirect(url_for('static', filename='img/Main_img2.png'))

@app.route('/backgroundimg3')
def backgroundimg3():
    return redirect(url_for('static', filename='img/Main_img3.jpg'))
