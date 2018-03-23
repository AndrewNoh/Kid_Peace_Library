# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request
from Server.controller.pagination_class import Pagination
from Server.app_blueprint import app
from Server.database import DB
from Server.databases.manage import Manage_DB
from werkzeug import secure_filename
import os


@app.route('/manage')
def manage():
    return render_template('manage.html', session=session)

@app.route('/manage/user/', defaults={'page':1})
@app.route('/manage/user/<int:page>')
def manage_user(page):
    
    mydb = Manage_DB()
    total_cnt = mydb.get_user_cnt()
    per_page = 20
    
    pagination = Pagination(page, per_page=per_page, total_count= total_cnt)

    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
        
    rows = mydb.get_Page_list_user(per_page, offset)

    return render_template("manage_users.html", session = session, rows = rows, pagination=pagination)

@app.route('/manage/sponsor/', defaults={'page':1})
@app.route('/manage/sponsor/<int:page>')
def manage_sponsor(page):
    
    mydb = Manage_DB()
    total_cnt = mydb.get_user_cnt()
    per_page = 20
        
    pagination = Pagination(page, per_page=per_page, total_count= total_cnt)

    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
        
    rows = mydb.get_Page_list_sponsor(per_page, offset)

    return render_template("manage_sponsor.html", session = session, rows = rows, pagination=pagination)

@app.route('/manage/modifyU/<id>/<sponsor>/')
def modify_sponsor(id, sponsor):
    if session['permission'] == "Admin" :
        db = Manage_DB()
        if sponsor == '1' :
            rows = db.mt_sponsor(id)
        else :
            rows = db.mf_sponsor(id)
        del db
        return redirect(url_for('.manage_user'))
    else:
        return render_template('alert_msg.html', msg="잘못된 접근입니다.")
    
@app.route('/manage/modifyP/<id>/<permission>/')
def modify_permission(id, permission):
    if session['permission'] == "Admin" :
        db = Manage_DB()
        if permission == 'user' :
            rows = db.mu_permission(id)
        else :
            rows = db.mm_permission(id)
        del db
        return redirect(url_for('.manage_user'))
    else:
        return render_template('alert_msg.html', msg="잘못된 접근입니다.")
    
@app.route('/manage/<id>/<m_delete>/')
def del_user(id, m_delete):
    if session['permission'] == "Admin" :
        db = DB()
        mydb = Manage_DB()
        if m_delete == '0' :
            mydb.delete_user(id)
            db.user_delete_update_board(id)
            del mydb
            del db
            return redirect(url_for('.manage_user'))
        else :
            return render_template('alert_msg.html', msg="탈퇴된 회원입니다.")
    else:
        return render_template('alert_msg.html', msg="잘못된 접근입니다.")


@app.route('/manage/introduce/<uuid>/')
def introduce(uuid):
    db = Manage_DB()
    rows = db.introduce(uuid)
    del db
    return render_template('introduce.html', rows=rows, session = session)
    
    
