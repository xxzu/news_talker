import redis
from dotenv import load_dotenv
load_dotenv()

import os
HOST =  os.getenv("REDIS_HOST")
PORT = int(os.getenv('REDIS_PORT'))

class RedisHandler:
    def __init__(self, host=HOST, port=PORT, db=0,set_key = ""):
        """
        初始化 Redis 连接
        """
        self.set_key = set_key
        self.redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        
        

    # def add_to_set(self,  value: str) -> bool:
    #     """
    #     向 Redis 的 Set 中添加数据，自动去重。
    #     :param set_key: Redis Set 的键名
    #     :param value: 要添加的数据
    #     :return: 如果是新数据，返回 True；如果已存在，返回 False
    #     """
    #     return self.redis.sadd(self.set_key, value) == 1
    def add_to_set(self, value: str, ttl: int = 86400) -> bool:
        """
        向 Redis Set 中添加数据并设置过期时间
        :param value: 要添加的数据
        :param ttl: 数据过期时间（秒），默认为1小时
        """
        result = self.redis.sadd(self.set_key, value)
        if result == 1:  # 数据成功添加
            self.redis.expire(self.set_key, ttl)  # 设置过期时间
        return result
        
    def random_pop_messages(self):
        return self.redis.spop(self.set_key)
    
    def get_set_length(self):
        
        return len(self.redis.smembers(self.set_key))

    def is_in_set(self, value: str) -> bool:
        """
        检查数据是否在 Redis 的 Set 中
        :param set_key: Redis Set 的键名
        :param value: 要检查的数据
        :return: 存在返回 True，否则返回 False
        """
        return self.redis.sismember(self.set_key, value)

    def get_all_from_set(self, ) -> list:
        """
        获取 Redis Set 中的所有数据
        :param set_key: Redis Set 的键名
        :return: 返回包含所有数据的列表
        """
        return list(self.redis.smembers(self.set_key))

    def remove_from_set(self,  value: str) -> bool:
        """
        从 Redis 的 Set 中移除指定数据
        :param set_key: Redis Set 的键名
        :param value: 要移除的数据
        :return: 成功移除返回 True，否则返回 False
        """
        return self.redis.srem(self.set_key, value) == 1

    def delete_set(self, ) -> None:
        """
        删除整个 Redis Set
        :param set_key: Redis Set 的键名
        """
        self.redis.delete(self.set_key)
    def clear_all_data(self):
        """
        清空 Redis 数据库中的所有数据
        """
        # 清空当前数据库中的所有键
        self.redis.flushdb()  # 删除当前数据库中的所有数据

# 示例使用
if __name__ == "__main__":
    redis_handler = RedisHandler(set_key = "unique_data")

    

    # 添加数据
    print(redis_handler.add_to_set( "value1"))  # True (新数据)
    print(redis_handler.add_to_set("value2"))  # True (新数据)
    print(redis_handler.add_to_set( "value1"))  # False (重复数据)

    # 检查数据是否存在
    print(redis_handler.is_in_set("value1"))  # True
    print(redis_handler.is_in_set("value3"))  # False

    # 获取所有数据
    print(redis_handler.get_all_from_set())  # ['value1', 'value2']

    # 移除数据
    print(redis_handler.remove_from_set( "value1"))  # True
    print(redis_handler.get_all_from_set()  )# ['valu2']

    # 删除整个集合
    redis_handler.delete_set()
    print(redis_handler.get_all_from_set())  # []
