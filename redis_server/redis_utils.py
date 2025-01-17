import redis
import os
import logging
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT"))
DB = int(os.getenv("REDIS_DB"))

logging.basicConfig(level=logging.INFO)

class RedisHandler:
    def __init__(self, host=HOST, port=PORT, db=DB, set_key="", default_ttl=86400):
        self.set_key = set_key
        self.default_ttl = default_ttl
        self.redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def add_to_set(self, value: str, ttl: int = None) -> bool:
        ttl = ttl or self.default_ttl
        result = self.redis.sadd(self.set_key, value)
        if result == 1:
            self.redis.expire(self.set_key, ttl)
            logging.info(f"Added {value} to {self.set_key} with TTL {ttl}")
        return result

    def add_multiple_to_set(self, values, ttl: int = None) -> None:
        for value in values:
            self.add_to_set(value, ttl)

    def random_pop_messages(self):
        return self.redis.spop(self.set_key)

    def get_set_length(self):
        return len(self.redis.smembers(self.set_key))

    def is_in_set(self, value: str) -> bool:
        if value is None or not isinstance(value, (str, bytes, int, float)):
            raise ValueError(f"Invalid value: {value}")
        return self.redis.sismember(self.set_key, value)

    def get_all_from_set(self) -> list:
        return list(self.redis.smembers(self.set_key))

    def remove_from_set(self, value: str) -> bool:
        return self.redis.srem(self.set_key, value) == 1

    def remove_multiple_from_set(self, values) -> None:
        for value in values:
            self.remove_from_set(value)

    def delete_set(self) -> None:
        self.redis.delete(self.set_key)

    def clear_database(self) -> None:
        self.redis.flushdb()
        logging.warning("Redis database cleared!")

# 示例使用
if __name__ == "__main__":
    redis_handler = RedisHandler(set_key="unique_data")

    redis_handler.add_to_set("value1")
    redis_handler.add_to_set("value2")
    print(redis_handler.get_all_from_set())
