import settings
import os
from utils import tail

CENTRALIZED_BASH_HISTORY_PATH = os.getenv("CENTRALIZED_BASH_HISTORY_PATH")

def run():
    print("[*] Starting BashParser Engine...")
    logfile = open(CENTRALIZED_BASH_HISTORY_PATH, 'a+')
    loglines = tail(logfile)
    for l in loglines:
        print(l.strip())
        
    return

if __name__ == "__main__":
    run()