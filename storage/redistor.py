from redistimeseries.client import Client
import redis
from collections import defaultdict
from utils import QueueHashmap
import json

class RedistorClient:
    """Constants"""
    TS_INSERT_KEY = "insert"
    TS_SELECT_KEY = "select"
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if RedistorClient.__instance == None:
            RedistorClient()
        return RedistorClient.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if RedistorClient.__instance != None:
            print("RedistorClient is a singleton!")
        else:
            self.__ts_client = Client() # timeseries redis client
            self.__redis_client = redis.Redis() # general redis client
            try:
                self.__ts_client.create(self.TS_INSERT_KEY)
                self.__ts_client.create(self.TS_SELECT_KEY)
            except Exception as e:
                pass
            RedistorClient.__instance = self
    def tsInsert(self, key, timestamp, value):
        self.__ts_client.add(key, timestamp, value)
        return
    def rsMultiInsert(self, key_ns, value):
        self.__redis_client.hmset(key_ns, value)
        return
    def tsGetByRange(self, key, start_time, end_time):
        data = self.__ts_client.range(key, start_time, end_time)
        return data
    def rsGetAllPopOne(self, key):
        from_redis = self.__redis_client.hgetall(key)
        self.__redis_client.delete(key)
        return from_redis
    # def rsGetAndPop(self, key):
    #     from_redis = self.__ts_client.rpop(key)
    #     return from_redis


    