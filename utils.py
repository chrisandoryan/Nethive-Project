from bs4 import BeautifulSoup
import csv
import time
import requests
import sys
import queue
from collections import defaultdict
import urllib
import re

# class QueueHashmap(queue.Queue):
#     def __init__(self, maxsize=65535):
#         super().__init__(maxsize)
#         self._store = defaultdict(lambda: defaultdict(list))
#     def get_queue(self, key):
#         return self._store.get(key, [])
#     def pop(self, key, subkey):
#         queue = self.get_queue(key)
#         if queue:
#             return queue[subkey].pop()
#         return None
#     def set(self, key, subkey, item):
#         self._store[key][subkey].insert(0, item)
#         return self._store[key][subkey]

# class OutputHandler:
#     __instance = None
#     loggerQueue = queue.Queue()
#     outerrQueue = queue.Queue()
#     @staticmethod
#     def getInstance():
#         """ Static access method. """
#         if OutputHandler.__instance == None:
#             OutputHandler()
#         return OutputHandler.__instance
#     def __init__(self):
#         """ Virtually private constructor. """
#         if OutputHandler.__instance != None:
#             # print("OutputHandler is a singleton!")
#             pass
#         else:
#             OutputHandler.__instance = self
#     # --- Helper function to create multiple output types
#     def success(self, buffer):
#         self.outerrQueue.put(buffer.strip())
#         return
#     def info(self, buffer):
#         self.outerrQueue.put(buffer.strip())
#         return
#     def warning(self, buffer):
#         self.outerrQueue.put(buffer.strip())
#         return
#     def sendLog(self, buffer):
#         self.loggerQueue.put(buffer.strip())
#         return


def tail(logfile):
    logfile.seek(0, 2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.01)
            continue
        yield line


def login_dvwa():
    url = "http://192.168.137.220/DVWA/login.php"
    req = requests.get(url)
    print(req.headers)
    session_id = re.match("PHPSESSID=(.*?);", req.headers["set-cookie"])
    session_id = session_id.group(1)
    print("[X] Session_id: " + session_id)
    cookie = {"PHPSESSID": session_id}
    soup = BeautifulSoup(req.text, "html.parser")
    user_token = soup.find("input", {"name": "user_token"})["value"]
    print("[X] User_token: " + user_token + "\n")
    payload = {"username": "admin",
               "password": "password",
               "Login": "Login",
               "user_token": user_token}
    req_login = requests.post(url, payload, cookies=cookie, allow_redirects=False)
    result = req_login.headers["Location"]
    if "index.php" in result:
        return session_id
    else:
        print("Failed.")
        return

def send_request(url, payload, method, sessid):
    if sessid == '':
        sessid = login_dvwa()

    s = requests.Session()
    cookie = {
        "PHPSESSID": sessid,
        "security": "low"
    }
    if method == "GET":
        res = s.get(url, params=payload, cookies=cookie, allow_redirects=False)
    elif method == "POST":
        res = s.post(url, data=payload, cookies=cookie, allow_redirects=False)
    print(res.status_code)


def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x


def decode_deeply(data):
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, dict):
        return dict(map(decode_deeply, data.items()))
    if isinstance(data, tuple):
        return tuple(map(decode_deeply, data))
    if isinstance(data, list):
        return list(map(decode_deeply, data))
    return data


def bufferOutput(process, max_line=0):
    line_count = 0
    while True:
        out = process.stdout.readline()
        if not out:
            break
        else:
            sys.stdout.write(out.rstrip() + "\r\n")
            line_count += 1
        if max_line == 0:
            pass
        elif line_count >= max_line:
            break


def checkProcess(process):
    while True:
        if process.poll() != None:  # process is dead
            return False
        return True

def replay_xss_payload_dataset():
    print("Replaying XSS Payload dataset from https://github.com/pgaijin66/XSS-Payloads/blob/master/payload.txt")

    target = 'http://192.168.137.220/DVWA/vulnerabilities/xss_r/'
    param_name = 'name'

    payloads = open('/home/sh/Documents/Research/Testing/MaliciousFormattedPayload.log', 'r', encoding="ISO-8859-1").readlines()

    send_count = 0
    
    sessid = login_dvwa()
    for data in payloads:
        x = data.split('#', 1)
        idx = x[0]
        payload = x[1]
        print(x)
        send_request(target, {param_name: payload, 'index': idx, 'Submit': 'Submit'}, "GET", sessid)
        send_count += 1
        time.sleep(1)
    
    print("Sent %d MALICIOUS requests." % send_count)

def replay_sqli_normal_dataset():
    print("Replaying SQLi Payload dataset from https://github.com/Scott-Park/MachineLearning/blob/master/Sql-Injection/source/trainingdata/plain.txt")

    target = 'http://192.168.137.220/DVWA/vulnerabilities/sqli/'
    param_name = 'id'

    payloads = open('/home/sh/Documents/Research/Testing/NormalSQLiPayload.txt', 'r').readlines()

    send_count = 0
    
    sessid = login_dvwa()

    for data in payloads:
        print(data)
        send_request(target, {param_name: data, 'Submit': 'Submit'}, "GET", sessid)
        send_count += 1
        time.sleep(1.5)
    
    print("Sent %d MALICIOUS requests." % send_count)


def replay_csic_dataset(mode):  # mode is either GET or POST
    print("Replaying %s packets from CSIC2010 Dataset\n" % mode)
    target = 'http://192.168.137.220/DVWA/vulnerabilities/xss_r/'
    param_name = 'name'
    
    dataset = open(
        "/home/sh/Documents/Research/Testing/httpcsic2010dataset.csv", "r")
    csv_reader = csv.reader(dataset, delimiter=',')

    sessid = login_dvwa()

    line_count = 0
    send_count = 0
    for row in csv_reader:
        if line_count == 0:
            # print(' '.join(row)) # Uncomment to print headers
            line_count += 1
        else:
            if row[17].strip() == mode:
                raw_payload = urllib.parse.unquote_plus(row[16].strip())
                payload = dict(re.findall(
                    r'(\S+)=(".*?"|\S+)', str(raw_payload)))
                if payload:
                    print(payload[list(payload.keys())[0]])
                    send_request(target, {param_name: payload[list(payload.keys())[0]], 'index':'NaN', 'Submit': 'Submit'}, row[1], sessid)
                    send_count += 1
                    with open('/tmp/NormalPayload.log', 'a+') as f:
                        f.write(payload[list(payload.keys())[0]] + '\n')
                    time.sleep(1)
            line_count += 1
            if send_count >= 480:
                print("Sent %d NORMAL requests." % send_count)
                return

    print("Finished sending %d requests" % send_count)
