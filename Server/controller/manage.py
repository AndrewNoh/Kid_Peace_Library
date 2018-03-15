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
    per_page =10
        
    pagination = Pagination(page, per_page=per_page, total_count= total_cnt)

    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
        
    rows = mydb.get_Page_list2(per_page, offset)

    return render_template("manage_users.html", session = session, rows = rows, pagination=pagination)
