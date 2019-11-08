import time
import requests
import sys
import queue
from collections import defaultdict

class QueueHashmap(queue.Queue):
    def __init__(self, maxsize=65535):
        super().__init__(maxsize)
        self._store = defaultdict(lambda: defaultdict(list))
    def get_queue(self, key):
        return self._store.get(key, [])
    def pop(self, key, subkey):
        queue = self.get_queue(key)
        if queue:
            return queue[subkey].pop()
        return None
    def set(self, key, subkey, item):
        self._store[key][subkey].insert(0, item)
        return self._store[key][subkey]

class OutputHandler:
    __instance = None
    loggerQueue = queue.Queue()
    outerrQueue = queue.Queue()
    @staticmethod
    def getInstance():
        """ Static access method. """
        if OutputHandler.__instance == None:
            OutputHandler()
        return OutputHandler.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if OutputHandler.__instance != None:
            print("OutputHandler is a singleton!")
        else:
            OutputHandler.__instance = self
    # --- Helper function to create multiple output types
    def success(self, buffer):
        self.outerrQueue.put(buffer.strip())
        return        
    def info(self, buffer):
        self.outerrQueue.put(buffer.strip())
        return
    def warning(self, buffer):
        self.outerrQueue.put(buffer.strip())
        return
    def sendLog(self, buffer):
        self.loggerQueue.put(buffer.strip())
        return

def tail(logfile):
    logfile.seek(0, 2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.01)
            continue
        yield line

def send_request(url, payload, method):
    s = requests.Session()
    cookie = {
        "PHPSESSID": "6i865obsioa6a1q609q1fb543h",
        "security": "low"
    }
    if method == "GET":
        res = s.get(url, params=payload, cookies=cookie, allow_redirects=False)
    elif method == "POST":
        res = s.post(url, data=payload, cookies=cookie, allow_redirects=False)
    print(res.status_code)

def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x

def convert(data):
    if isinstance(data, bytes):  return data.decode()
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return tuple(map(convert, data))
    if isinstance(data, list):   return list(map(convert, data))
    return data