import os

def get_base_path():
    """
    获取项目根目录
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_path