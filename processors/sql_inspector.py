import json
import sqlparse

def count_stacked_query(query):
    res = sqlparse.split(query)
    return len(res) - 1

def transform_for_sqli_model(package):
    try:
        """
        Features needed for model:
        1. tokenized request payload
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
                "rows_affected": request_packet['sql_stat']['affected_rows']
            }
            results.append(material)

        return results
    except Exception as e:
        print(e)
    
def inspect(inspection_package):
    batch = transform_for_sqli_model(inspection_package)
    if batch:
        print(batch)
        return predict(batch)


def teach(learning_package):

    return

def predict(inspection_package):
    
    return