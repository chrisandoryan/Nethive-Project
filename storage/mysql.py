import sys
import os
import settings
import threading

try:
    import MySQLdb  # MySQL-python
except ImportError:
    try:
        import pymysql as MySQLdb  # PyMySQL
    except ImportError:
        print("Please install MySQLdb or PyMySQL")
        sys.exit(1)

class MySQLClient(threading.local):
    __instance = None
    _conn = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if MySQLClient.__instance == None:
            MySQLClient()
        return MySQLClient.__instance
    def __init__(self):
        """ Virtually private constructor. """
        super(MySQLClient, self).__init__()
        if MySQLClient.__instance != None:
            # print("MySQLClient is a singleton!")
            pass
        else:
            MySQLClient._conn = MySQLdb.connect(host=os.getenv('MYSQL_HOSTNAME'), user=os.getenv('MYSQL_USER'), passwd=os.getenv('MYSQL_PASS'))
            MySQLClient.__instance = self
    @property
    def connection(self):
        return MySQLClient._conn
    def close(self):
        if MySQLClient.__instance != None:
            MySQLClient.__instance.close()
            MySQLClient.__instance = None
            MySQLClient()
            print(MySQLClient.__instance)