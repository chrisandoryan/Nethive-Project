from scapy.all import *
from scapy.layers.http import *
import time
import os
import settings
import json

from processors import sql_tokenizer
from processors import xss_watcher
from parsers import slog_parser

from utils import OutputHandler, QueueHashmap

HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
mode = None

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- (hopefully) Thread-safe request-to-response storage
quehash = QueueHashmap()

def sniff_packet(interface):
    sniff(iface=interface, store=False, prn=process_packets(), session=TCPSession)

def write_httplog(packet, buffer):
    global HTTP_LOG_PATH, outHand

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
        outHand.sendLog(json.dumps(s))
        with open(HTTP_LOG_PATH, 'a') as f:
            f.writelines(json.dumps(s) + "\n")
        return    

# https://gist.github.com/thepacketgeek/6876699
def process_packets():
    def processor(packet):
        global mode

        src, dst = get_ip_port(packet)
        ip_src, tcp_sport = src
        ip_dst, tcp_dport = dst

        if packet.haslayer(HTTPRequest):
            # print(packet[HTTPRequest].show())
            url = packet[HTTPRequest].Path
            payload = get_payload(packet)

            if mode == "GET":
                write_httplog(packet, url)
            elif mode == "POST":
                write_httplog(packet, payload)
            elif mode == "*":
                write_httplog(packet, url)
                write_httplog(packet, payload)        

            xss_watcher.inspect([url, payload])
            quehash.set(ip_src, tcp_sport, packet)

        if packet.haslayer(HTTPResponse):
            # print(packet[HTTPResponse].show())
            rqst_pkt = quehash.pop(ip_dst, tcp_dport)
            body = get_payload(packet)
            xss_watcher.domparse(body, rqst_pkt, False)

    return processor

def get_referer(packet):
    return packet[HTTPRequest].Referer

def get_method(packet):
    return packet[HTTPRequest].Method

def get_cookie(packet):
    try:
        return packet[HTTPRequest].Cookie.decode("utf-8")
    except Exception as e:
        outHand.warning("[!] %s" % e)
        return ""

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

def get_content_type(packet):
    try:
        return getattr(packet[HTTPRequest], 'Content_Type').decode("utf-8")
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

""" mode: GET, POST, * """
def run(sniffMode, iface):
    global mode, outHand
    mode = sniffMode
    outHand.info("[*] Starting HTTPSensor Engine...")
    sniff_packet(iface)

