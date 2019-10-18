import pylibmc

class MemcacheClient:
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if MemcacheClient.__instance == None:
            MemcacheClient()
        return MemcacheClient.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if MemcacheClient.__instance != None:
            print("MemcacheClient is a singleton!")
        else:
            mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
            MemcacheClient.__instance = mc