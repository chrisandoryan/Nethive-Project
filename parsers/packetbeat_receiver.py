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

bind_ip = '0.0.0.0'
bind_port = 5129

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

redis = RedistorClient.getInstance()

def keyboardInterruptHandler(signal, frame):
    server.close()

def parse_beat(beat_packet):
    try:
        d = parse(beat_packet['@timestamp'])
        return {
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
                'response': beat_packet['response'],
            },
            'sql_stat': {
                'affected_rows': beat_packet['mysql']['affected_rows'],
                'insert_id': beat_packet['mysql']['insert_id'],
                'num_fields': beat_packet['mysql']['num_fields'],
                'num_rows': beat_packet['mysql']['num_rows'],
            },
            'status': beat_packet['status']
        }
    except Exception as e:
        # print(e)
        # print(traceback.format_exc())
        pass

def dewrap_from_http(package):
    try:
        package = {
            "req_data": json.loads(package['req_data']),
            "res_body": package['res_body'].encode()
        }
        return package
    except Exception as e:
        pass
    return None

def get_flow_time_average():
    # TODO: write an algorithm to  calculate time between http and sql dynamically
    return 1.0

def find_related_redisdata(package_ids):
    for pack in package_ids:
        timestamp, package_id = pack
        package_id =  int(float(package_id))
        package = redis.rsGetAllPopOne("audit:{}".format(package_id))

        package = dewrap_from_http(convert(package))
        if package != None:
            xss_watcher.domparse(package['res_body'], package['req_data'], False)

def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(4096)
        try:
            beat = json.loads(request.decode())
            if beat['type'] == 'mysql':
                beat = parse_beat(beat)
                # print("BEAT TIMESTAMP: ", beat['timestamp'])
                # print("SQL DATA INBOUND ON:", int(time.time()))
                lower_boundary = int(int(time.time()) - get_flow_time_average())
                upper_boundary = int(int(time.time()) + get_flow_time_average())
                # print("LOWER_BOUNDARY: ", lower_boundary)
                # print("UPPER_BOUNDARY: ", upper_boundary)
                package_ids = redis.tsGetByRange(RedistorClient.TS_SELECT_KEY, lower_boundary, upper_boundary)
                find_related_redisdata(package_ids)
        except Exception as e:
            print("[!] %s" % e)
            # print(traceback.format_exc())

def start():
    # --- Set signal handlers
    # signal.signal(signal.SIGINT, keyboardInterruptHandler)

    while True:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

    # server.close()

def run():
    print('[Packetbeat_Receiver] Listening on {}:{}'.format(bind_ip, bind_port))
    start()