from scapy.all import *
from scapy.layers.http import *
import time
import os

from processors import sql_tokenizer
from parsers import slogparser

HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
mode = None

def sniff_packet(interface):
    sniff(iface=interface, store=False, prn=process_packets, session=TCPSession)

def write_httplog(packet):
    print(packet[HTTPRequest].show())
    # request_method = get_method(packet)
    # load = get_payload(packet)
    # cookie = packet[HTTPRequest].Cookie
    # user_agent = getattr(packet[HTTPRequest], 'User-Agent')
    # content_type = getattr(packet[HTTPRequest], 'Content-Type')
    # referer = get_referer(packet)
    ip = packet[IP].src
    timestamp = int(time.time())
    # for s in sql_tokenizer.tokenize(buffer):
    #     s['request_method'] = request_method.decode("utf-8")
    #     s['user_agent'] = user_agent.decode("utf-8")
    #     s['centrality'] = ' '.join(map(str, list(s['centrality'].values())))
    #     s['timestamp'] = timestamp
    #     with open(HTTP_LOG_PATH, 'a') as f:
    #         # print(s)
    #         return    

def process_packets(packet):
    global mode
    if packet.haslayer(HTTPRequest):
        if mode is "GET":
            url = packet[HTTPRequest].Path
            write_httplog(packet, url)
        elif mode is "POST":
            payload = get_payload(packet)
            write_httplog(packet, payload)

def get_referer(packet):
    return packet[HTTPRequest].Referer

def get_method(packet):
    return packet[HTTPRequest].Method

def get_cookie(packet):
    return packet[HTTPRequest].Cookie

def get_ua(packet):
    return getattr(packet[HTTPRequest], 'User-Agent')

def get_content_type(packet):
    return getattr(packet[HTTPRequest], 'Content-Type')

def get_url(packet):
    return packet[HTTPRequest].Host + packet[HTTPRequest].Path

def get_payload(packet):
    if packet.haslayer(Raw):
        return packet[Raw].load

""" mode: GET, POST, * """
def run(reqMode):
    global mode
    mode = reqMode
    sniff_packet('ens33')
