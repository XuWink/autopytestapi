import os
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.util import get_base_path

BASE_PATH = get_base_path()
# 定义日志文件路径
LOG_PATH = os.path.join(BASE_PATH, "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger:
    _instance = None  # 单例模式实例
    _initialized = False  # 初始化标志

    def __new__(cls, log_path=None, log_level=logging.DEBUG):
        # 实现单例模式
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_path=None, log_level=logging.DEBUG):
        # 防止重复初始化
        if self._initialized:
            return

        # 设置日志路径
        self.log_path = log_path or LOG_PATH
        os.makedirs(self.log_path, exist_ok=True)

        # 配置日志
        self.logger = logging.getLogger("app")
        self.logger.setLevel(log_level)

        # 设置日志格式
        self.formatter = logging.Formatter(
            '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]: %(message)s'
        )

        # 添加文件处理器（每天自动切割日志）
        self._add_file_handler()

        # 添加控制台处理器
        self._add_console_handler()

        self._initialized = True

    def _add_file_handler(self):
        # 使用时间轮转文件处理器，每天生成一个新日志文件
        now = datetime.now()
        formatted = now.strftime("%Y%m%d")
        log_file = os.path.join(self.log_path, f"{formatted}.log")
        file_handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",
            interval=1,
            backupCount=30,  # 保留30天的日志
            encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)  # 文件中记录INFO及以上级别
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def _add_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # 控制台显示DEBUG及以上级别
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


# 全局日志实例
logger = Logger().get_logger()

def test():
    logger.info("---测试开始---")
    logger.debug("---测试结束---")
    logger.error("---<UNK>---")
    logger.warning("---<UNK>---")

if __name__ == '__main__':
    test()