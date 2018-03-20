# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request
from Server.controller.pagination_class import Pagination
from Server.app_blueprint import app
from Server.database import DB


@app.route('/manage')
def manage():
    return render_template('manage.html', session=session)

@app.route('/manage/user/', defaults={'page':1})
@app.route('/manage/user/<int:page>')
def manage_user(page):
    
    mydb = DB()
    total_cnt = mydb.get_user_cnt()
    per_page = 20
        
    pagination = Pagination(page, per_page=per_page, total_count= total_cnt)

    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
        
    rows = mydb.get_Page_list2(per_page, offset)

    return render_template("manage_users.html", session = session, rows = rows, pagination=pagination)

@app.route('/manage/modify/<id>/<sponsor>/')
def modify_sponsor(id, sponsor):
    if session['permission'] == "Admin" :
        db = DB()
        if sponsor == '1' :
            rows = db.mt_sponsor(id)
        else :
            rows = db.mf_sponsor(id)
        del db
        return redirect(url_for('.manage_user'))
    else:
        return render_template('alert_msg.html', msg="잘못된 접근입니다.")
    
@app.route('/manage/modify/<id>/<permission>/')
def modify_permission(id, permission):
    if session['permission'] == "Admin" :
        db = DB()
        if permission == 'user' :
            rows = db.mu_sponsor(id)
        else :
            rows = db.mm_sponsor(id)
        del db
        return redirect(url_for('.manage_user'))
    else:
        return render_template('alert_msg.html', msg="잘못된 접근입니다.")

