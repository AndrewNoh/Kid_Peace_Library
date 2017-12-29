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


@app.route('/Write')
def write_form():
    get_user = login_requied()
    if get_user:
        return render_template("write.html", name = get_user.name, permission = get_user.permission)
    return render_template("write.html")

@app.route('/Board/Category', methods=['POST'])
def category():
    if request.method == 'POST':
        cat = request.form[cat]
        mydb=DB()
        categorys = mydb.view_board(cat)
        if categorys == "소식마당":

        return
    return
