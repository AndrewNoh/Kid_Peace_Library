class board() :
    def __init__(self, uuid, title, contents, hits, write_time, modify_time, category, id):
    	self.uuid = uuid
    	self.title = title
    	self.contents = contents
    	self.hits = hits
    	self.write_time = write_time
    	self.modify_time = modify_time
    	self.category = category
    	self.id = id


class categorys() :
    def __init__(self, category):
        self.category = category


class comments() :
    def __init__(self, comments, uuid, id):
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
