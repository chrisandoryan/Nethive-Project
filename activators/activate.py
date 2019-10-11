import MySQLdb
import os
import shutil
import subprocess
import settings
import yaml
from string import Template
import re
from utils import OutputHandler

DOCKER_ELK_REPO_PATH = os.getenv("DOCKER_ELK_REPO_PATH")
AUDIT_RULES_PATH = os.getenv("AUDIT_RULES_PATH")
AUDITBEAT_RULES_PATH = os.getenv("AUDITBEAT_RULES_PATH")
FILEBEAT_CONFIG_PATH = os.getenv("FILEBEAT_CONFIG_PATH")
AUDITBEAT_CONFIG_PATH = os.getenv("AUDITBEAT_CONFIG_PATH")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH")
MSQL_SLOW_QUERY_LOG_PATH = os.getenv("MYSQL_SLOW_QUERY_LOG_PATH")
HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
CENTRALIZED_BASH_HISTORY_PATH = os.getenv("CENTRALIZED_BASH_HISTORY_PATH")

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- Helper methods

def replConfigFile(original, modified):
    if not os.path.exists(original + ".original"):
        os.rename(original, original + ".original")
    shutil.copy(modified, original)

def bufferOutput(process):
    while True:
        out = process.stdout.readline()
        outHand.info(out.decode("utf-8"))
        if not out: break

# --- End of Helper methods

def depman():
    depman = subprocess.call(['/bin/bash', './activators/depman.sh', DOCKER_ELK_REPO_PATH])
    return

def slog():
    db = MySQLdb.connect(os.getenv("MYSQL_HOSTNAME"),os.getenv("MYSQL_USER"),os.getenv("MYSQL_PASS"),os.getenv("MYSQL_DB"))
    cursor = db.cursor()
    for line in open("./activators/config/slog.sql"):
        cursor.execute(line)
    db.close()
    return

def audit():
    replConfigFile(AUDIT_RULES_PATH, "./activators/config/audit.rules")
    # os.rename(AUDIT_RULES_PATH, AUDIT_RULES_PATH + ".original")
    # shutil.copy("./activators/config/audit.rules", AUDIT_RULES_PATH)
    subprocess.call(['service', 'auditd', 'restart'])
    return

def filebeat():
    """ 
    Setup configuration for Filebeat, log shipper.
    Changes:
        - filebeat.yml
        - filebeat service restart
    """
    replConfigFile(FILEBEAT_CONFIG_PATH, "./activators/config/filebeat.yml")
    # os.rename(FILEBEAT_CONFIG_PATH, FILEBEAT_CONFIG_PATH + ".original")
    # shutil.copy("./activators/config/filebeat.yml", FILEBEAT_CONFIG_PATH)
    subprocess.call(['service', 'filebeat', 'restart'])
    return

def auditbeat():
    """ 
    Setup configuration for Auditbeat.
    Changes:
        - auditbeat.yml
        - auditbeat service restart
    """
    replConfigFile(AUDITBEAT_CONFIG_PATH, "./activators/config/auditbeat.yml")
    shutil.copy("./activators/config/auditbeat.rules", AUDITBEAT_RULES_PATH)

    subprocess.call(['service', 'auditbeat', 'restart'])
    return

def logstash():
    """ 
    Setup configuration for dockerized Logstash (docker-elk).
    Changes:
        - logstash.conf
        - docker-elk reload and restart
    """
    LOGSTASH_CONFIG_PATH = DOCKER_ELK_REPO_PATH + '/logstash/pipeline/logstash.conf'
    LOGSTASH_DOCKERFILE_PATH = DOCKER_ELK_REPO_PATH + '/logstash/Dockerfile'

    replConfigFile(LOGSTASH_CONFIG_PATH, "./activators/config/logstash.conf")
    # os.rename(LOGSTASH_CONFIG_PATH, LOGSTASH_CONFIG_PATH + ".original")
    # shutil.copy("./activators/config/logstash.conf", LOGSTASH_CONFIG_PATH)

    replConfigFile(LOGSTASH_DOCKERFILE_PATH, "./activators/config/Dockerfile.logstash")
    # os.rename(LOGSTASH_DOCKERFILE_PATH, LOGSTASH_DOCKERFILE_PATH + ".original")
    # shutil.copy("./activators/config/Dockerfile.logstash", LOGSTASH_DOCKERFILE_PATH)
    return

