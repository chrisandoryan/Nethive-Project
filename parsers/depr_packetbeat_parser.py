from utils import tail
from utils import OutputHandler
import settings
import os
import json
from storage.memcache import MemCacheClient

"""
SQL Response Interceptor powered by Packetbeat

"""

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- (hopefully) Thread-safe request-to-response storage. Memc is used for system wide storage
memcache = MemCacheClient().getInstance()

SQL_RESPONSE_LOG_PATH = os.getenv("SQL_RESPONSE_LOG_PATH")

def parse_output(line):
    try:
        line = json.loads(line)
        print(line)
    except Exception as e:
        print("[!] %s" % e)

def run():
    logfile = open(SQL_RESPONSE_LOG_PATH, 'r')
    loglines = tail(logfile)

    outHand.info("[*] Starting SQL Interceptor Engine...")
    print("[*] Starting SQL Packetparser Engine...")
    for l in loglines:
        parse_output(l)
