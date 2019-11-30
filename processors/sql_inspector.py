import json

def count_stacked_query(query):

    return

def transform_for_sqli_model(package):
    """
    Features needed for model:
    1. tokenized request payload
    2. centrality
    3. request payload length
    4. query stack
    5. rows examined
    6. rows send

    """
    print("LETS TRANSFORM", package)

    # loop for every data in single request
    request_packet = package['req_packet']
    
    # print(type(request_packet['tokenization']))
    # for t in json.loads(request_packet['tokenization']):
    #     print(t, "HEHE")
        # result = {
        #     "token": t['token'],
        #     "centrality": t['centrality'],
        #     "payload_length": t['payload_length'],
        #     "n_stacked_query": count_stacked_query(request_packet['sql_data']['query']),
        #     "rows_send": request_packet['sql_stat']['num_rows'],
        #     "rows_affected": request_packet['sql_stat']['affected_rows']
        # }
        # print("RESULT BEBEH", result)
    # return result

def inspect(inspection_package):
    transform_for_sqli_model(inspection_package)
    return