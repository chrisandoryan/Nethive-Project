import subprocess
import utils
import os
import settings

proc = None

def run():
    print("[XSSAuditor] Starting XSS Auditor engine...")
    os.remove(os.getenv("XSS_WATCHMAN_SOCKET"))
    proc = subprocess.Popen("./processors/xss_auditor/xss_auditor", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    utils.bufferOutput(proc, 2)
    print("[XSSAuditor] Started.")

def stop():
    if proc:
        print("[XSSAuditor] Stopping XSS Auditor engine...")
        proc.kill()
        print("[XSSAuditor] Stopped.")