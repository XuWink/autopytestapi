from common.logger import logger
from common.mysql import db
from common.md5 import encrypt_string
from common.redis import redis_client
from common.faker import generator

def get_all_users():
    sql = f"SELECT id, username, password, telephone, role, sex, address FROM user"
    data = db.select(sql)
    return data