from scapy.all import *
from scapy.layers.http import *
import time
import os
import settings
import json
import uuid
import random
import socket

from processors import sql_tokenizer
from parsers import slog_parser

import observers

from utils import OutputHandler, QueueHashmap, decode_deeply

from storage.memcache import MemCacheClient
from storage.mysql import MySQLClient
from storage.redistor import RedisClient

import subprocess

HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
AUDIT_CONTROL_HOST = os.getenv("AUDIT_CONTROL_HOST")
AUDIT_CONTROL_PORT = int(os.getenv("AUDIT_CONTROL_PORT"))

sniff_mode = None

unsafe_content_types = [
    "text/html",
    "image/svg+xml",
    "text/xml",
]

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- (hopefully) Thread-safe request-to-response storage. Memc is used for system wide storage
# quehash = QueueHashmap() # merged into MemCacheClient
memcache = MemCacheClient().getInstance()
mysqlobj = MySQLClient.getInstance()
redis = RedisClient.getInstance()

def sniff_packet(interface):
    sniff(iface=interface, store=False, prn=process_packets(), session=TCPSession)

def write_httplog(packet, buffer):
    global HTTP_LOG_PATH, outHand

    timestamp = int(time.time())

    cookie = get_cookie_unidecoded(packet)
    user_agent = get_ua(packet)
    content_type = get_content_type(packet, HTTPRequest)
    referer = packet[HTTPRequest].Referer
    request_method = packet[HTTPRequest].Method
    host = packet[HTTPRequest].Host

    try:
        ip = packet[IP].src
    except Exception as e:
        outHand.warning("[!] %s" % e)
        ip = ""

    for s in sql_tokenizer.tokenize(buffer):
        s['cookie'] = cookie
        s['source_address'] = ip
        s['request_method'] = request_method.decode("utf-8")
        s['user_agent'] = user_agent
        s['centrality'] = ' '.join(map(str, list(s['centrality'].values())))
        s['host'] = host.decode("utf-8")
        s['timestamp'] = timestamp
        # print(s)
        # print(type(s))
        try:
            outHand.sendLog(json.dumps(s))
            with open(HTTP_LOG_PATH, 'a+') as f:
                f.writelines(json.dumps(s) + "\n")
        except Exception as e:
            print("[!] %s" % e)
        return    

def wrap_for_redis(packet):
    package = {
        "url": get_url_unidecoded(packet),
        "body": get_payload_unidecoded(packet),
    }
    return package

def wrap_for_auditor(req_data, res_body):
    package = {
        "req_packet": json.dumps(req_data),
        "res_body": res_body.decode()
    }
    return package

def relay_to_audit_control(the_package):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((AUDIT_CONTROL_HOST, AUDIT_CONTROL_PORT))
    tcp_socket.send((json.dumps(the_package) + "\n").encode())
    tcp_socket.close()

def get_mime_type(content_type):
    if content_type is None:
        return ['', '']
    content_type, *extra = content_type.split(';')
    return content_type, extra

