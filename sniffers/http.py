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

from storage.memcache import MemCacheClient

HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
mode = None

unsafe_content_types = [
    "text/html",
    "image/svg+xml",
    "text/xml",
]

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- (hopefully) Thread-safe request-to-response storage. Memc is used for system wide storage
quehash = QueueHashmap()
memc = MemCacheClient().getInstance()

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
        outHand.sendLog(json.dumps(s))
        with open(HTTP_LOG_PATH, 'a+') as f:
            f.writelines(json.dumps(s) + "\n")
        return    

def wrap_for_auditor(packet):
    package = {
        "url": get_url_unidecoded(packet),
        "body": get_payload_unidecoded(packet),
    }
    return package

def get_mime_type(content_type):
    if content_type is None:
        return ['', '']
    content_type, *extra = content_type.split(';')
    return content_type, extra

# https://gist.github.com/thepacketgeek/6876699
def process_packets():
    def processor(packet):
        global mode

        src, dst = get_ip_port(packet)
        ip_src, tcp_sport = src
        ip_dst, tcp_dport = dst

        if packet.haslayer(HTTPRequest):
            # print(packet[HTTPRequest].show())
            url = get_url(packet)
            payload = get_payload(packet)

            if mode == "GET":
                write_httplog(packet, url)
            elif mode == "POST":
                write_httplog(packet, payload)
            elif mode == "*":
                write_httplog(packet, url)
                write_httplog(packet, payload)        

            xss_watcher.inspect([url, payload])
            req_data = quehash.set(ip_src, tcp_sport, wrap_for_auditor(packet))
            # print(req_data)
            # memc.set("structured", {"a": ("b", "c"), "a2": fractions.Fraction(1, 3)})



        if packet.haslayer(HTTPResponse):
            # print(packet[HTTPResponse].show())
            content_type = get_content_type(packet, HTTPResponse)
            if get_mime_type(content_type)[0] in unsafe_content_types:
                req_data = quehash.pop(ip_dst, tcp_dport)
                res_body = get_payload(packet)
                xss_watcher.domparse(res_body, req_data, False)

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
        return bytearray('')

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

""" mode: GET, POST, * """
def run(sniffMode, iface):
    global mode, outHand
    mode = sniffMode
    outHand.info("[*] Starting HTTPSensor Engine...")
    sniff_packet(iface)

