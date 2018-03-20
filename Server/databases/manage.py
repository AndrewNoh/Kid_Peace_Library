'''
Created on 2018. 3. 20.

@author: andrew
'''

from Server.database import DB
from pymysql.err import MySQLError


class Manage_DB(DB):
    def __init__(self):
        super().__init__()
    def __del__(self):
        super().__del__()

    def get_Page_list_user(self, limit, offset):
        sql = "SELECT * FROM MEMBERS WHERE ID != 'Admin' ORDER BY ID DESC LIMIT %s OFFSET %s"
        try:
            self.cur.execute(sql, (limit, offset))
            rows = self.cur.fetchall()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        """for row in rows:
            row['id'] = 'None'"""
        return rows
    
    def get_Page_list_sponsor(self, limit, offset):
        sql = "SELECT * FROM MEMBERS WHERE ID != 'Admin' AND SPONSOR_STATUS = '1' ORDER BY ID DESC LIMIT %s OFFSET %s"
        try:
            self.cur.execute(sql, (limit, offset))
            rows = self.cur.fetchall()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        """for row in rows:
            row['id'] = 'None'"""
        return rows
    
    def mt_sponsor(self, id):
            sql ="UPDATE MEMBERS SET sponsor_status=0 WHERE id=%s"
            try:
                self.cur.execute(sql, (id))
                self.conn.commit()
            except MySQLError as e:
                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                return False
            return True
        
    def mf_sponsor(self, id):
            sql ="UPDATE MEMBERS SET sponsor_status=1 WHERE id=%s"
            try:
                self.cur.execute(sql, (id))
                self.conn.commit()
            except MySQLError as e:
                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                return False
            return True
    
    def mu_permission(self, id):
            sql ="UPDATE MEMBERS SET permission='Manage' WHERE id=%s"
            try:
                self.cur.execute(sql, (id))
                self.conn.commit()
            except MySQLError as e:
                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                return False
            return True
            
    def mm_permission(self, id):
            sql ="UPDATE MEMBERS SET sponsor_status='user' WHERE id=%s"
            try:
                self.cur.execute(sql, (id))
                self.conn.commit()
            except MySQLError as e:
                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                return False
            return True

    def introduce(self, uuid):
        sql = "SELECT * FROM BOARD WHERE uuid=%s"
        try:
            self.cur.execute(sql, (uuid))
            rows = self.cur.fetchone()
            if rows:
                return rows
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return None


    