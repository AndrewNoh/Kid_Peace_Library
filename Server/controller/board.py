# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request, jsonify
from Server.app_blueprint import app
from Server.model.user import user
from Server.database import DB
from Server.controller.login import login_requied
from collections import OrderedDict


@app.route('/Board')
def board_form():
    get_user = login_requied()
    if get_user:
        return render_template("board.html", name = get_user.name, permission = get_user.permission)
    return render_template("board.html")

@app.route('/Board/<category>/', defaults={'page':1})
@app.route('/Board/<category>/<int:page>')
def board_list(category, page):
    get_user = login_requied()
    if get_user:
        return render_template("board.html", name = get_user.name, permission = get_user.permission, board_name= category)
    else:
        return render_template("board.html", board_name= category)

@app.route('/Write/<category>/')
def write_form(category):
    get_user = login_requied()
    if get_user:
        if session['permission'] == "admin" or session['permission'] == "manager" :
            return render_template("write.html", name = get_user.name, permission = get_user.permission, board_name= category)
        elif session['permission'] == "user" :
            if category == "회원 게시판" or category == "자유 게시판" :
                return render_template("write.html", name = get_user.name, permission = get_user.permission, board_name= category)
            else :
                return render_template("alert_msg.html", msg="권한이 없습니다.")
    elif category == "자유 게시판":
        return render_template("write.html", board_name=category)
    return render_template("alert_msg.html", msg="로그인을 해주세요.")


