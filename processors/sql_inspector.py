import json
import sqlparse
import joblib
import csv
import os
import socket
import pandas as pd

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_PORT'))

""" Constants """

MODEL_LEARNING = False
ACTIVE_LABEL = "normal"

""" End of Constants """


def send_to_logstash(message):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        tcp_socket.sendall((json.dumps(message) + "\n").encode())
        tcp_socket.close()
    except Exception as e:
        print("[SQL Inspector] %s" % e)
        logger.exception(e)
    
    return

def count_stacked_query(query):
    res = sqlparse.split(query)
    return len(res) - 1

def transform_for_sqli_model(package):
    try:
        """
        Features needed for model:
        1. tokenized request payload -> need to process deeper
        2. centrality
        3. request payload length
        4. query stack
        5. rows examined
        6. rows send

        """
        results = []
        request_packet = package['req_packet']
        sql_response = package['sql_response']

        # loop for every param/body in a single request
        # e.g:
        # username=ao&password=123456 -- will loop twice, yet still categorized as a single request 
        for t in json.loads(request_packet['tokenization']):
            material = {
                "payload": t['payload'],
                "stacked_query": count_stacked_query(t['payload']), #request_packet['sql_data']['query']
                'punct_token': t['punct_token'],
                'spec_char': t['spec_char'],
                'sql_token': t['sql_token'],
                'dangerous_token': t['dangerous_token'],
                'hex_char': t['hex_char'],
                'whitespace': t['whitespace'],
                "error_code": 0,
            }

            if MODEL_LEARNING:
                # material["payload"] = t['payload']
                material["label"] = ACTIVE_LABEL
                # "tokenized_payload": t['tokenized_payload'],
                # "centrality": t['centrality'],
                # "rows_send": sql_response['sql_stat']['num_rows'],
                # "rows_affected": sql_response['sql_stat']['affected_rows'],
                # "payload_length": t['payload_length'],


            if sql_response['status'] != "OK":
                material['error_code'] = sql_response['sql_stat']['error_code']

            results.append(material)

        return results

    except Exception as e:
        print(e)
    
def inspect(inspection_package):
    transformed = transform_for_sqli_model(inspection_package)
    if transformed:
        if MODEL_LEARNING:
            write_learning_data(transformed)
        else:
            return predict(transformed, inspection_package['req_packet'])

def write_learning_data(learning_package):
    file_name = "/tmp/sqlinspection_%s.csv" % ACTIVE_LABEL
    file_exists = os.path.isfile(file_name)
    with open(file_name, "a+") as f:
        writer = csv.writer(f)
        if not file_exists and len(learning_package) > 0:
            writer.writerow(list(learning_package[0].keys()))
        for l in learning_package:
            writer.writerow(list(l.values()))

def train():
    # use old train.py from Frogod
    return

def retrain(learning_package):
    """ retrain model on-the-fly """

    return

def predict(inspection_package, request_data):
    sqli_model = joblib.load('./models/sqli.pkl')
    sqli_cols = joblib.load('./models/sqli_cols.pkl')

    result = {}

    for pkg in inspection_package:
        # print(pkg)

        compat_package = pd.DataFrame.from_dict([pkg])
        compat_package.drop('payload', axis=1, inplace=True)

        predict = sqli_model.predict(compat_package).tolist()
        # print(predict)

        pkg['classification'] = predict[0]

    result['url'] = request_data['url']
    result['body'] = request_data['body']
    result['client_ip'] = request_data['client_ip']
    result['client_port'] = request_data['client_port']
    result['inspection_result'] = inspection_package

    message = {'parsed_log': result, 'log_type': 'TYPE_SQLI_INSPECTOR'}
    print("SQLI INSPECTION RESULT", result)
    # send_to_logstash(message) # uncomment to store the result in its own index in elasticsearch

    return result