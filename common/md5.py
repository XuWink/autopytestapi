'''
MD5 已被证明不安全​​，因其易受碰撞攻击，不推荐用于密码存储等安全场景，在本项目中，为了简便，仍采用MD5加密方式，采用加盐方式保证安全。
'''

import hashlib
from config.setting import MD5_SALT

def encrypt_string(text : str, salt : str = MD5_SALT) -> str:
    """
    对字符串进行加密
    :param text: 待加密的字符串
    :param salt: 自定义盐值，确保md5安全
    :return: 十六进制哈希值
    """
    md5 = hashlib.md5()
    md5.update(f"{salt}{text}".encode('utf8'))
    return md5.hexdigest()
