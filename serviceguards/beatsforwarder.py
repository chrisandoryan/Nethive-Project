import subprocess
import utils
import os
import threading

proc = None

BEATS_FORWARDER_DIRECTORY = os.getcwd() + "/thirdparties/beats-forwarder/"

def checkAlive(process):
    while True:
        if process.poll() is not None: # process is dead
            print("[beats-forwarder] Detected beats-forwarder is dead.")
            run()
            break
        return True

def run():
    print("[beats-forwarder] Starting beats-forwarder binary...")
    print("[beats-forwarder] Reading configuration from {}".format(BEATS_FORWARDER_DIRECTORY))
    proc = subprocess.Popen("./beats-forwarder -c etc/config.yml", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=BEATS_FORWARDER_DIRECTORY, encoding='utf-8', bufsize=1, universal_newlines=True)
    utils.bufferOutput(proc, 3)    
    print("[beats-forwarder] Started.")
    # proc.stdout.close()
    threading.Thread(target=checkAlive, args=(proc,)).start()

def stop():
    if proc:
        print("[beats-forwarder] Stopping beats-forwarder binary...")
        proc.kill()
        print("[beats-forwarder] Stopped.")