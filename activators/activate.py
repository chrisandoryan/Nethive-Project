import MySQLdb
import os
import shutil
import subprocess
import settings

def slog():
    db = MySQLdb.connect(os.getenv("MYSQL_HOSTNAME"),os.getenv("MYSQL_USER"),os.getenv("MYSQL_PASS"),os.getenv("MYSQL_DB"))
    cursor = db.cursor()
    for line in open("./activators/slog.sql"):
        cursor.execute(line)
    db.close()
    return

def audit():
    AUDIT_RULES_PATH = os.getenv("AUDIT_RULES_PATH")
    
    os.rename(AUDIT_RULES_PATH, AUDIT_RULES_PATH + ".original")
    shutil.copy("./activators/audit.rules", AUDIT_RULES_PATH)
    subprocess.call(['service', 'auditd', 'restart'])
    return
    
def all():
    slog()
    audit()
    return

if __name__ == "__main__":
    slog()