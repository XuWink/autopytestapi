import os
import re

def get_base_path():
    """
    获取项目根目录
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_path


def validate_phone_number(phone):
    """验证手机号格式"""
    return len(phone) == 11 and re.match(r'^1[3-9]\d{9}$', phone) is not None