#!/usr/bin/env python
# coding: utf-8

"""myprofiler - Casual MySQL Profiler

https://github.com/methane/myprofiler
"""

import sys
from time import sleep
from optparse import OptionParser

try:
    import MySQLdb  # MySQL-python
except ImportError:
    try:
        import pymysql as MySQLdb  # PyMySQL
    except ImportError:
        print("Please install MySQLdb or PyMySQL")
        sys.exit(1)

CMD_PROCESSLIST = "show full processlist"
DELAY = 0.000001 # 0.000002 # delay between processlist check
LIMIT = DELAY * 1000 # 1 # max wait for the web to open connection to the db)
def connect():
    return MySQLdb.connect(host='localhost', user='root', passwd='007isKingsman!')

def processlist(con):
    con.query(CMD_PROCESSLIST)
    for row in con.store_result().fetch_row(maxrows=200, how=1):
        if row['Info']:
            yield row

def run_once():
    try:
        con = connect()
    except Exception as e:
        print(e)
    proc_haystack = []
    time_elapsed = 0.0
    try:
        for row in processlist(con):
            if row['Info'] == CMD_PROCESSLIST:
                continue
            proc_haystack.append(row)
        # for q in list({v['Info']:v for v in proc_haystack}.values()):
        #     print(q)
        return list({v['Info']:v for v in proc_haystack}.values())
    except Exception as e:
        print(e)


def run():
    # print("Running SQL Connection")
    try:
        con = connect()
    except Exception as e:
        print(e)
    proc_haystack = []
    time_elapsed = 0.0
    try:
        while time_elapsed < float(LIMIT):
            # print(time_elapsed)
            for row in processlist(con):
                if row['Info'] == CMD_PROCESSLIST:
                    continue
                proc_haystack.append(row)
                # print(row)
            sleep(DELAY)
            time_elapsed += DELAY # update how many time has elapsed
        return list({v['Info']:v for v in proc_haystack}.values())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    run()
