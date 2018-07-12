# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, url_for
#from flask_jsglue import JSGlue
"""
    Server 패키지 초기화 모듈
"""

# pagenation 할때 html에서 쓰일 글로벌 함수
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def create_app():
    #jsglue = JSGlue()
    application = Flask(__name__)
    
    #jsglue.init_app(application)
    # 비밀키 등록
    application.secret_key = 'any random string'

    # 블루프린트 등록전 뷰 함수 모듈 임포트
    from Server.controller import login
    from Server.controller import register_user
    from Server.controller import board
    from Server.controller import api
    from Server.controller import manage
    from Server.controller import file_controller
    # 블루프린트 등록
    from Server.app_blueprint import app
    application.register_blueprint(app)
    application.jinja_env.globals['url_for_other_page'] = url_for_other_page
    
    return application;
