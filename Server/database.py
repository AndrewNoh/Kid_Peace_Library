# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import sys
from Server.model.user import user


class DB():
    def __init__(self):
        try:
            self.conn = MySQLdb.connect("localhost","Admin", "kosta6006", "Kid_Peace_Library_db", charset="utf8")
            #db.row_factory = dict_factory
            self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("database connect fail")
            sys.exit()

    def __del__(self):
        self.conn.close()
        self.cur.close()

    def login(self, id, password):
        sql = "select * from MEMBERS where id='"+id+"' AND password=password('"+password+"')"
        try:
            self.cur.execute(sql)
            rows = self.cur.fetchall()
        except:
            print("login execute error!")
            return

        for data in rows:
            buf = user(\
                       id = data['id'],
                       password = data['password'],
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
        +user.permission+"',"\
        +user.cell_phone+",'"\
        +user.email+"','"\
        +user.name+"', 0, 0)"


        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print('sign_up execute error!')
            return False
        return True

if __name__ == '__main__':
    mydb = DB()
    data = mydb.select_Member('kim910712', 'kim15885')

    print(data.email)
