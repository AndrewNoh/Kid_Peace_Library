# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, session, request
from Server.app_blueprint import app
from Server.model.user import user
from Server.database import DB


@app.route('/manage')
def manage():
    return render_template('manage.html', session=session)

@app.route('/manage/user')
def user_manage():
    return render_template('user_manage.html', session=session)