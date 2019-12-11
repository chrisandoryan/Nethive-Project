import subprocess
import utils

proc = None

def run():
    print("[Kafka] Initiating Kafka container...")
    proc = subprocess.Popen("docker-compose -f thirdparties/kafka-docker/docker-compose.yml up -d", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8', bufsize=1, universal_newlines=True)
    utils.bufferOutput(proc)
    print("[Kafka] Done.")
    proc.stdout.close()

def stop():
    print("[Kafka] Stopping Kafka container...")
    proc = subprocess.Popen("docker-compose -f thirdparties/kafka-docker/docker-compose.yml down", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8', bufsize=1, universal_newlines=True)
    utils.bufferOutput(proc)
    print("[Kafka] Stopped.")
    proc.stdout.close()

