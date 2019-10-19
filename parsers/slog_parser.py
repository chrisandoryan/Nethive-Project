#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Overview
========

A small but useful tool to parser mysql slow query
contact: qingqibai@gmail.com

Usage summary
=============

You need to install python-sqlparse to run this tool
you may:
    apt-get install python-sqlparse
or:
    pip install sqlparse

How to use mysql-slow-query-parser to parser slow query::
    You can get help with ./parser -h or ./parser --help
    ./parser -f /var/log/mysql/slow-query.log (this will parser the last two hours slow query)
    tail -n2000 /var/log/mysql/slow-query.log|./parser (this will parser the lastest 2000 lines slow query)
    ./parser -f /var/log/mysql/slow-query.log -b'130811 13' -e'130811 15' -sa
    ./parser -f /var/log/mysql/slow-query.log -b'130818' -e'130809' -sc
    -f or --log_file: the mysql slow query log you want to parser
    -b or --begin-time: the begin time to parse, if not set, it will start at two hours ago
    -e or --end-time: the end time to parse, if not set, it will parse to now
    -t or --tmp-file: the tmp file, default /tmp/mysql-slow-query-parse
    -s or --sort: sort method, c: sort by count desc, t:sort by averger query time desc,
                  a: sort by c*t desc; default c
"""

import json
import sys
import re
import sqlparse
import argparse
from datetime import datetime, timedelta
from parsers.Slog import SlowQueryLog
from sqlparse.tokens import Token
from utils import tail
from utils import OutputHandler
import time
import csv
import os
import settings
from storage.memcache import MemCacheClient

MYSQL_SLOW_QUERY_LOG_PATH = os.getenv("MYSQL_SLOW_QUERY_LOG_PATH")
PARSED_SLOW_QUERY_LOG_PATH = os.getenv("PARSED_SLOW_QUERY_LOG_PATH")

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- (hopefully) Thread-safe request-to-response storage. Memc is used for system wide storage
memcache = MemCacheClient().getInstance()

class SlowQueryParser(object):

    outOfContextQueries = ("# administrator command:", "USE ")

    def __init__(self, stream):
        self.stream = stream

    def pattern(self, sql):
        res = sqlparse.parse(sql)
        if len(res) != 1:
            raise ValueError("Invalid sql: %s" % sql)
        stmt = res[0]
        tokens_queue = [stmt.tokens]
        while len(tokens_queue) > 0:
            tokens = tokens_queue.pop(0)
            for t in tokens:
                if hasattr(t, 'tokens'):
                    tokens_queue.append(t.tokens)
                else:
                    if self.is_atomic_type(t):
                        t.value = '?'
        return self.optimize(str(stmt))

    def is_atomic_type(self, token):
        t = self.token_type(token)
        if t == Token.Keyword and token.value == 'NULL':
            return True

        return t in {
            Token.Literal.Number.Integer,
            Token.Literal.Number.Float,
            Token.Literal.String.Single,
            Token.Literal.String.Symbol
        }

    def token_type(self, token):
        if hasattr(token, 'ttype'):
            return token.ttype
        return None

    def optimize(self, pattern):
        return re.sub("in\s+\([\?\s,]+\)", 'IN (?, ?)', pattern, flags=re.IGNORECASE)

    def strip_non_ascii(self, string):
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def remove_use_and_ts(self, sql):
        clean_patterns = ['use ', 'SET timestamp']
        for p in clean_patterns:
            if sql.startswith(p):
                sql = sql[sql.find(';') + 1:].strip()
        return sql.strip(';')

    def shorter(self, sql):
        sql = re.sub('(\d+\s*,\s*){32,}', '123321, 123321', sql)
        sql = re.sub("('\d+'\s*,\s*){32,}", "'123321', '123321'", sql)
        return sql

    def clean(self, sql):
        sql = self.strip_non_ascii(sql)
        sql = self.remove_use_and_ts(sql)
        sql = self.shorter(sql)
        return sql

    def prettify_sql(self, sql):
        if len(sql) > 400:
            return sql[0:200] + '...' + sql[-200:]
        return sql

    def read_by_chunks(self, fd, size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = fd.read(size)
            if not data:
                break
            yield data

    def calc_stats(self):
        for e in SlowQueryLog(self.stream):
            if not e.query_time:
                continue
            try:
                query_pattern = self.pattern(self.clean(e.query))
            except:
                pass
            entry = {
                'org': {
                    'datetime': e.datetime,
                    'database': e.database,
                    'user': e.user,
                    'host': e.host,
                },
                'query_time': e.query_time,
                'query_pattern': query_pattern,
                'query': self.clean(e.query),
                'rows_sent': e.rows_sent,
                'rows_examined': e.rows_examined,
            }
            yield entry

    def start_parser(self, outHand):
        stats = self.calc_stats()
        res = []
        for s in stats:
            if not s['query'].startswith(self.outOfContextQueries):
                with open(PARSED_SLOW_QUERY_LOG_PATH, 'a+') as f:
                    obj = {
                        'query': s['query'],
                        'query_time': s['query_time'],
                        'rows_sent': s['rows_sent'],
                        'rows_examined': s['rows_examined'],
                        'timestamp': int(time.mktime(s['org']['datetime'].timetuple()))
                    }   
                    outHand.sendLog(json.dumps(obj))
                    f.writelines(json.dumps(obj) + "\n") 

def run():
    global MYSQL_SLOW_QUERY_LOG_PATH, PARSED_SLOW_QUERY_LOG_PATH
    logfile = open(MYSQL_SLOW_QUERY_LOG_PATH, 'r')
    loglines = tail(logfile)

    outHand.info("[*] Starting SlogParser Engine...")
    query_parser = SlowQueryParser(loglines)
    query_parser.start_parser(outHand)
