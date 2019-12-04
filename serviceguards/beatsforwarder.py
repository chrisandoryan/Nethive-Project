import subprocess
import utils
import os

proc = None

BEATS_FORWARDER_DIRECTORY = os.getcwd() + "/thirdparties/beats-forwarder/"

def run():
    print("[beats-forwarder] Starting beats-forwarder binary...")
    print("[beats-forwarder] Reading configuration from {}".format(BEATS_FORWARDER_DIRECTORY))
    proc = subprocess.call("./beats-forwarder -c etc/config.yml", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=BEATS_FORWARDER_DIRECTORY, universal_newlines=True)
    print("[beats-forwarder] Started.")

def stop():
    if proc:
        print("[beats-forwarder] Stopping beats-forwarder binary...")
        proc.kill()
        print("[beats-forwarder] Stopped.")