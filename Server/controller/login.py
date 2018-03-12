# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request
from Server.app_blueprint import app
from Server.model.user import user
from Server.database import DB

def session_refresh(id):
    mydb = DB()
    user_buffer = mydb.user_info(id)
    del mydb
    
    session.clear()
    
    if user_buffer:
        session['id'] = user_buffer.id
        session['password'] = user_buffer.password
        session['permission'] = user_buffer.permission
        session['cell_phone'] = user_buffer.cell_phone
        session['email'] = user_buffer.email
        session['name'] = user_buffer.name
        session['sponsor_status'] = user_buffer.sponsor_status
        session['m_delete'] = user_buffer.m_delete
        return True
    return False


@app.route('/')
def index():
    if session:
        return render_template("index.html", session=session)
    return render_template("index.html")

@app.route('/Login_from')
def login_from():
    if session:
        session.clear()
    return render_template('Login.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        mydb = DB()
        user_buffer = mydb.user_info(id)
        del mydb
        
        session.clear()
        
        if user_buffer:
            session['id'] = user_buffer.id
            session['permission'] = user_buffer.permission
            session['cell_phone'] = user_buffer.cell_phone
            session['email'] = user_buffer.email
            session['name'] = user_buffer.name
            session['sponsor_status'] = user_buffer.sponsor_status
            session['m_delete'] = user_buffer.m_delete
            
            if user_buffer.m_delete:
                return render_template('alert_msg.html', msg="탈퇴한 회원입니다.")
            return redirect(url_for('app.index'))
        else:
            return render_template('alert_msg.html', msg="Login Fail! 등록되지 않았거나 아이디 혹은 비밀번호가 다릅니다.")
    else:
        return render_template('alert_msg.html', msg="POST Error!")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.index'))


@app.route('/manage')
def manage():
    return render_template('manage.html', session=session)

@app.route('/backgroundimg1')
def backgroundimg1():
    return redirect(url_for('static', filename='img/Main_img1.jpg'))

@app.route('/backgroundimg2')
def backgroundimg2():
    return redirect(url_for('static', filename='img/Main_img2.png'))

@app.route('/backgroundimg3')
def backgroundimg3():
    return redirect(url_for('static', filename='img/Main_img3.jpg'))
