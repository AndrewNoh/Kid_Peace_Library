# -*- coding: utf-8 -*-


class board() :
    def __init__(self, uuid, title, contents, hits , category, id, write_time=None, modify_time= None, user_delete=0):
        self.uuid = uuid
        self.title = title
        self.contents = contents
        self.hits = hits
        self.write_time = write_time
        self.modify_time = modify_time
        self.category = category
        self.id = id
        self.user_delete = user_delete


class categorys() :
    def __init__(self, category):
        self.category = category


class comments() :
    def __init__(self, comment_contents, uuid, id):
        self.comment_contents = comment_contents
        self.uuid = uuid
        self.id = id


class files() :
    def __init__(self, file_name, path, size, format, uuid):
        self.file_name = file_name
        self.path = path
        self.size = size
        self.format = format
        self.uuid = uuid
