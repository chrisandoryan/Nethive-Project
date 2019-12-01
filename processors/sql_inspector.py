import json
import sqlparse
import joblib
import csv

""" Constants """

MODEL_LEARNING = False
PAYLOAD_TYPE = "normal"

""" End of Constants """

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

        # loop for every param/body in a single request
        # e.g:
        # username=ao&password=123456 -- will loop twice, yet still categorized as a single request 
        for t in json.loads(request_packet['tokenization']):
            material = {
                "token": t['token'],
                "centrality": t['centrality'],
                "payload_length": t['payload_length'],
                "stacked_query": count_stacked_query(t['payload']), #request_packet['sql_data']['query']
                "rows_send": request_packet['sql_stat']['num_rows'],
                "rows_affected": request_packet['sql_stat']['affected_rows'],
                "label": PAYLOAD_TYPE
            }
            results.append(material)

        return results
    except Exception as e:
        print(e)
    
def inspect(inspection_package):
    transformed = transform_for_sqli_model(inspection_package)
    if transformed:
        if MODEL_LEARNING:
            write_learning_data(transformed)
        return predict(transformed)

def write_learning_data(learning_package):
    # headers: token,centrality,payload_length,stacked_query,rows_send,rows_affected,label
    with open("/tmp/sqlinspection.csv", "a+") as f:
        writer = csv.writer(f)
        for l in learning_package:
            writer.writerow(list(l.values()))

def teach(learning_package):
    """ retrain model on-the-fly """

    return

def predict(inspection_package):
    sqli_model = joblib.load('./models/sqli.pkl')
    sqli_cols = joblib.load('./models/sqli_cols.pkl')
    # print(sqli_cols)

    return