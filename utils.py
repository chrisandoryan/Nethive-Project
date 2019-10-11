import time
import requests
import sys
import queue


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
            print("This class is a singleton!")
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


    
