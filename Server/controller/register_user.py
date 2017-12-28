# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request, jsonify
from Server.app_blueprint import app
from Server.model.user import user
from Server.database import DB
from collections import OrderedDict
from Server.controller.login import login_requied

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



@app.route('/user/modify')
def modify():
    get_user = login_requied
    if request.method == 'POST':
        id = get_user.id
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        cell_phone = request.form['cell_phone']
        new_passoword = request.form['new_password']
        if password == '':
            return render_template('alert_msg.html', msg="회원가입 실패! 비밀번호는 8자리 이상 문자, 숫자, 특수문자로 구성하여야 합니다.")
        elif password == get_user.password :
            item = user(\
                        id = id,
                        permission = 'user',
                        cell_phone = cell_phone,
                        email = email,
                        name = name,
                        password = new_passoword)
            mydb = DB()
            if not mydb.modify(item):
                del mydb
                return render_template('alert_msg.html', msg="회원정보 수정 실패")
            del mydb
        return redirect(url_for('.index'))

    return render_template('modify.html', name정 = get_user.name, password = get_user.password, cell_phone = get_user.cell_phone, id = get_user.id, email = get_user.email)
