from scapy.all import *
from scapy.layers.http import *
import time
import os
import settings

from processors import sql_tokenizer
from parsers import slogparser

HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
mode = None

def sniff_packet(interface):
    sniff(iface=interface, store=False, prn=process_packets, session=TCPSession)

def write_httplog(packet, buffer):
    global HTTP_LOG_PATH
    # print(packet[HTTPRequest].show())

    cookie = packet[HTTPRequest].Cookie
    user_agent = getattr(packet[HTTPRequest], 'User_Agent')
    content_type = getattr(packet[HTTPRequest], 'Content_Type')
    referer = packet[HTTPRequest].Referer
    request_method = packet[HTTPRequest].Method
    host = packet[HTTPRequest].Host

    try:
        ip = packet[IP].src
    except Exception as e:
        print("[!] %s" % e)
        ip = ""

    timestamp = int(time.time())

    for s in sql_tokenizer.tokenize(buffer):
        s['cookie'] = cookie.decode("utf-8")
        s['source_address'] = ip
        s['request_method'] = request_method.decode("utf-8")
        s['user_agent'] = user_agent.decode("utf-8")
        s['centrality'] = ' '.join(map(str, list(s['centrality'].values())))
        s['host'] = host.decode("utf-8")
        s['timestamp'] = timestamp
        with open(HTTP_LOG_PATH, 'a') as f:
            print(s)
        return    

def process_packets(packet):
    global mode
    if packet.haslayer(HTTPRequest):
        url = packet[HTTPRequest].Path
        payload = get_payload(packet)
        if mode is "GET":
            write_httplog(packet, url)
        elif mode is "POST":
            write_httplog(packet, payload)
        elif mode is "*":
            write_httplog(packet, url)
            write_httplog(packet, payload)            
    return

def get_referer(packet):
    return packet[HTTPRequest].Referer

def get_method(packet):
    return packet[HTTPRequest].Method

def get_cookie(packet):
    return packet[HTTPRequest].Cookie

def get_ua(packet):
    return getattr(packet[HTTPRequest], 'User_Agent')

def get_content_type(packet):
    return getattr(packet[HTTPRequest], 'Content_Type')

def get_url(packet):
    return packet[HTTPRequest].Host + packet[HTTPRequest].Path

def get_payload(packet):
    if packet.haslayer(Raw):
        return packet[Raw].load
    else:
        return bytearray()

""" mode: GET, POST, * """
def run(sniffMode):
    global mode
    mode = sniffMode
    print("[*] Starting HTTPSensor Engine...")
    sniff_packet('lo')

