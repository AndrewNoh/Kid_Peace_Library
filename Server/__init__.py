# -*- coding: utf-8 -*-

from flask import Flask, render_template
"""
    Server 패키지 초기화 모듈
"""

def create_app():
    application = Flask(__name__);
    
    # 비밀키 등록
    application.secret_key = 'any random string'
    
    # 블루프린트 등록전 뷰 함수 모듈 임포트
    from Server.controller import login
    from Server.controller import register_user
    
    # 블루프린트 등록
    from Server.app_blueprint import app
    application.register_blueprint(app)
    
    return application;