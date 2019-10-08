import MySQLdb
import os
import shutil
import subprocess
import settings
import yaml

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
    """ 
    Setup configuration for Filebeat, log shipper.
    Changes:
        - filebeat.yml
        - filebeat service restart
    """
    FILEBEAT_CONFIG_PATH = os.getenv("FILEBEAT_CONFIG_PATH")
    os.rename(FILEBEAT_CONFIG_PATH, FILEBEAT_CONFIG_PATH + ".original")
    shutil.copy("./activators/config/filebeat.yml", FILEBEAT_CONFIG_PATH)
    subprocess.call(['service', 'filebeat', 'restart'])
    return

def logstash():
    """ 
    Setup configuration for dockerized Logstash (docker-elk).
    Changes:
        - logstash.conf
        - docker-elk reload and restart
    """
    DOCKER_ELK_REPO_PATH = os.getenv("DOCKER_ELK_REPO_PATH")
    LOGSTASH_CONFIG_PATH = DOCKER_ELK_REPO_PATH + '/logstash/pipeline/logstash.conf'
    os.rename(LOGSTASH_CONFIG_PATH, LOGSTASH_CONFIG_PATH + ".original")
    shutil.copy("./activators/config/logstash.conf", LOGSTASH_CONFIG_PATH)
    subprocess.Popen(["docker-compose", "up"], cwd=DOCKER_ELK_REPO_PATH)
    return

def killswitch():
    """ 
    Invoke reset for ELK system, turning off SIEM.
    Changes:
        - All engine will be offline
    """
    DOCKER_ELK_REPO_PATH = os.getenv("DOCKER_ELK_REPO_PATH")
    subprocess.Popen(["docker-compose", "down", "-v"], cwd=DOCKER_ELK_REPO_PATH)
    return

def bash():
    """ 
    Setup configuration for BashHistory module.
    Changes:
        - .bashrc of targeted users
    """
    f = open('./activators/config/historians.yaml', 'r')
    config = yaml.load(f.read())
    print(config)


def all():
    depman()
    slog()
    audit()
    filebeat()
    bash()
    logstash()
    return

if __name__ == "__main__":
    bash()