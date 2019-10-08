import settings
from utils import tail

def run():
    print("[*] Starting BashParser Engine...")
    logfile = open("", 'r')
    loglines = tail(logfile)
    return

if __name__ == "__main__":
    run()