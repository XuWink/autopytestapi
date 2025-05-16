from typing import Optional, Any, Union
import redis
from config.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWD,  DB_ID, MAX_CONNECTIONS, EXPIRE_TIME
from common.logger import logger

class RedisClient:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, 
                 password: str = REDIS_PASSWD, db: int = DB_ID,
                 max_connections: int = MAX_CONNECTIONS):
        """
        初始化 Redis 连接
        
        :param host: Redis 服务器地址
        :param port: Redis 服务器端口
        :param password: Redis 密码
        :param db: 数据库编号
        :param max_connections: 连接池最大连接数
        """
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            db=db,
            max_connections=max_connections,
            decode_responses=True
        )
        # self.expire = expire
        self._redis = redis.Redis(connection_pool=self.pool)
    
    @property
    def client(self) -> redis.Redis:
        """获取客户端实例"""
        return self._redis
    
    def set_value(self, key : str, value : Any, expire : int = EXPIRE_TIME) -> bool:
        """
        设置键值对，可设置过期时间
        
        :param key: 键名
        :param value: 值
        :param expire: 过期时间(秒)
        :return: 是否设置成功
        """
        try:
            if expire:
                return self._redis.setex(key, expire, value)
            return self._redis.set(key, value)
        except redis.RedisError as e:
            # raise RedisOperationError(f"Redis 设置键值失败: {e}")
            logger.error(f"Redis 设置键值失败: {e}")

    def get_value(self, key : str) -> Optional[str]:
        """
        获取值
        :param key: 键
        :return: 键值，如果不存在则返回None
        """
        try:
            return self._redis.get(key)
        except redis.RedisError as e:
            logger.error(f"Redis 获取键值失败：{e}")
    
    def delete_key(self, *key: str) -> int:
        """
        删除一个或多个键
        :param key: 要删除的键名
        :return: 返回删除的个数
        """
        try:
            return self._redis.delete(*key)
        except redis.RedisError as e:
            logger.error(f"Redis 删除键失败：{e}")

    def expire_key(self, key: str, expire: int) -> bool:
        """
        设置键的过期时间
        
        :param key: 键名
        :param expire: 过期时间(秒)
        :return: 是否设置成功
        """
        try:
            return self._redis.expire(key, expire)
        except redis.RedisError as e:
            logger.error(f"Redis 设置过期时间失败: {e}")

    def key_exists(self, key: str) -> bool:
        """
        检查键是否存在
        
        :param key: 键名
        :return: 键是否存在
        """
        try:
            return self._redis.exists(key) == 1
        except redis.RedisError as e:
            logger.error(f"Redis 检查键存在失败: {e}")

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWD,  DB_ID, MAX_CONNECTIONS)


def test():
    # 设置键值
    redis_client.set_value("user:token:123", "abc123", expire=3600)

    # 获取值
    token = redis_client.get_value("user:token:123")
    print(token)  # 输出: abc123

    # 检查键是否存在
    if redis_client.key_exists("user:token:123"):
        print("键存在")

    # 删除键
    del_num = redis_client.delete_key("user:token:123")
    print(f"删除了几个：{del_num}")

    # # 使用原生 Redis 客户端（如果需要）
    # r = redis_client.client
    # r.sadd("users", "user1", "user2")