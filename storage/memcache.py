import pylibmc
import queue
from collections import defaultdict
from utils import QueueHashmap

class MemCacheClient(QueueHashmap):
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if MemCacheClient.__instance == None:
            MemCacheClient()
        return MemCacheClient.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if MemCacheClient.__instance != None:
            print("MemCacheClient is a singleton!")
        else:
            self._store = defaultdict(lambda: defaultdict(list))
            self.__memcache_client = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"cas": True, "tcp_nodelay": True, "ketama": True})
            MemCacheClient.__instance = self
    def set(self, key, subkey, item):
        super().set(key, subkey, item)
        print("Set to {} with data {}".format(key, self._store[key]))
        return self.__memcache_client.set(key, self._store[key])
    def get(self, key, subkey):
        return self.__memcache_client.get('key')
