from Server.database import DB
from pymysql.err import MySQLError


class file_db(DB):
    def __init__(self):
        super().__init__()
    def __del__(self):
        super().__del__()
        
    def file_upload(self, data):
        sql =\
        "INSERT INTO FILES VALUES( %s, %s, %s, %s, %s, %s)"
        try:
            self.cur.execute(sql, (data['file_name'], data['origin_name'], data['path'], data['size'], data['format'], data['uuid']))
            self.conn.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        
        return True