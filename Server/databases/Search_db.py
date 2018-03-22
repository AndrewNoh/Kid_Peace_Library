from Server.database import DB
from pymysql.err import MySQLError

class search_db(DB):
    def __init__(self):
        super().__init__()
    def __del__(self):
        super().__del__()
        
    def get_search_list(self, data, LIMIT, OFFSET):
        sql_data = "%"+data+"%"
        sql = "SELECT * FROM BOARD WHERE title LIKE %s OR contents LIKE %s OR id LIKE %s ORDER BY write_time DESC LIMIT %s OFFSET %s"
        try:
            self.cur.execute(sql, (sql_data, sql_data, sql_data, LIMIT, OFFSET))
            rows = self.cur.fetchall()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return None
        return rows
    

if __name__=="__main__":
    db = search_db();
    rows = db.get_search_list('kim', 10, 0)
    print(rows)
    