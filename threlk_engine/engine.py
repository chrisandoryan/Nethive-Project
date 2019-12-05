from elasticsearch import Elasticsearch
from kafka import KafkaProducer

import historian, auditbeat, webflow
import threading
import time
import json

"""
Threlk Engine is the engine that specifically constructed to process raw data from the ELK infrasctructure into something more useful for the client.

"""

es = Elasticsearch(hosts="http://elastic:changeme@localhost:9200/")
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), compression_type='gzip', bootstrap_servers='localhost:1234')

BASH_INDEX = "nethive-bash-*"
SQLI_INDEX = "nethive-sqli-*"
XSS_INDEX = "nethive-xss-*"
AUDIT_INDEX = "nethive-audit-*"

KAFKA_TOPIC = "LEXY"

FETCH_SIZE = 10
SORT = "desc"

def initial_search(targetIndex):
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
    for result in parser_function(hits):
        if result:
            producer.send(KAFKA_TOPIC, {'foo': 'bar'})

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

def start():
    print("[Threlk Engine] Starting Threlk...")
    threading.Thread(target=elastail, args=(BASH_INDEX, historian.parse)).start() 
    threading.Thread(target=elastail, args=(AUDIT_INDEX, auditbeat.parse)).start()
    print("[Threlk Engine] Started.")

# https://gist.github.com/hmldd/44d12d3a61a8d8077a3091c4ff7b9307