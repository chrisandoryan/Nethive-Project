import settings
from utils import tail

def run(username):
    BASHRC_PATH = "/home/%s/.bash_history" % username
    print("[*] Starting BashParser Engine...")
    
    logfile = open(BASHRC_PATH, 'r')
    loglines = tail(logfile)
    for l in loglines:
        print(l.strip())
        
    return

if __name__ == "__main__":
    run()