import socket
import json
import html
from urllib.parse import unquote, unquote_plus
import os
import time
import traceback
import logging

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

# Matching Algorithm. 
# Before searching for scripts in the
# HTTP request, the filter transforms the URL request (and
# any POST data) as follows:
# 1. URL decode (e.g., replace %41 with A). This step mimics the URL decoding that the server does when receiving an HTTP request (e.g., before PHP returns
# the value of $_GET["q"]).
# 2. Character set decode (e.g., replace UTF-7 code points
# with Unicode characters). This step mimics a transformation done by the HTML tokenizer.
# 3. HTML entity decode (e.g., replace &amp; with &). The
# filter applies this transformation only to some of the
# interception points. For example, inline scripts are not
# entity decoded but inline event handlers are.
# http://www.collinjackson.com/research/xssauditor.pdf

WATCHMAN_HOST = '127.0.0.1'
WATCHMAN_PORT = 5127

XSS_WATCHMAN_SOCKET = os.getenv("XSS_WATCHMAN_SOCKET")

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_PORT'))

# xss_logger = logging.getLogger('xss_audit_logger')
# xss_logger.setLevel(logging.INFO)
# xss_logger.addHandler(AsynchronousLogstashHandler(LOGSTASH_HOST, LOGSTASH_PORT, database_path='xss_audit_log.db'))

def send_to_logstash(message):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        tcp_socket.sendall((json.dumps(message) + "\n").encode())
        tcp_socket.close()
    except Exception as e:
        print("[XSS Watcher] %s" % e)
        logger.exception(e)
    return

def send_to_watchman(the_package):
    if os.path.exists(XSS_WATCHMAN_SOCKET):
        try:
            unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            unix_socket.connect(XSS_WATCHMAN_SOCKET)
            unix_socket.sendall(json.dumps(the_package).encode())
            result = unix_socket.recv(4096)
            unix_socket.close()
            return result
        except Exception as e:
            print("[XSS Watcher] %s" % e)
            logger.exception(e)
    else:
        print("[XSS_Watcher] No socket file on %s" % XSS_WATCHMAN_SOCKET)

def package_transform(the_package):
    for key, value in the_package.items():
        if isinstance(value, dict):
            the_package[key] = package_transform(value)
        else:
            if isinstance(value, list) or isinstance(value, int):
                continue;
            if value != None:
                value = unquote(value) # 1.1 URL Decode
                value = unquote_plus(value) # 1.2 URL Decode Plus Sign (is this neccessary?)
                value = value # 2. Character-Set Decode
                value = html.unescape(value) # 3. HTML Entity Decode
                the_package[key] = value

    return the_package

def domparse(the_package, is_flagged_xss):
    """
        Send HTTP Response to DOM Parser to detect XSS
    """

    the_package['res_body'] = the_package['res_body'].decode('ISO-8859-1')
    the_package = package_transform(the_package)

    try:
        print("[XSS Watcher] Auditing the package...")
        result = send_to_watchman(the_package)
        if result:
            result = json.loads(result)

            message = {'parsed_log': result, 'log_type': 'TYPE_XSS_AUDITOR'}
            # send_to_logstash(message) # uncomment to store the result in its own index in elasticsearch

            print("[XSS Watcher] Finished.")
            
            return result
    except Exception as e:
        print("[XSS Watcher] %s" % e)
        logger.exception(e)
    return {}

def inspect(arr_buff):
    """
        Check HTTP Request content for potential XSS payload (static analysis)
    """
    # for buff in arr_buff:
    #     print(buff)

    return

if __name__ == "__main__":
    pass