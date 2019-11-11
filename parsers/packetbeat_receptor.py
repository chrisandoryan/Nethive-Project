import socket
import threading
import json
from storage.redistor import RedistorClient
from dateutil.parser import parse
import traceback
import time
from utils import convert
from processors import xss_watcher

# import signal

bind_ip = '127.0.0.1'
bind_port = 5129

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

redis = RedistorClient.getInstance()

def keyboardInterruptHandler(signal, frame):
    server.close()

def parse_returned_sql_rows(raw_rows):
    # print("RAW_ROWS", raw_rows)
    raw_rows = list(filter(None, raw_rows.split("\n")))
    headers = raw_rows[0].split(",")
    responses = []
    for row in raw_rows[1:]:
        rsp_obj = {}
        row = row.split(",")
        for i in range(len(headers)):
            # print("ROW i", normalize_json_quote_problem(row[i]))
            rsp_obj[headers[i]] = normalize_json_quote_problem(row[i])
        responses.append(rsp_obj)
    # print("RESPONSES", responses)
    return responses

def parse_beat(beat_packet):
    # print("BEAT_PACKET", type(beat_packet), beat_packet)
    try:
        d = parse(beat_packet['@timestamp'])
        beat_packet = {
            'timestamp': int(time.mktime(d.timetuple())),
            'conn_stat': {
                'from_ip': beat_packet['client']['ip'],
                'from_port': beat_packet['client']['port'],
                'bytes': beat_packet['client']['bytes'],
            },
            'sql_method': beat_packet['method'],
            'sql_data': {
                'db_object': beat_packet['path'],
                'query': beat_packet['query'],
                'response': parse_returned_sql_rows(beat_packet['response']),
            },
            'sql_stat': {
                'affected_rows': beat_packet['mysql']['affected_rows'],
                'insert_id': beat_packet['mysql']['insert_id'],
                'num_fields': beat_packet['mysql']['num_fields'],
                'num_rows': beat_packet['mysql']['num_rows'],
            },
            'status': beat_packet['status']
        }
        # print("BEAT_PACKET_GREEN", beat_packet)
        return beat_packet
    except Exception as e:
        print(traceback.format_exc())

def rewrap_inspection_package(package, beat_data):
    try:
        package = {
            "req_packet": json.loads(package['req_packet']),
            "res_body": package['res_body'].encode(),
            "time": int(time.time())
        }
        package['req_packet']['sql_response'] = beat_data['sql_data']['response']
        return package
    except Exception as e:
        print(traceback.format_exc())
        return package

def get_flow_time_average():
    # TODO: write an algorithm to  calculate time between http and sql dynamically
    return 1.0

def normalize_json_quote_problem(the_data):
    """
        Setiap data yang mengandung double-quote (") pada database, ketika masuk ke packetbeat, double-quote tersebut akan menjadi double double-quote (""). Fungsi ini berguna untuk melakukan normalisasi terhadap anomali tersebut.

        Algorithm:
        1. remove wrapping double quote (at start and end of the data)
        2. for each of the remaining double quotes, remove half of it.
            Example:
                "nama saya adalah """"""ANDO""""""" | 6 double quotes before ANDO (exclude the double quotes in the beginning of the string), 7 double quotes after ANDO
                1 -> nama saya adalah """"""ANDO"""""" | 6 double quotes before ANDO, 6 double quotes after ANDO
                2 -> nama saya adalah \"\"\"ANDO\"\"\" | 6/2 double quotes before and after ANDO (remove the backslashes)
    """
    # 1
    if the_data.startswith('"') and the_data.endswith('"'):
        the_data = the_data[1:-1]
        # 2
        the_data = the_data.replace('""', '"')
    return the_data

def find_related_redisdata(package_ids, beat_data):
    for pack in package_ids:
        timestamp, package_id = pack
        package_id =  int(float(package_id))
        package = redis.rsGetAllPopOne("audit:{}".format(package_id))

        if package:
            package = rewrap_inspection_package(convert(package), beat_data)
            xss_watcher.domparse(package, False)

def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(4096)
        if not request:
            print("[Packetbeat_Receptor] Client has disconnected")
            client_socket.close()
            break
        try:
            # print("REQUEST", request.decode())
            beat = json.loads(request.decode("utf-8"))
            # print("BEAT", beat)
            if beat['type'] == 'mysql':
                beat = parse_beat(beat)

                if beat:
                    # print("BEAT TIMESTAMP: ", beat['timestamp'])
                    # print("SQL DATA INBOUND ON:", int(time.time()))
                    lower_boundary = int(int(time.time()) - get_flow_time_average())
                    upper_boundary = int(int(time.time()) + get_flow_time_average())
                    # print("LOWER_BOUNDARY: ", lower_boundary)
                    # print("UPPER_BOUNDARY: ", upper_boundary)
                    package_ids = redis.tsGetByRange(RedistorClient.TS_SELECT_KEY, lower_boundary, upper_boundary)
                    find_related_redisdata(package_ids, beat)
        except Exception as e:
            print(traceback.format_exc())
            pass

def start():
    # --- Set signal handlers
    # signal.signal(signal.SIGINT, keyboardInterruptHandler)

    while True:
        client_sock, address = server.accept()
        print('[Packetbeat_Receptor] Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

    server.close()

def run():
    print('[Packetbeat_Receptor] Listening on {}:{}'.format(bind_ip, bind_port))
    start()