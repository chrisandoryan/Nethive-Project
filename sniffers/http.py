from scapy.all import *
from scapy.layers.http import *
import time
import os
import settings
import json

from processors import sql_tokenizer
from parsers import slog_parser

HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
mode = None

def sniff_packet(interface, queue):
    sniff(iface=interface, store=False, prn=process_packets(queue), session=TCPSession)

def write_httplog(packet, buffer, queue):
    global HTTP_LOG_PATH
    # print(packet[HTTPRequest].show())

    timestamp = int(time.time())

    cookie = get_cookie(packet)
    user_agent = get_ua(packet)
    content_type = get_content_type(packet)
    referer = packet[HTTPRequest].Referer
    request_method = packet[HTTPRequest].Method
    host = packet[HTTPRequest].Host

    try:
        ip = packet[IP].src
    except Exception as e:
        print("[!] %s" % e)
        ip = ""

    for s in sql_tokenizer.tokenize(buffer):
        s['cookie'] = cookie
        s['source_address'] = ip
        s['request_method'] = request_method.decode("utf-8")
        s['user_agent'] = user_agent
        s['centrality'] = ' '.join(map(str, list(s['centrality'].values())))
        s['host'] = host.decode("utf-8")
        s['timestamp'] = timestamp
        queue.put(s)
        with open(HTTP_LOG_PATH, 'a') as f:
            f.writelines(json.dumps(s) + "\n")
        return    

# https://gist.github.com/thepacketgeek/6876699
def process_packets(queue):
    def processor(packet):
        global mode
        if packet.haslayer(HTTPRequest):
            url = packet[HTTPRequest].Path
            payload = get_payload(packet)
            if mode is "GET":
                write_httplog(packet, url, queue)
            elif mode is "POST":
                write_httplog(packet, payload, queue)
            elif mode is "*":
                write_httplog(packet, url, queue)
                write_httplog(packet, payload, queue)            
    return processor

def get_referer(packet):
    return packet[HTTPRequest].Referer

def get_method(packet):
    return packet[HTTPRequest].Method

def get_cookie(packet):
    try:
        return packet[HTTPRequest].Cookie.decode("utf-8")
    except Exception as e:
        print("[!] %s" % e)
        return ""

def get_ua(packet):
    try:
        return getattr(packet[HTTPRequest], 'User_Agent').decode("utf-8")
    except Exception as e:
        print("[!] %s" % e)
        return ""

def get_content_type(packet):
    try:
        return getattr(packet[HTTPRequest], 'Content_Type').decode("utf-8")
    except Exception as e:
        print("[!] %s" % e)
        pass

def get_longurl(packet):
    return packet[HTTPRequest].Host + packet[HTTPRequest].Path

def get_payload(packet):
    if packet.haslayer(Raw):
        return packet[Raw].load
    else:
        return bytearray()

""" mode: GET, POST, * """
def run(sniffMode, iface, queue):
    global mode
    mode = sniffMode
    print("[*] Starting HTTPSensor Engine...")
    sniff_packet(iface, queue)

