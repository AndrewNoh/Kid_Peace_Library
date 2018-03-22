# -*- coding: utf-8 -*-

import os
import random
from flask import render_template, url_for, session, request, jsonify, current_app, make_response, redirect
from Server.app_blueprint import app
from Server.database import DB
from Server.databases.comments import Comments_DB
from Server.databases.Search_db import search_db
from Server.controller.pagination_class import Pagination
from collections import OrderedDict
import uuid, datetime


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@app.route('/Board/<category>/', defaults={'page':1})
@app.route('/Board/<category>/<int:page>')
def board_list(category, page):
    
    mydb = DB()
    total_cnt = mydb.get_board_cnt(category)
    per_page =10

    pagination = Pagination(page, per_page=per_page, total_count= total_cnt)

    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0

    rows = mydb.get_Page_list(per_page, offset, category)
    
    if session:
        return render_template("board.html", session = session, board_name= category, rows = rows,pagination=pagination)
    else:
        return render_template("board.html", board_name=category, rows = rows,pagination=pagination)

@app.route('/Search/get_keyword', methods=['POST'])
def search_get_keyword():
    if request.method=="POST":
        keyword = request.form['keyword']
        if (len(keyword)<=1) or  keyword.find(' ')!=-1:
            return render_template('alert_msg.html', msg="2글자이상, 공백없이 입력해주세요.")
        return redirect(url_for('.Search_Boards', keyword = keyword))

@app.route('/Search/<keyword>/', defaults={'page':1})
@app.route('/Search/<keyword>/<int:page>')
def Search_Boards(keyword, page):
    if request.method=="GET":
        db = DB()
        total_cnt = db.get_boardtotal_cnt()
        
        per_page = 10
        pagination = Pagination(page, per_page=per_page, total_count= total_cnt)
        
        if page != 1:
            offset = per_page * (page - 1)
        else:
            offset = 0
        
        del db
        mydb = search_db()
        result = mydb.get_search_list(keyword, per_page, offset)
        if not result:
            result = "not search"
        if session:
            return render_template("board.html", session = session, keyword=keyword, search_list = result, pagination=pagination)
        else:
            return render_template("board.html", keyword=keyword, search_list = result, pagination=pagination)

@app.route('/Board_View/<uuid>/', defaults={'page':1}, methods=['GET', 'POST'])
@app.route('/Board_View/<uuid>/<int:page>', methods=['GET', 'POST'])
def board_show(uuid, page):
    db = DB()
    rows = db.get_board(uuid)
    del db
    db = Comments_DB()
    total_cnt = db.get_comment_cnt(uuid)
        
    per_page =10
    pagination = Pagination(page, per_page=per_page, total_count= total_cnt)
        
    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
            
    comments = db.get_comments_list(per_page, offset, uuid)
    
    if request.method=="POST":
        hits = request.form['hits']
        db.hits_add(uuid, hits)
        rows['hits'] = hits
        del db
        
        if session:
            if session['id'] == rows['id']:
                return render_template("board_show.html",session = session, rows=rows, pagination=pagination, comments=comments, user_check=True)
    return render_template("board_show.html", rows=rows, pagination=pagination, comments=comments)
        
@app.route('/Board/delete', methods=['POST'])
def board_delete():
    uuid = request.form['uuid']
    db = DB()
    rows = db.get_board(uuid)
    data = OrderedDict()
    data['status'] = 'error'
    if session:
        if session['id'] == rows['id']:
            if db.delete_board(uuid):
                data['status'] = 'ok'
            else:
                data['status'] = 'fail'
    return jsonify(data)

@app.route('/Write')
@app.route('/Write/<category>')
def write_form(category):
    if session:
        if session['permission'] == "Admin" or session['permission'] == "Manager" :
            return render_template("write.html", session = session, board_name= category)
        elif session['permission'] == "user" :
            if category == "자유 게시판" :
                return render_template("write.html", session = session, board_name= category)
            else :
                return render_template("alert_msg.html", msg="권한이 없습니다.")
    return render_template("alert_msg.html", msg="로그인을 해주세요.")

@app.route('/Write/create/<category>', methods =['POST'])
def create(category):
    if request.method=="POST":
        if session:
            data = dict()
            if 'notice' in request.form.keys():
                data['notice'] = True
            else:
                data['notice'] = False
            data['id'] = session['id']
            data['title'] =  request.form['subject']
            data['contents'] = request.form['editor1']
            data['category'] = category
            data['hits'] = 0
            data['uuid'] = str(uuid.uuid4())
            
            mydb = DB()
            if mydb.create_board(data):
                del mydb
                return render_template('write_next_page.html', board_name=category, status="ok")
            else:
                del mydb
                return render_template('write_next_page.html', board_name=category, status="fail")
    return render_template('write_next_page.html', board_name=category, status="error")

@app.route('/Board/Modify_form/<uuid>')
def board_modify_form(uuid):
    db = DB()
    rows = db.get_board(uuid)
    if session:
        if session['id'] == rows['id']:
            return render_template('board_modify.html', session = session, data = rows)
    return render_template("alert_msg.html", msg="잘못된 접근 입니다.")

@app.route('/Board/Modify/', methods=['POST'])
def board_modify():
    send_data = OrderedDict()
    data = dict()
    if request.method=="POST":
        data['uuid'] = request.form['uuid']
        data['title'] = request.form['subject']
        data['contents'] = request.form['editor1']
        send_data['status'] = 'error'
        db = DB()
        rows = db.get_board(data['uuid'])
        if session:
            if session['id'] == rows['id']:
                if db.modify_board(data):
                        send_data['status'] = 'ok'
                else :
                    send_data['status'] = 'fail'
        else :
            send_data['status'] = 'permission error'
    return jsonify(send_data)

@app.route('/Board/comment/insert', methods=['POST'])
def insert_comment():
    if request.method=="POST":
        send_data = OrderedDict()
        recv_data = dict()
        recv_data['uuid'] = request.form['uuid']
        recv_data['id'] = request.form['id']
        recv_data['comment_contents'] = request.form['comment_contents']
        send_data['status'] = 'error'
        db = Comments_DB()
        if db.Insert_comment(recv_data):
            send_data['status'] = 'ok'
        else:
            send_data['status'] = 'fail'
        del db
    return jsonify(send_data)

@app.route('/Baord/comment/delete', methods=['POST'])
def delete_comment():
    if request.method=="POST":
        send_data = OrderedDict()
        recv_data = dict()
        recv_data['uuid'] = request.form['uuid']
        recv_data['write_time'] = request.form['write_time']
        recv_data['id'] = request.form['id']
        send_data['status'] = 'error'
        db = Comments_DB()
        if db.delete_comment(recv_data):
            send_data['status'] = 'ok'
        else:
            send_data['status'] = 'fail'
        del db
    return jsonify(send_data)

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
