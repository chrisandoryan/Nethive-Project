import pylibmc
import queue
from collections import defaultdict

class QueueHashmap(queue.Queue):
    def __init__(self, maxsize=65535):
        super().__init__(maxsize)
        self._store = defaultdict(lambda: defaultdict(list))

    def get_queue(self, key):
        print("GET_QUE", self._store.get(key, []))
        return self._store.get(key, [])

    def pop(self, key, subkey):
        queue = self.get_queue(key)
        if queue:
            return queue[subkey].pop()
        return None
    
    def set(self, key, subkey, item):
        self._store[key][subkey].insert(0, item)
        print("SET", self._store[key][subkey])
        return self._store[key][subkey]

class MemCacheClient:
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
            MemCacheClient.__instance = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
    def set(self, key, subkey, item):
        super()
        self._store[key][subkey].insert(0, item)
        self.__instance.set(key, self._store[key])
