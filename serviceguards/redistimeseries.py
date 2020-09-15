import subprocess
import utils

proc = None

def run():
    print("[Redis] Starting redis-timeseries docker...")
    proc = subprocess.Popen("docker run -d --name redis_ts -p 6379:6379 -it --rm redislabs/redistimeseries:1.2.4", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8', bufsize=1, universal_newlines=True)
    utils.bufferOutput(proc)
    print("[Redis] Started.")
    proc.stdout.close()

def stop():
    print("[Redis] Stopping redis-timeseries...")
    proc = subprocess.Popen("docker kill redis_ts", stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True, encoding='utf-8', bufsize=1,universal_newlines=True)
    print("[Redis] Stopped.")

