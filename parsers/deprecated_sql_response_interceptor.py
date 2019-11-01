from utils import tail
from utils import OutputHandler
import settings
import os
import json
from storage.memcache import MemCacheClient
from observers import sql_connection

"""
SQL Response Interceptor powered by Packetbeat
(currently not used anymore)

"""

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- (hopefully) Thread-safe request-to-response storage. Memc is used for system wide storage
memcache = MemCacheClient().getInstance()

SQL_RESPONSE_LOG_PATH = os.getenv("SQL_RESPONSE_LOG_PATH")

def parse_output(line):
    try:
        line = json.loads(line)
    except Exception as e:
        print("[!] %s" % e)
    if 'mysql' in line:
        if line['query'] != sql_connection.CMD_PROCESSLIST and int(line['mysql']['num_rows']) > 0:
            query = line['query']
            result = line['response']
            src_port = line['client_port']
            print("===============")
            print(query)
            print(src_port)
            print("===============")
            for row in result.splitlines()[1:]:
                print(row)
                print("===============")
            # data = memcache.get('', '') # how to relate the data with the http request?
        # else:
        #     print("Skipping because of zero rows return")

def run():
    logfile = open(SQL_RESPONSE_LOG_PATH, 'r')
    loglines = tail(logfile)

    outHand.info("[*] Starting SQL Interceptor Engine...")
    for l in loglines:
        parse_output(l)
