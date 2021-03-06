# -*- coding: utf-8 -*-

import os
import random
from flask import url_for, request, current_app, make_response, send_from_directory, render_template, session, jsonify
from Server.app_blueprint import app
from Server.databases.files_db import files_db
from werkzeug import secure_filename
import uuid, datetime

IMAGE_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
FILES_ALLOWED_EXTENSIONS = set(['php', 'jsp', 'asp', 'PHP', 'JSP', 'ASP'])


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

def allowed_imagefile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in IMAGE_ALLOWED_EXTENSIONS

def get_file_Extension(f_name):
    filename , extension = f_name.rsplit('.', 1)
    return filename , extension

def allowed_file(filename):
    if '.' in filename and\
        get_file_Extension(filename)[1] in FILES_ALLOWED_EXTENSIONS :
        return False
    else :
        return True
    

def files_delete(rows):
    for row in rows:
        file_delete(row['path'])

def file_delete(path):
    error = None
    try:
        os.remove(path)
    except:
        error = "remove error"
    return error

def file_db(uuid, f_name, o_name, size, format, filepath):
        data = dict()
        data['file_name'] = f_name
        data['origin_name'] = o_name
        data['path'] =  filepath
        data['size'] = size
        data['format'] = format
        data['uuid'] = uuid
            
        mydb = files_db()
        if mydb.file_upload(data):
            del mydb
            return True
        else:
            del mydb
            return False
        

@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = None
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        if fileobj and allowed_imagefile(fileobj.filename):
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
                error = 'ERROR_DIR_NOT_WRITEABLE(permission denied)'
            if not error:
                error = ""
                fileobj.save(filepath)
                url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
        else:
            error = '이미지가 아닙니다.'
    else:
        error = 'post error'
    res = """<script type="text/javascript"> 
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
             </script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response

def f_upload(uid, files_obj):
    error = None
    fileobj_o = files_obj
    for fileobj in fileobj_o :
        if fileobj and allowed_file(fileobj.filename):
            try:
                pos = fileobj.tell()
                fileobj.seek(0, 2)  #seek to end
                size = fileobj.tell()
                fileobj.seek(pos) 
            except:
                pass
            limit_size = 50*1024*1024
            if size >= limit_size :
                error = "파일크기가 너무 큽니다 #max size = 50MB"
            f_name = secure_filename(str(uuid.uuid4()) + fileobj.filename)
            o_name = fileobj.filename
            filepath = os.path.join(current_app.static_folder, 'repository', f_name)
            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)    
                except:
                    error = 'ERROR_CREATE_DIR'
            elif not os.access(dirname, os.W_OK):
                error = 'ERROR_DIR_NOT_WRITEABLE(permission denied)'
            if not error:
                if file_db( uuid=uid, f_name=f_name, o_name=o_name, size=size, format=get_file_Extension(f_name)[1], filepath=filepath):
                    fileobj.save(filepath)
                else:
                    error = 'file upload DB save Error'
        else:
            error = "File formatter ERROR ('jsp, asp, php')"
    return error


@app.route('/download/<filename>')
def download_file(filename):
    repopath = os.path.join(current_app.static_folder, 'repository')
    filepath = os.path.join(current_app.static_folder, 'repository', filename)
    if not os.path.exists(filepath):
        return render_template('alert_msg.html', msg="파일을 찾을 수 없습니다.")
    return send_from_directory(repopath, filename,as_attachment=True)

@app.route('/File/Delete', methods=['GET','POST'])
def board_file_delete():
    push_data = dict()
    push_data['status'] = 'error'
    if request.method == 'POST' :
        filename = request.form['filename']
        path = request.form['path']
        db = files_db()
        if db.del_file(filename):
            file_delete(path)
            push_data['status'] = 'ok'
        else:
            push_data['msg'] = "db Error"
    return jsonify(push_data)

