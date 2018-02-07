# -*- coding: utf-8 -*-

import pymysql.cursors
from pymysql.err import MySQLError
import sys
from Server.model.user import user
from Server.model.board import board

class DB():
    def __init__(self):
        try:
            self.conn = pymysql.connect("localhost","Admin", "kosta6006", "Kid_Peace_Library_db", charset="utf8")
            #db.row_factory = dict_factory
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        except:
            print("database connect fail")
            sys.exit()

    def __del__(self):
        self.conn.close()
        self.cur.close()

    def id_check(self, id):
        sql = "select count(*) from MEMBERS where id='"+id+"'"
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
        except:
            print("Select id execute error!")
            return "error"
        if rows:
            return rows[0]['count(*)']
        return

    def login(self, id, password):
        sql = "select * from MEMBERS where id='"+id+"' AND password=password('"+password+"')"
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
        except:
            print("login execute error!")
            return None

        if rows:
            data = rows[0]
            buf = user(\
                       id = data['id'],
                       permission = data['permission'],
                       cell_phone = data['cell_phone'],
                       email = data['email'],
                       name = data['name'],
                       sponsor_status = data['sponsor_status'],
                       m_delete = data['m_delete'])
            return buf
        else:
            return None

    def user_info(self, id):
        sql = "select * from MEMBERS where id='"+id+"'"
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
        except:
            print("login execute error!")
            return

        if rows:
            data = rows[0]
            buf = user(\
                       id = data['id'],
                       permission = data['permission'],
                       cell_phone = data['cell_phone'],
                       email = data['email'],
                       name = data['name'],
                       sponsor_status = data['sponsor_status'],
                       m_delete = data['m_delete'])
            return buf
        else:
            return

    def sign_up(self, user):
        sql = \
        "insert into MEMBERS values('"\
        +user.id+"', "\
        +"password('"+user.password+"'), '"\
        +user.permission+"','"\
        +user.cell_phone+"','"\
        +user.email+"','"\
        +user.name+"', 0, 0)"


        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print('sign_up execute error!')
            return False
        return True


    def modify_nopassword(self, user):
        sql = \
            "update MEMBERS set cell_phone = '"\
            +user.cell_phone+"', email = '"+user.email+"',"\
            "name = '"+user.name+"' where id= '"+user.id+"'"

        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print('modify execute error!')
            return False
        return True

    def modify(self, user):
        sql =  "update MEMBERS set password=password(%s) , cell_phone=%s, email=%s, name=%s, sponsor_status=%s, m_delete=%s where id=%s"

        try:
            self.cur.execute(sql, (user.password, user.cell_phone, user.email, user.name, int(user.sponsor_status), int(user.m_delete), user.id))
            self.conn.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return True
        
    def create_board(self, board):
        sql =\
        "INSERT INTO BOARD VALUES( %s, %s, %s, 0, NOW(), NOW(), %s, %s, %s)"
        try:
            self.cur.execute(sql, (board.uuid, board.title, board.contents, board.category, board.id, board.user_delete))
            self.conn.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        
        return True

    def user_delete_update_board(self, id):
        sql =\
        "update BOARD set user_delete=%s where id=%s"
        try:
            self.cur.execute(sql, (1, id))
            self.conn.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return True
    
    def get_board_cnt(self, category):
        sql = "SELECT count(*) cnt FROM BOARD where category=%s"
        try:
            self.cur.execute(sql, (category))
            total_cnt = self.cur.fetchone()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return total_cnt['cnt']
    
    def get_Page_list(self, limit, offset, category):
        sql = "SELECT * FROM BOARD where category=%s ORDER BY write_time DESC LIMIT %s OFFSET %s"
        try:
            self.cur.execute(sql, (category, limit, offset))
            rows = self.cur.fetchall()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        """for row in rows:
            row['id'] = 'None'"""
        return rows

    def get_board(self, uuid):
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
    
    def hits_add(self, uuid, hits):
        sql = "UPDATE BOARD SET hits=%s WHERE uuid=%s"
        try:
            self.cur.execute(sql, (hits, uuid))
            self.conn.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return True
    
if __name__ == '__main__':
    mydb = DB()
    rows = mydb.get_Page_list(10, 0, '자유 게시판')
    print(rows)
    cnt = mydb.get_board_cnt( '자유 게시판');
    print(cnt)
    data = mydb.get_board('03b093b5-839f-4d5d-acd7-9018435286ac')
    print(data.contents)
    del mydb
    for index, row in enumerate(rows):
        print(index)
