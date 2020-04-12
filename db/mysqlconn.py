import pymysql
from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DB, KEYWORD
from pypinyin import lazy_pinyin


class MysqlConn(object):
    def __init__(self):
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.port = MYSQL_PORT
        self.db = MYSQL_DB
        self.table = ''.join(lazy_pinyin(KEYWORD))
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.db,
                # charset='utf8'
            )
        except pymysql.MySQLError as e:
            print(e.args)
        else:
            print('链接成功！')
            self.cursor = self.conn.cursor()

    def add_table(self):
        sql = """CREATE TABLE IF NOT EXISTS %s(
        id INT(20) NOT NULL PRIMARY KEY,
        city_name VARCHAR(20),
        address VARCHAR(255),
        title VARCHAR(255),
        backCateName VARCHAR(255),
        areaname VARCHAR(255),
        avgprice INT(10),
        avgscore DECIMAL(2,1),
        comments VARCHAR(255),
        phone VARCHAR(255),
        imageUrl VARCHAR(255));
        """ % self.table
        self.cursor.execute(sql)

    def insert(self, data):
        keys = ', '.join(data.keys())
        val_num = ', '.join(['%s'] * len(data.values()))
        sql = """
        INSERT INTO %s(
        %s
        ) VALUES(%s)
        ON DUPLICATE KEY UPDATE id = values(id);
        
        """ % (self.table, keys, val_num)
        try:
            self.cursor.execute(sql, tuple(data.values()))
        except pymysql.MySQLError as e:
            print(e.args)
            self.conn.rollback()
            print("插入失败")
        else:
            print('插入成功')
            self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    mysql = MysqlConn()
    data = {
            'id': 1223232222,
            'title': 'hehe',
            'city_name': 'qweqwe',
            'address': 'qeqw',
            'backCateName': 'backCateName',
            'areaname': 'areaname',
            'avgprice': 66,
            'avgscore': 8.7,
            'phone': 'phone',
            'imageUrl': 'imageUrl',
            'comments': 123,
    }
    mysql.insert(data)

