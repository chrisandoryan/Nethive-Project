import settings
import os
from utils import tail
# from utils import OutputHandler

CENTRALIZED_BASH_HISTORY_PATH = os.getenv("CENTRALIZED_BASH_HISTORY_PATH")

# --- Handle output synchronization
# outHand = OutputHandler.getInstance()

def run():
    print("[BashParser] Starting BashParser Engine...")
    logfile = open(CENTRALIZED_BASH_HISTORY_PATH, 'a+')
    # loglines = tail(logfile)
    # for l in loglines:
    #     outHand.sendLog(l.strip())
    return

if __name__ == "__main__":
    run()