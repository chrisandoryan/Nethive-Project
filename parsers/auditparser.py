from utils import tail
import os

def main():
    AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH")

    logfile = open(AUDIT_LOG_PATH, 'r')
    loglines = tail(logfile)

    print("[*] Starting AuditParser Engine...")

if __name__ == '__main__':
    main()