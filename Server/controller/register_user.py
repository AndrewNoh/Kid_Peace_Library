# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request, jsonify
from Server.app_blueprint import app
from Server.model.user import user
from Server.database import DB
from collections import OrderedDict
from Server.controller.login import login_requied
from Server.controller.login import session_refresh

@app.route('/user/check_id')
def Check_id():
    id = request.args.get('id', 0)
    if id == "error" or\
    id == "Error" or \
    id == "Admin" or \
    id == "admin" or \
    id == "Menager" or\
    id == "menager" :
        return render_template('alert_msg.html', msg="사용할수 없는 id 입니다.")
    mydb = DB()
    count = int(mydb.id_check(id))

    data = OrderedDict()
    data['count'] = count
    return jsonify(data)


@app.route('/user/Signup', methods=['post'])
def signup_form():
    if request.method == 'POST':

        id = request.form['id']
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        cell_phone = request.form['cell_phone']
        
        item = user(\
                    id = id,
                    permission = 'user',
                    cell_phone = cell_phone,
                    email = email,
                    name = name,
                    password=password)

        mydb = DB()
        data = OrderedDict()
        data['status'] = 'ok' 
        if not mydb.sign_up(item):
            del mydb
            data['status'] = 'error'
            return jsonify(data)
        del mydb
    if 'id' in session:
        session.clear()
    return jsonify(data)



@app.route('/user/modify_form')
def modify_form():
    get_user = login_requied()
    if get_user:
        id = get_user.id
        email = get_user.email
        password = ''
        name = get_user.name
        cell_phone = get_user.cell_phone
        
        return render_template('modify.html', name = name, password = password, cell_phone = cell_phone, id = id, email = email, permission = get_user.permission)
    else:
        return render_template('alert_msg.html', msg="로그인후 이용할 수 있습니다.")
    
@app.route('/user/modify/password/check', methods=['POST'])
def modify_password_check():
    if request.method == 'POST':
        id = session['id']
        password = request.form['password']
        
        #보낼 json데이터
        data = OrderedDict()
        
        db = DB()
        user_buf = db.login(id, password)
        del db
        if user_buf != None:
            data['status'] = 'ok'
            return jsonify(data)
        else:
            data['status'] = 'fail'
            return jsonify(data)
    data['status'] = 'error'
    return jsonify(data)

@app.route('/user/modify', methods=['post'])
def modify():
    if request.method == 'POST':
        id = session['id']
        newpassword = request.form['new_password']
        email = request.form['email']
        name = request.form['name']
        cell_phone = request.form['cell_phone']
        
        buf = user(\
                   id=id, \
                   permission= session['permission'],\
                   password=newpassword,\
                   email=email,\
                   name=name,\
                   cell_phone=cell_phone)
        
        data = OrderedDict()
        
        db = DB()
        if newpassword == '':
            if db.modify_nopassword(buf):
                session_refresh(buf.id)
                data['status'] = 'ok'
            else:
                data['status'] = 'fail'
        else:
            if db.modify(buf):
                session_refresh(buf.id)
                data['status'] = 'ok'
            else:
                data['status'] = 'fail'
        del db
        return jsonify(data)
    data['status'] = 'error'
    return jsonify(data)

@app.route('/user/Withdrawal', methods=['POST'])
def withdrawal():
    if request.method == 'POST':
        get_user = login_requied()
        if get_user:
            password = request.form['password']
            data = OrderedDict()
            
            db = DB()
            user_buf = db.login(get_user.id, password)
            if user_buf==None:
                data['status'] = 'password_discordance'
                return jsonify(data) 
            
            buf = user(\
                   id=user_buf.id, \
                   permission= session['permission'],\
                   password='',\
                   email='',\
                   name='',\
                   cell_phone='',\
                   m_delete=1)
            if db.modify(buf):
                if db.user_delete_update_board(buf.id):
                    del db
                    session_refresh(buf.id)
                    data['status'] = 'ok'
                    return jsonify(data)
            del db 
    data['status'] = 'error'
    return jsonify(data) 
