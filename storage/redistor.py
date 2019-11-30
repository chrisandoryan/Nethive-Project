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

    # Timeseries Query

    def ts_insert_http_bundle(self, key, timestamp, value, label):
        return self.__ts_client.add(key, timestamp, value, labels=label)
    def ts_get_http_bundles(self, start_time, end_time):
        return self.__ts_client.mrange(start_time, end_time, filters=['type=http'])
        # return self.__ts_client.info(key)
        # return self.__ts_client.mrange(start_time, end_time)
        # id = self.__ts_client.range(key, start_time, end_time)

    # End of Timeseries Query    

    # Redis Query

    def store_http_request(self, key, value):
        return self.__redis_client.hmset(key, value)
    def get_http_request(self, key):
        # from_redis = self.__redis_client.hgetall(key)
        # self.__redis_client.delete(key)
        return self.__redis_client.hgetall(key)

    # End of Redis Query

    