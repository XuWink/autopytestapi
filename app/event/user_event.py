from common.logger import logger
from common.mysql import db
from common.md5 import encrypt_string
from common.redis import redis_client
from common.faker import generator

def get_all_users():
    sql = f"SELECT id, username, password, telephone, role, sex, address FROM user"
    data = db.select(sql)
    return data

def get_user(username : str):
    sql = f"""SELECT id, username, password, telephone, role, sex, address FROM user WHERE username=%s""".format(username)
    data = db.select_one(sql)
    logger.info("获取 {} 用户信息：{}".format(username, data))
    if data:
        return data
    return None

def select_by_username(username : str):
    sql = "SELECT id FROM user WHERE username=%s"
    data = db.select_one(sql, (username,))
    logger.info(f"""select_by_username 获取到用户名：{data}""")
    return data

def select_by_telephone(telephone : str):
    sql = "SELECT id FROM user WHERE telephone=%s"
    data = db.select_one(sql, (telephone,))
    logger.info(f"""select_by_telephone 获取到用户ID：{data}""")
    return data

def register(username, password, DEFAULT_ROLE, sex, telephone, address):
    sql = f"""
        INSERT INTO user(username, password, role, sex, telephone, address)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
    password = encrypt_string(f"{username}{password}")
    return db.execute(sql, (username, password, DEFAULT_ROLE, sex, telephone, address))