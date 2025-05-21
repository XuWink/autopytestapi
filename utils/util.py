import os
import re
from common.md5 import encrypt_string

def get_base_path():
    """
    获取项目根目录
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_path


def validate_phone_number(phone):
    """验证手机号格式"""
    return len(phone) == 11 and re.match(r'^1[3-9]\d{9}$', phone) is not None


def check_password_hash(password_hash, password):
    '''验证数据库中的密码与登录输入的密码是否一直'''
    return password_hash == encrypt_string(password)