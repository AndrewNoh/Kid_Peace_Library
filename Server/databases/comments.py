# -*- coding: utf-8 -*-
'''
Created on 2018. 3. 13.

@author: jeongnam
'''

from Server.database import DB
from pymysql.err import MySQLError

class Comments_DB(DB):
    def __init__(self):
        super().__init__()
    def __del__(self):
        super().__del__()

    def Insert_comment(self, data):
        sql ="INSERT INTO COMMENTS VALUES( %s, %s, %s, NOW())"
        try:
            self.cur.execute(sql, (data['comment_contents'], data['uuid'], data['id']))
            self.conn.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return True
    
    def get_comment_cnt(self, uuid):
        sql = "SELECT count(*) cnt FROM COMMENTS WHERE uuid=%s"
        try:
            self.cur.execute(sql, (uuid))
            total_cnt = self.cur.fetchone()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return total_cnt['cnt']
    
    def get_comments_list(self, limit, offset, uuid):
        sql = "SELECT * FROM COMMENTS WHERE uuid=%s ORDER BY write_time DESC LIMIT %s OFFSET %s"
        try:
            self.cur.execute(sql, (uuid, limit, offset))
            rows = self.cur.fetchall()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        """for row in rows:
            row['id'] = 'None'"""
        return rows
    
    def delete_comment(self,data):
        sql =\
        "DELETE FROM COMMENTS WHERE write_time=%s AND uuid=%s AND id=%s"
        try:
            self.cur.execute(sql, (data['write_time'], data['uuid'], data['id']))
            self.conn.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return True
    