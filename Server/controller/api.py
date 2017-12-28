# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request, jsonify
from Server.app_blueprint import app
from Server.model.user import user
from Server.database import DB
from collections import OrderedDict
from Server.controller.login import login_requied

@app.route('/api/v1.0/login', methods=['POST'])
def api_login():
    id = request.json['id']
    password = request.json['password']
    
    data = OrderedDict()
    
    db = DB()
    flag = db.id_check(id)
    
    if flag == 0:
        data['status'] = 'id not found'
        return jsonify(data)
    
    user_buf = db.login(id, password)
    del db
    
    if user_buf:
        data['status'] = 'ok'
        data['id'] = user_buf.id
        data['permission'] = user_buf.permission
        
        return jsonify(data)
    else:
        data['status'] = 'password wrong'
        return jsonify(data)