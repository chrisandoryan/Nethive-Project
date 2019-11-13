from redistimeseries.client import Client
import redis
from collections import defaultdict
from utils import QueueHashmap
import json

class RedisClient:
    """Constants"""
    TS_STORE_KEY = "nethive"
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if RedisClient.__instance == None:
            RedisClient()
        return RedisClient.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if RedisClient.__instance != None:
            print("RedisClient is a singleton!")
        else:
            self.__ts_client = Client() # timeseries redis client
            self.__redis_client = redis.Redis() # general redis client
            try:
                self.__ts_client.create(self.TS_STORE_KEY)
            except Exception as e:
                pass
            RedisClient.__instance = self
    def ts_insert(self, key, timestamp, value):
        return self.__ts_client.add(key, timestamp, value)
    def rs_multi_insert(self, key_ns, value):
        return self.__redis_client.hmset(key_ns, value)
    def ts_get_by_range(self, key, start_time, end_time):
        return self.__ts_client.range(key, start_time, end_time)
    def rs_get_all_pop_one(self, key):
        from_redis = self.__redis_client.hgetall(key)
        self.__redis_client.delete(key)
        return from_redis

    