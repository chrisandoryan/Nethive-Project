from elasticsearch import Elasticsearch
from kafka import KafkaProducer
from threlk_engine import _auditmon, _bashmon, _httpmon

import threading
import time
import json
import logging
import os
import settings

logger = logging.getLogger('elasticsearch')
logger.setLevel(logging.CRITICAL)
logger.addHandler(logging.FileHandler('threlk.log'))

"""
Threlk Engine is the engine that specifically constructed to process raw data from the ELK infrasctructure into something more useful for the client.

"""

es = None
producer = None

BASH_INDEX = "nethive-bash-*"
HTTPMON_INDEX = "nethive-httpmon-*"
AUDIT_INDEX = "nethive-audit-*"
SQLI_INDEX = "nethive-sqli-*"
XSS_INDEX = "nethive-xss-*"

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")

FETCH_SIZE = 10
SORT = "desc"

def initial_search(targetIndex):
    global es
    return es.search(index=targetIndex, body={
        "query": {
            "match_all": {}
        },
        "size": FETCH_SIZE,
        "sort": [
            {
                "@timestamp": {
                    "order": SORT
                }
            }
        ]
    })


def next_search(targetIndex, lastTimestamp, prevIds):
    global es
    return es.search(index=targetIndex, body={
        "query": {
            "bool": {
                "must": {
                    "range": {
                        "@timestamp": {
                            "gte": lastTimestamp,
                        }
                    },
                },
                "must_not": {
                    "ids": {
                        "values": prevIds
                    }
                },
            }
        },
        "from": 0,
        "size": FETCH_SIZE,
        "sort": [
            {
                "@timestamp": {
                    "order": SORT
                }
            }
        ]
    })

def display_hits(hits):
    for hit in hits:
        print(hit, "\n") 

def relay_to_kafka(parser_function, hits):
    global producer
    for result in parser_function(hits):
        if result:
            foo = producer.send(KAFKA_TOPIC, result)
            print(result, "\n")
            meta = foo.get(timeout=60)
            print("Offset: %d" % meta.offset)

def elastail(targetIndex, parser_function):
    first = initial_search(targetIndex)

    hits = first['hits']['hits']
    # display_hits(hits)
    relay_to_kafka(parser_function, hits)

    lastHitTimestamp = hits[0]['_source']['@timestamp']
    # print(lastHitTimestamp)
    # print(len(hits))

    prevIds = [hit['_id'] for hit in hits]
    # print(prevIds)

    delay = 0.5
    currentHitTimestamp = ""

    while True:
        # print("Fetching...")
        # print("Current: ", currentHitTimestamp)
        # print("Last: ", lastHitTimestamp)
        time.sleep(delay)
        if currentHitTimestamp != lastHitTimestamp:

            if currentHitTimestamp != "":
                lastHitTimestamp = currentHitTimestamp

            next = next_search(targetIndex, lastHitTimestamp, prevIds)
            hits = next['hits']['hits']

            if next['hits']['total']['value'] > 0:
                # print([hit['_source']['@timestamp'] for hit in hits])

                currentHitTimestamp = hits[0]['_source']['@timestamp']
                # print(currentHitTimestamp)

                prevIds = [hit['_id'] for hit in hits]

                relay_to_kafka(parser_function, hits)

            else:
                currentHitTimestamp = ""
                # print("Already up to date.")
        else:
            # print("Here")
            pass
    
    if next['hits']['total']['value'] > 0 and delay > 0.5:
        delay = 0.5
    elif delay <= 2:
        delay = delay + 0.5
    
def booting():
    global es, producer
    es_online = False
    kafka_online = False
    es = Elasticsearch(hosts="http://elastic:changeme@localhost:9200/")
    print("[Threlk Engine] Waiting for Elasticsearch and Kafka to start...")
    while not es_online and not kafka_online:
        try:
            producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), compression_type='gzip', bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
            if es.ping():
                print("[Threlk Engine] Elasticsearch is online. Starting...")
                es_online = True
            else:
                print("[Threlk Engine] Waiting for Elasticsearch to start...")
            if producer.bootstrap_connected():
                print("[Threlk Engine] Kafka is online. Starting...")
                kafka_online = True
            else:
                print("[Threlk Engine] Waiting for Kafka to start...")
            time.sleep(3)
        except Exception as e:
            pass

def start():
    print("[Threlk Engine] Initiating Threlk Engine...")
    booting()
    # threading.Thread(target=elastail, args=(BASH_INDEX, _bashmon.parse)).start() 
    threading.Thread(target=elastail, args=(AUDIT_INDEX, _auditmon.parse)).start()
    # threading.Thread(target=elastail, args=(HTTPMON_INDEX, _httpmon.parse)).start()
    print("[Threlk Engine] Started.")

# start()

# https://gist.github.com/hmldd/44d12d3a61a8d8077a3091c4ff7b9307