# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_jsglue import JSGlue
"""
    Server 패키지 초기화 모듈
"""

def create_app():
    jsglue = JSGlue()
    application = Flask(__name__);
    
    jsglue.init_app(application)
    # 비밀키 등록
    application.secret_key = 'any random string'

    # 블루프린트 등록전 뷰 함수 모듈 임포트
    from Server.controller import login
    from Server.controller import register_user
    from Server.controller import board
    from Server.controller import api
    # 블루프린트 등록
    from Server.app_blueprint import app
    application.register_blueprint(app)

    return application;
