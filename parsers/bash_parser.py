import settings
import os
from utils import tail

CENTRALIZED_BASH_HISTORY_PATH = os.getenv("CENTRALIZED_BASH_HISTORY_PATH")

def run(logQueue, outQueue):
    outQueue.put("[*] Starting BashParser Engine...")
    logfile = open(CENTRALIZED_BASH_HISTORY_PATH, 'a+')
    loglines = tail(logfile)
    for l in loglines:
        logQueue.put(l.strip())
        
    return

if __name__ == "__main__":
    run()