# -*- coding: utf-8 -*-

import os
import datetime
import random
from flask import render_template, url_for, redirect, session, request, jsonify, current_app, make_response
from Server.app_blueprint import app
from Server.model.user import user
from Server.model.board import board
from Server.database import DB
from Server.controller.login import login_requied
from Server.controller.pagination_class import Pagination
from collections import OrderedDict
import uuid, datetime


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@app.route('/Board/<category>/', defaults={'page':1})
@app.route('/Board/<category>/<int:page>')
def board_list(category, page):
    get_user = login_requied()
    
    mydb = DB()
    total_cnt = mydb.get_board_cnt(category)
    per_page =10
        
    pagination = Pagination(page, per_page=per_page, total_count= total_cnt)

    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
        
    rows = mydb.get_Page_list(per_page, offset, category)
    
    if get_user:
        return render_template("board.html", name = get_user.name, permission = get_user.permission, board_name= category, rows = rows,pagination=pagination)
    else:
        return render_template("board.html", board_name=category, rows = rows,pagination=pagination)
    
@app.route('/Board/show/<uuid>/<hits>')
def board_show(uuid, hits):
    get_user = login_requied()
    db = DB()
    rows = db.get_board(uuid)
    db.hits_add(uuid, hits)
    rows['hits'] = hits
    del db
    if get_user:
        if get_user.id == rows['id']:
            return render_template("board_show.html", name = get_user.name, permission = get_user.permission, rows=rows, user_check=True)
        
        return render_template("board_show.html", rows=rows)
    return render_template("board_show.html", rows=rows)

@app.route('/Write')
@app.route('/Write/<category>')
def write_form(category):
    get_user = login_requied()
    if get_user:
        if session['permission'] == "admin" or session['permission'] == "manager" :
            return render_template("write.html", name = get_user.name, permission = get_user.permission, board_name= category)
        elif session['permission'] == "user" :
            if category == "자유 게시판" :
                return render_template("write.html", name = get_user.name, permission = get_user.permission, board_name= category)
            else :
                return render_template("alert_msg.html", msg="권한이 없습니다.")
    return render_template("alert_msg.html", msg="로그인을 해주세요.")

@app.route('/Write/create/<category>', methods =['POST'])
def create(category):
    if request.method=="POST":
        get_user = login_requied()
        if get_user:  
            id = get_user.id
            title =  request.form['subject']
            contents = request.form['editor1']
                
            item = board(\
                        uuid = str(uuid.uuid4()),
                        title = title,
                        category = category,
                        contents = contents,
                        hits = 0,
                        id = id)
            mydb = DB()
            if mydb.create_board(item):
                del mydb
                return render_template('write_next_page.html', board_name=category, status="ok")
            else:
                del mydb
                return render_template('write_next_page.html', board_name=category, status="fail")
        return render_template('write_next_page.html', board_name=category, status="denied")
    else:
        return render_template('write_next_page.html', board_name=category, status="error")
        
        
@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """<script type="text/javascript"> 
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
             </script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