def killswitch():
    """ 
    Invoke reset for ELK system, turning off SIEM engine.
    Changes:
        - All configurations will be reverted back to original
        - All engines will be offline
    """
    return

def bash():
    """ 
    Setup configuration for BashHistory module.
    Changes:
        - .bashrc of targeted users
    """
    f = open('./activators/config/historians.yaml', 'r')
    config = yaml.load(f.read())
    f.close()
    for u in config['users']:
        BASHRC_PATH = "/home/%s/.bashrc" % u['username']
        # os.rename(BASHRC_PATH, BASHRC_PATH + ".original")
        template = open('./activators/config/.bashrc', 'r')
        t = Template(template.read())
        config = t.safe_substitute(
            HISTSIZE=1000,
            HISTIGNORE='"ls:ps:history"',
            HISTCONTROL='"ignorespace:erasedups"',
            HISTTIMEFORMAT='"%y-%h-%d %H:%M:%S "'
        )
        pattern = re.compile(r'# --- Plug by SIEM, Do Not MODIFY.*# --- End of Plug', re.DOTALL)
        with open(BASHRC_PATH, 'a+') as bashrc:
            b = re.sub(pattern, '', bashrc.read())
            b = b + config
            bashrc.writelines(b)

        # "$(whoami)@$([ \"$SSH_CONNECTION\" == \"\" ] && echo \"local\" || echo $SSH_CONNECTION | awk '{print $1}')"
        
        # if 'force_append' in u and u['force_append']:
        #     if "PROMPT_COMMAND" in os.environ:
        #         f.writelines("PROMPT_COMMAND='$PROMPT_COMMAND; history -a'")                
        #     else:
        #         f.writelines("PROMPT_COMMAND='history -a'")
        # if 'hist_size' in u:
        #     f.writelines("export HISTSIZE=%d" % u['hist_size'])
        # if 'with_datetime' in u and u['with_datetime']:
        #     f.writelines("export HISTTIMEFORMAT=\"%h %d %H:%M:%S \"")
        # if 'exclude_commands' in u and u['exclude_commands']:
        #     f.writelines("export HISTIGNORE=\"%s\"" % ':'.join(u['exclude_commands']))
        
        # subprocess.call(['source', BASHRC_PATH])

        template.close()

    return

def dirs():
    if not os.path.exists(AUDIT_LOG_PATH):
        os.makedirs(os.path.dirname(AUDIT_LOG_PATH))
    if not os.path.exists(MSQL_SLOW_QUERY_LOG_PATH):    
        os.makedirs(os.path.dirname(MSQL_SLOW_QUERY_LOG_PATH))
    if not os.path.exists(HTTP_LOG_PATH):
        os.makedirs(os.path.dirname(HTTP_LOG_PATH))
    if not os.path.exists(CENTRALIZED_BASH_HISTORY_PATH):
        os.makedirs(os.path.dirname(CENTRALIZED_BASH_HISTORY_PATH))

def elk():
    DOCKER_ELK_COMPOSE_PATH = DOCKER_ELK_REPO_PATH + 'docker-compose.yml'

    replConfigFile(DOCKER_ELK_COMPOSE_PATH, "./activators/config/docker-compose.yml")
    # os.rename(DOCKER_ELK_COMPOSE_PATH, DOCKER_ELK_COMPOSE_PATH + ".original")
    # shutil.copy("./activators/config/docker-compose.yml", DOCKER_ELK_COMPOSE_PATH)

    elkstack = subprocess.Popen(['/bin/bash', './activators/elkstack.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    bufferOutput(elkstack)

def configs():
    # outHand.info("[*] Initiating dependency manager...")
    # depman()
    outHand.info("[*] Creating directories...")
    dirs()
    outHand.info("[*] Configuring SQL Slow Query Log...")
    slog()
    outHand.info("[*] Activating auditd module...")
    audit()
    outHand.info("[*] Configuring filebeat module...")
    filebeat()
    outHand.info("[*] Configuring auditbeat module...")
    auditbeat()
    outHand.info("[*] Configuring bashparse module...")
    bash()
    outHand.info("[*] Configuring Logstash...")
    logstash()
    return

if __name__ == "__main__":
    bash()