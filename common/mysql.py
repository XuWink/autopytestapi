import pymysql
from common.logger import logger
from config.setting import MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT
from pymysql.cursors import DictCursor
from contextlib import contextmanager


class MysqlDb:
    def __init__(self, host, port, user, password, db, charset='utf8mb4', autocommit=True):
        # 数据库连接配置
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'db': db,
            'charset': charset,
            'autocommit': autocommit,
            'cursorclass': DictCursor
        }
        self._conn = None
        self._cursor = None

    @property
    def connection(self):
        """获取数据库连接，如果连接断开则重新连接"""
        if not self._conn or self._conn.open == 0:
            self._conn = pymysql.connect(**self.config)
        return self._conn

    @property
    def cursor(self):
        """获取数据库游标"""
        if not self._cursor or self._cursor.connection is None:
            self._cursor = self.connection.cursor()
        return self._cursor

    def __del__(self):
        """对象销毁时关闭游标和连接"""
        self.close()

    def close(self):
        """关闭游标和连接"""
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            self._conn.close()
            self._conn = None

    def select(self, sql, params=None):
        """执行查询语句，返回多行结果"""
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"查询失败: {e}, SQL: {sql}, 参数: {params}")
            raise

    def select_one(self, sql, params=None):
        """执行查询语句，返回单行结果"""
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"查询失败: {e}, SQL: {sql}, 参数: {params}")
            raise

    def execute(self, sql, params=None):
        """执行单条SQL语句"""
        try:
            self.cursor.execute(sql, params)
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"执行SQL失败: {e}, SQL: {sql}, 参数: {params}")
            self.connection.rollback()
            raise

    def execute_many(self, sql, params_list):
        """批量执行SQL语句"""
        try:
            self.cursor.executemany(sql, params_list)
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"批量执行SQL失败: {e}, SQL: {sql}, 参数列表: {params_list}")
            self.connection.rollback()
            raise

    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        try:
            self.connection.begin()
            yield
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"事务执行失败: {e}")
            raise


# 创建数据库连接实例
db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


if __name__ == '__main__':
    # 查询示例
    users = db.select("SELECT * FROM user WHERE id > %s", (4,))
    print(users)

    # 插入示例
    db.execute("INSERT INTO user (username, password, role, sex, telephone, address) VALUES (%s, %s, %s, %s, %s, %s)",\
               ("Alice", '123456',1,1,'17838346012','河南省郑州市'))

    # 批量插入
    data = [("Alice1", '123456',1,1,'17838346013','河南省郑州市'), \
            ("Alice2", '123456',1,1,'17838346014','河南省郑州市'), \
            ("Alice3", '123456',1,1,'17838346015','河南省郑州市')]
    db.execute_many("INSERT INTO user (username, password, role, sex, telephone, address) VALUES (%s, %s, %s, %s, %s, %s)", data)

    users = db.select("SELECT * FROM user")

    # 事务示例
    with db.transaction():
        db.execute("UPDATE user SET sex = 0 WHERE id = 5")
        db.execute("UPDATE user SET telephone = 17823846011 WHERE id = 6")