# https://gist.github.com/thepacketgeek/6876699
def process_packets():
    # threading.Thread(target=observers.sql_connection.run, args=()).start()

    def processor(packet):
        global sniff_mode

        src, dst = get_ip_port(packet)
        ip_src, tcp_sport = src
        ip_dst, tcp_dport = dst
        
        # TODO: make this a thread/nonblocking
        # foo = observers.sql_connection.run()
        # if len(sql_processes) == 0:
        #     sql_processes = foo if len(foo) > 0 else sql_processes

        if packet.haslayer(HTTPRequest):
            # print("sql_processes2: ", sql_processes)
            # print(packet[HTTPRequest].show())
            # sql_conn_observer.start()

            # p = subprocess.Popen(['netstat', 'tulpn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # out, err = p.communicate()
            # print(out)

            url = get_url(packet)
            payload = get_payload(packet)

            if sniff_mode == "GET":
                write_httplog(packet, url)
            elif sniff_mode == "POST":
                write_httplog(packet, payload)
            elif sniff_mode == "*":
                write_httplog(packet, url)
                write_httplog(packet, payload)        

            # xss_watcher.inspect([url, payload])
            # memcache.set(ip_src, tcp_sport, wrap_for_redis(packet))
            redis.rs_multi_insert("{}:{}".format(ip_src, tcp_sport), wrap_for_redis(decode_deeply(packet)))
            
            # print(req_data)

        if packet.haslayer(HTTPResponse):
            # print(packet[HTTPResponse].show())
            content_type = get_content_type(packet, HTTPResponse)
            if get_mime_type(content_type)[0] in unsafe_content_types:
                # req_data = memcache.pop(ip_dst, tcp_dport)
                req_data = redis.rs_get_all_pop_one("{}:{}".format(ip_dst, tcp_dport))
                if req_data:
                    req_data['client_ip'] = ip_dst
                    req_data['client_port'] = str(tcp_dport)
                    res_body = get_payload(packet)

                    """ 
                    Algorithm for Deep Inspection:
                        1. store timestamp and package_id in redistimeseries
                        2. store package for inspection in redis
                        3. from packetbeat_receptor.py, find all ids matching the specified timestamp
                    
                    Algorithm for Light Inspection:
                        1. send inspection packet to packetbeat_receptor.py with 'http' as the packet type

                    Light inspection works in near realtime, while deep inspection increases accuracy since it also checks the sql response data.
                    """
                    package_id = random.getrandbits(48) # generate random 48bit integer # uuid.uuid4().int >> 8
                    current_timestamp = int(time.time())

                    the_package = wrap_for_auditor(decode_deeply(req_data), res_body)

                    # --1. Deep Inspection
                    redis.ts_insert(RedisClient.TS_STORE_KEY, current_timestamp, package_id)
                    # --2. Deep Inspection
                    redis.rs_multi_insert("audit:{}".format(package_id), the_package)

                    # --1. Light Inspection
                    the_package['type'] = 'http'
                    relay_to_audit_control(the_package)

                    # xss_watcher.domparse(res_body, req_data, False)

    return processor

def get_url(packet):
    return packet[HTTPRequest].Path

def get_url_unidecoded(packet):
    return get_url(packet).decode('utf-8')

def get_referer(packet):
    return packet[HTTPRequest].Referer

def get_method(packet):
    return packet[HTTPRequest].Method

def get_cookie_unidecoded(packet):
    try:
        return packet[HTTPRequest].Cookie.decode('utf-8')
    except Exception as e:
        outHand.warning("[!] %s" % e)
        return bytearray()

def get_ua(packet):
    try:
        return getattr(packet[HTTPRequest], 'User_Agent').decode("utf-8")
    except Exception as e:
        outHand.warning("[!] %s" % e)
        return ""

def get_ip_port(packet):
    ip_src = ip_dst = tcp_sport = tcp_dport = None
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
    if TCP in packet:
        tcp_sport = packet[TCP].sport
        tcp_dport = packet[TCP].dport
    return((ip_src, tcp_sport), (ip_dst, tcp_dport))

def get_content_type(packet, state):
    try:
        return getattr(packet[state], 'Content_Type').decode("utf-8")
    except Exception as e:
        outHand.warning("[!] %s" % e)
        pass

def get_longurl(packet):
    return packet[HTTPRequest].Host + packet[HTTPRequest].Path

def get_payload(packet):
    if packet.haslayer(Raw):
        return packet[Raw].load
    else:
        return bytearray()

def get_payload_unidecoded(packet):
    return get_payload(packet).decode('utf-8')

""" sniff_mode: GET, POST, * """
def run(sniffMode, iface):
    global sniff_mode, outHand
    sniff_mode = sniffMode
    outHand.info("[*] Starting HTTPSensor Engine...")
    sniff_packet(iface)

