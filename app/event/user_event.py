from common.logger import logger
from common.mysql import db
from common.md5 import encrypt_string
from common.redis import redis_client
from common.faker import generator
from utils.util import check_password_hash, validate_phone_number

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

def select_by_ID(ID):
    sql = "SELECT username, password FROM user WHERE id=%s"
    data = db.select_one(sql, (ID,))
    logger.info(f"""select_by_ID 获取到用户名和密码：{data}""")
    return data

def register(username, password, DEFAULT_ROLE, sex, telephone, address):
    sql = f"""
        INSERT INTO user(username, password, role, sex, telephone, address)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
    password = encrypt_string(f"{username}{password}")
    return db.execute(sql, (username, password, DEFAULT_ROLE, sex, telephone, address))


def login_user(self, username, password):
        """登录用户"""
        try:
            # 查询用户
            user = select_by_username(username)
            if not user:
                return False, "用户名不存在"
            
            # 验证密码
            if not check_password_hash(user['password'], f"{username}{password}"):
                return False, "用户名或密码错误"
            
            # 生成 token
            import time
            time_stamp = int(time.time())
            token = encrypt_string(username, str(time_stamp))
            redis_client.set_value(username, token)
            
            # 构造登录信息
            login_info = {
                "id": user["id"],
                "username": username,
                "token": token,
                "login_time": time.strftime("%Y/%m/%d %H:%M:%S")
            }
            return True, login_info
        except Exception as e:
            logger.error(f"登录失败：{str(e)}")
            return False, "服务器内部错误"
        

def update_user(admin_user, token, id, new_password, new_sex, new_telephone, new_address):
    """更新用户信息"""
    # 验证输入
    if not admin_user or not token or not new_password or not new_telephone:
        return False, "管理员用户/token口令/密码/手机号不能为空，请检查！！！"
    if new_sex not in ("0", "1"):
        return False, "输入的性别只能是 0(男) 或 1(女)！！！"
    if not validate_phone_number(new_telephone):
        return False, "手机号格式不正确！！！"
    
    # 验证 token
    redis_token = redis_client.get_value(admin_user)
    if not redis_token or redis_token != token:
        return False, "token口令不正确或当前用户未登录，请检查！！！"
    if redis_client.is_key_expired(redis_token):
        return False, "token口令已过期或不存在，请重新登录"
    
    # 获取管理员角色
    user = select_by_username(admin_user)
    if user.get("role") != 0:
        return False, "当前用户不是管理员用户，无法进行操作，请检查！！！"
    
    user_info = select_by_ID(id)
    if not user_info:
        return False, "修改的用户ID不存在，无法进行修改，请检查！！！"
    
    if select_by_telephone(new_telephone):
        return False, "手机号已被注册，无法进行修改，请检查！！！"
    
    # 更新用户信息
    sql = f"UPDATE user SET password=%s,sex=%s,telephone=%s,address=%s WHERE id=%s"
    try:
        # 加密敏感信息
        encrypted_password = encrypt_string(user_info.get("username"), new_password)
        success = db.execute(sql, (encrypted_password, new_sex, new_telephone, new_address, id))
        if success:
            logger.info(f"用户 ID {id} 信息更新成功")
            return True, "恭喜，修改用户信息成功！"
        else:
            logger.error(f"更新用户 ID {id} 信息失败")
            return False, "修改用户信息失败"
    except Exception as e:
        logger.error(f"更新用户 ID {id} 信息时发生错误: {e}")
        return False, f"更新用户信息时发生错误: {e}"
    

def delete_user(admin_user, token, username):
    if not admin_user or not token or not username:
        return False, "管理员用户/token口令/要删除用户名不能为空，请检查！！！"

    # 验证 token
    redis_token = redis_client.get_value(admin_user)
    if not redis_token or redis_token != token:
        return False, "token口令不正确或当前用户未登录，请检查！！！"
    if redis_client.is_key_expired(redis_token):
        return False, "token口令已过期或不存在，请重新登录"
    
    # 获取管理员角色
    user = select_by_username(admin_user)
    if user.get("role") != 0:
        return False, "当前用户不是管理员用户，无法进行操作，请检查！！！"
    
    user_info = select_by_username(username)
    if not user_info:
        return False, "要删除的用户不存在"
    
    # 删除用户信息
    sql = f"DELETE FROM user WHERE username = %s "
    try:
        success = db.execute(sql, (username,))
        if success:
            logger.info(f"用户 {username} 删除成功")
            return True, "删除成功！"
        else:
            logger.error(f"删除用户 {username} 失败")
            return False, "删除失败"
    except Exception as e:
        logger.error(f"删除用户 {username} 时发生错误: {e}")
        return False, f"删除用户时发生错误: {e}"
    

def generat_fake(count):
    '''向数据库中批量插入假数据'''
    users = generator.generate_users(count=count)
    encrypted_users = [generator.get_encrypted_version(u) for u in users]
    
    sql = "INSERT INTO user (username, password, sex, telephone, address) VALUES (%s, %s, %s, %s, %s)"
    try:
        success = db.execute_many(sql,encrypted_users)
        if success:
            logger.info(f"插入了 {success} 条数据")
            return True, "成功！"
        else:
            logger.error(f"插入失败")
            return False, "失败"
    except Exception as e:
        logger.error(f"插入时发生错误: {e}")
        return False, f"插入时发生错误: {e}"
    