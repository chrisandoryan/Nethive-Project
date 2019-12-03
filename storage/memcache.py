import pylibmc
import queue
from collections import defaultdict
from utils import QueueHashmap
import json

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
            # print("MemCacheClient is a singleton!")
            pass
        else:
            self._store = defaultdict(lambda: defaultdict(list))
            self.__memcache_client = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"cas": True, "tcp_nodelay": True, "ketama": True})
            MemCacheClient.__instance = self

    def set(self, key, subkey, item):
        super().set(key, subkey, item)
        # print("Set to {} with data {}".format(key, json.dumps(self._store[key])))
        return self.__memcache_client.set(key, self._store[key])
        # return self.__memcache_client.set(key, json.dumps(self._store[key]))

    def get(self, key):
        return self.__memcache_client.get(key)

    def pop(self, key, subkey):
        queue = self.get(key)
        if queue:
            try:
                popped = queue[int(subkey)].pop()
                return popped
            except Exception as e:
                print("[!] %s" % e)
        return None
 
    def update(self, key, subkey, add_key, add_value):
        the_dict = self.get(key) 
        for i in range(len(the_dict[int(subkey)])):
            the_dict[int(subkey)][i][add_key] = add_value
        self._store[key] = the_dict
        return self.__memcache_client.set(key, self._store[key])


