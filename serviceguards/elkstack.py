import subprocess
import utils

proc = None

def run():
    print("[ELKStack] Initiating docker-elk container...")
    proc = subprocess.call("docker-compose -f thirdparties/docker-elk/docker-compose.yml up -d", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    # utils.bufferOutput(proc)
    print("[ELKStack] Done.")

def stop():
    print("[ELKStack] Stopping docker-elk container...")
    proc = subprocess.call("docker-compose -f thirdparties/docker-elk/docker-compose.yml down", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    # utils.bufferOutput(proc)
    print("[ELKStack] Stopped.")

