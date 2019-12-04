import subprocess
import utils

proc = None

def run():
    print("[ELKStack] Initiating docker-elk container...")
    proc = subprocess.Popen("docker-compose -f thirdparties/docker-elk/docker-compose.yml up -d", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8', bufsize=1, universal_newlines=True)
    utils.bufferOutput(proc)
    print("[ELKStack] Done.")
    proc.stdout.close()

def stop():
    print("[ELKStack] Stopping docker-elk container...")
    proc = subprocess.Popen("docker-compose -f thirdparties/docker-elk/docker-compose.yml down", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8', bufsize=1, universal_newlines=True)
    utils.bufferOutput(proc)
    print("[ELKStack] Stopped.")
    proc.stdout.close()

