import scapy.all as scapy
from scapy_http import http
import argparse
import json
import csv
import time

from processors import sqltokenize
from parsers import slogparser

count = 1
mode = None

def sniff_packet(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packets)

def process_packets(packet):
    global count, mode
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        request_method = get_method(packet)
        load = get_payload(packet)
        cookie = get_cookie(packet)
        user_agent = get_ua(packet)
        content_type = get_content_type(packet)
        referer = get_referer(packet)
        
        inbound = url if mode is "GET" else load
        timestamp = int(time.time())
        
        for s in sqltokenize.tokenize(inbound):
            s['request_method'] = request_method.decode("utf-8")
            s['user_agent'] = user_agent.decode("utf-8")
            # if (args.label_normal):
            #     s['label'] = 'normal'
            #     s['technique'] = 'normal'
            # elif (args.label_threat):
            #     s['label'] = 'threat'
            # if (args.technique):
            #     s['technique'] = args.technique
            # with open('data_temp/{}.json'.format('GET_http' if args.get else 'POST_http'), 'a') as f:
            #     f.write(json.dumps(s) + "\n")
            with open('data_temp/{}.csv'.format('GET_http' if args.get else 'POST_http'), 'a') as f:
                # convert {0: 1.5, 1: 2.2, ...} to [1.5, 2.2, ...] to 1.5 2.2, ...
                s['centrality'] = ' '.join(map(str, list(s['centrality'].values())))
                s['timestamp'] = timestamp
                writer = csv.writer(f)
                # writer.writerow(list(s.keys()))
                writer.writerow(list(s.values()))
            count += 1


def get_referer(packet):
    return packet[http.HTTPRequest].Referer


def get_method(packet):
    return packet[http.HTTPRequest].Method


def get_cookie(packet):
    return packet[http.HTTPRequest].Cookie


def get_ua(packet):
    return getattr(packet[http.HTTPRequest], 'User-Agent')


def get_content_type(packet):
    return getattr(packet[http.HTTPRequest], 'Content-Type')


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_payload(packet):
    if packet.haslayer(scapy.Raw):
        return packet[scapy.Raw].load

""" mode: GET, POST, * """
def run(mode):
    print("Listening...")
    sniff_packet('lo', mode)
