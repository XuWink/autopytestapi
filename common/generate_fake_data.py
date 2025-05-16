"""
使用Fake生成假数据，
"""
import os
import csv
import random
from faker import Faker
from typing import List, Dict, Optional, Union
from common.md5 import encrypt_string
from utils.util import get_base_path
from config.conf import FAKE_PASSWORD

class UserDataGenerator:
    """
    用户数据生成器（保存明文密码版本）
    功能：
    1. 生成随机用户数据（密码明文保存）
    2. 可选密码加密功能
    3. 导出CSV文件
    
    示例用法：
    >>> generator = UserDataGenerator(locale='zh_CN')
    >>> users = generator.generate_users(count=100, encrypt=False)
    >>> generator.export_to_csv(users, "output.csv")
    """
    
    def __init__(self, locale: str = 'zh_CN'):
        """
        初始化生成器
        :param locale: 地区设置，决定生成数据的语言/格式
        """
        self.fake = Faker(locale=locale)
        self._default_csv_fields = [
            'username', 
            'password',  # 明文密码
            'role', 
            'sex', 
            'telephone', 
            'address'
        ]
    
    def _generate_single_user(self) -> Dict[str, Optional[Union[str, int]]]:
        """
        生成单个用户数据（内部方法）
        :return: 用户数据字典（包含明文密码）
        """
        return {
            'username': self.fake.name(),
            'password': FAKE_PASSWORD if FAKE_PASSWORD else self.fake.password(
                length=8,
                special_chars=False,
                digits=True,
                upper_case=True,
                lower_case=True
            ),
            'role': random.choice([0, 1]),
            'sex': random.choice([0, 1, None]),
            'telephone': self.fake.phone_number(),
            'address': self.fake.address()
        }
    
    def generate_users(self, count: int = 100) -> List[Dict]:
        """
        批量生成用户数据（明文密码）
        :param count: 生成数量
        :return: 用户数据列表
        """
        return [self._generate_single_user() for _ in range(count)]
    
    def export_to_csv(
        self, 
        users: List[Dict], 
        filepath: str, 
        fields: Optional[List[str]] = None,
        encoding: str = 'utf-8'
    ) -> None:
        """
        导出用户数据到CSV文件（保持密码明文）
        :param users: 用户数据列表
        :param filepath: 文件路径
        :param fields: 要导出的字段（默认全部导出）
        :param encoding: 文件编码
        """
        fields = fields or self._default_csv_fields

        filepath = os.path.join(get_base_path(), f'data/{filepath}')
        
        with open(filepath, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(users)
    
    def get_encrypted_version(self, user: Dict) -> Dict:
        """
        获取加密版本的用户数据（不影响原始数据）
        :param user: 原始用户数据
        :return: 加密后的用户数据
        """
        encrypted = user.copy()
        combined = f"{encrypted['username']}{encrypted['password']}"
        encrypted['password'] = encrypt_string(combined)
        return encrypted
    
    def generate(
        self, 
        filepath: str = None, 
        count: int = 100,
        return_users: bool = False
    ) -> Optional[List[Dict]]:
        """
        生成并保存用户数据（快捷方法，保持密码明文）
        :param filepath: 保存路径
        :param count: 生成数量
        :param return_users: 是否返回生成的数据
        :return: 可选返回用户数据
        """
        users = self.generate_users(count)
        if filepath:
            filepath = os.path.basename(filepath)
            self.export_to_csv(users, filepath)
        return users if return_users else None

generator = UserDataGenerator(locale='zh_CN')

# 使用示例
def test():
    # 1. 初始化生成器
    # generator = UserDataGenerator(locale='zh_CN')
    
    # 2. 生成100个用户（明文密码）
    # users = generator.generate_users(count=100)
    
    # # 3. 导出明文密码到CSV
    # csv_path = os.path.join(get_base_path(), 'data')
    # if not os.path.exists(csv_path):
    #     os.mkdir(csv_path)
    # generator.export_to_csv(users, os.path.join(csv_path, "users_plaintext.csv"))
    
    # # 4. 获取加密版本（不影响原始数据）
    # encrypted_users = [generator.get_encrypted_version(u) for u in users]
    # print(f"示例加密密码: {encrypted_users[0]['password']}")
    
    # 或者使用快捷方法
    generator.generate("users_plaintext.csv", count=100)

if __name__ == "__main__":
    test()