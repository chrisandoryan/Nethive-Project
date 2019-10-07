import MySQLdb
import os
import shutil
import subprocess
import settings

def depman():
    DOCKER_ELK_REPO_PATH = os.getenv("DOCKER_ELK_REPO_PATH")
    subprocess.call(['/bin/bash', './activators/depman.sh', DOCKER_ELK_REPO_PATH])
    return

def slog():
    db = MySQLdb.connect(os.getenv("MYSQL_HOSTNAME"),os.getenv("MYSQL_USER"),os.getenv("MYSQL_PASS"),os.getenv("MYSQL_DB"))
    cursor = db.cursor()
    for line in open("./activators/config/slog.sql"):
        cursor.execute(line)
    db.close()
    return

def audit():
    AUDIT_RULES_PATH = os.getenv("AUDIT_RULES_PATH")
    os.rename(AUDIT_RULES_PATH, AUDIT_RULES_PATH + ".original")
    shutil.copy("./activators/config/audit.rules", AUDIT_RULES_PATH)
    subprocess.call(['service', 'auditd', 'restart'])
    return

def filebeat():
    FILEBEAT_CONFIG_PATH = os.getenv("FILEBEAT_CONFIG_PATH")
    os.rename(FILEBEAT_CONFIG_PATH, FILEBEAT_CONFIG_PATH + ".original")
    shutil.copy("./activators/config/filebeat.yml", FILEBEAT_CONFIG_PATH)
    subprocess.call(['service', 'filebeat', 'restart'])
    return

def logstash():
    DOCKER_ELK_REPO_PATH = os.getenv("DOCKER_ELK_REPO_PATH")
    LOGSTASH_CONFIG_PATH = DOCKER_ELK_REPO_PATH + '/logstash/pipeline/logstash.conf'
    os.rename(LOGSTASH_CONFIG_PATH, LOGSTASH_CONFIG_PATH + ".original")
    shutil.copy("./activators/config/logstash.conf", LOGSTASH_CONFIG_PATH)
    subprocess.Popen(["docker-compose", "up"], cwd=DOCKER_ELK_REPO_PATH)

def killswitch():
    DOCKER_ELK_REPO_PATH = os.getenv("DOCKER_ELK_REPO_PATH")
    subprocess.Popen(["docker-compose", "down", "-v"], cwd=DOCKER_ELK_REPO_PATH)

def all():
    # depman()
    slog()
    audit()
    filebeat()
    logstash()
    return

if __name__ == "__main__":
    slog()