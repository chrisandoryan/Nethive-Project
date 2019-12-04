import subprocess
import utils
import os
import settings
import threading

proc = None

def checkAlive(process):
    while True:
        print(process.poll())
        if process.poll() is not None: # process is dead
            print("[XSSAuditor] Detected XSS Auditor engine is dead.")
            run()
            break
        return True

def run():
    print("[XSSAuditor] Starting XSS Auditor engine...")
    try:
        os.remove(os.getenv("XSS_WATCHMAN_SOCKET"))
    except OSError:
        pass
    proc = subprocess.Popen("./processors/xss_auditor/xss_auditor", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8', bufsize=1, universal_newlines=True)
    utils.bufferOutput(proc, 1)
    print("[XSSAuditor] Started.")
    # proc.stdout.close()
    threading.Thread(target=checkAlive, args=(proc,)).start()

def stop():
    if proc:
        print("[XSSAuditor] Stopping XSS Auditor engine...")
        proc.kill()
        print("[XSSAuditor] Stopped.")