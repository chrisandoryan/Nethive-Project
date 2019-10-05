import time
import requests
import sys

def tail(logfile):
    logfile.seek(0, 2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.01)
            continue
        yield line

def send_request(url, payload, method):
    s = requests.Session()
    cookie = {
        "PHPSESSID": "6i865obsioa6a1q609q1fb543h",
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


    
