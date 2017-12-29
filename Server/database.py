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
            return

        if rows:
            data = rows[0]
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
        sql = \
            "update MEMBERS set password= password('"+user.password+"') , "\
            "cell_phone='"+user.cell_phone+"', email='"+user.email+"', "\
            "name='"+user.name+"' where id='"+user.id+"'"
    
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print('modify execute error!')
            return False
        return True
    
    def select_category(self, category):
        sql = "select CATEGORYS from '+category+'"
        try:
            self.cur.excute(sql)
            rows = self.cur.fetchall()
        except:
            print("잘못된 접근입니다.")
            return
        if rows:
            data = rows[0]
            category = data['category']
            return category
        else :
            return

if __name__ == '__main__':
    mydb = DB()
    data = mydb.select_Member('kim910712', 'kim15885')
    del mydb
    print(data.email)
