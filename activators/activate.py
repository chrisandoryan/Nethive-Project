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
PACKETBEAT_CONFIG_PATH = os.getenv("PACKETBEAT_CONFIG_PATH")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH")
MSQL_SLOW_QUERY_LOG_PATH = os.getenv("MYSQL_SLOW_QUERY_LOG_PATH")
HTTP_LOG_PATH = os.getenv("HTTP_LOG_PATH")
CENTRALIZED_BASH_HISTORY_PATH = os.getenv("CENTRALIZED_BASH_HISTORY_PATH")
SQL_RESPONSE_LOG_PATH = os.getenv("SQL_RESPONSE_LOG_PATH")

# --- Handle output synchronization
outHand = OutputHandler().getInstance()

# --- Helper methods
def backupOriginalConf(original):
    if not os.path.exists(original + ".original"):
        os.rename(original, original + ".original")

def replConfigFile(original, modified):
    # For ELK Configuration, DO NOT COPY/CREATE BACKUP inside same directory!
    # backupOriginalConf(original)
    shutil.copy(modified, original)    

def copyTemplateFile(original, modified):
    # For ELK Configuration, backup original config file
    # then substitute in modified config file and place it in the original directory
    backupOriginalConf(original)
    with open(modified, 'r') as r:
        t = Template(r.read())
        new_conf = t.safe_substitute(LOGSTASH_HOST=os.getenv("LOGSTASH_HOST"))

        with open(original, 'w') as w:
            w.write(new_conf)

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

def audit(): # WILL BE REMOVED - NOT USED ANYMORE
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
    copyTemplateFile(FILEBEAT_CONFIG_PATH, "./activators/config/filebeat.yml")
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
    copyTemplateFile(AUDITBEAT_CONFIG_PATH, "./activators/config/auditbeat.yml")
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
    LOGSTASH_CONFIG_PATH = DOCKER_ELK_REPO_PATH + 'logstash/pipeline/logstash.conf'
    LOGSTASH_DOCKERFILE_PATH = DOCKER_ELK_REPO_PATH + 'logstash/Dockerfile'

    shutil.copy(LOGSTASH_CONFIG_PATH, "./activators/config/logstash.conf")
    # os.rename(LOGSTASH_CONFIG_PATH, LOGSTASH_CONFIG_PATH + ".original")
    # shutil.copy("./activators/config/logstash.conf", LOGSTASH_CONFIG_PATH)

    shutil.copy(LOGSTASH_DOCKERFILE_PATH, "./activators/config/Dockerfile.logstash")
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
    # sudo aa-remove-unknown
    # 
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
        os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
    if not os.path.exists(MSQL_SLOW_QUERY_LOG_PATH):    
        os.makedirs(os.path.dirname(MSQL_SLOW_QUERY_LOG_PATH), exist_ok=True)
    if not os.path.exists(SQL_RESPONSE_LOG_PATH):    
        os.makedirs(os.path.dirname(SQL_RESPONSE_LOG_PATH), exist_ok=True)
    if not os.path.exists(HTTP_LOG_PATH):
        os.makedirs(os.path.dirname(HTTP_LOG_PATH), exist_ok=True)
    if not os.path.exists(CENTRALIZED_BASH_HISTORY_PATH):
        os.makedirs(os.path.dirname(CENTRALIZED_BASH_HISTORY_PATH), exist_ok=True)

def memcache():
    # TODO: setup memcache configuration WILL BE REMOVED - NOT USED ANYMORE
    # apt install memcached php-memcached
    # copy /etc/memcached.conf to /etc/memcached.conf.orig
    # write custom configuration from ./config/memcached.conf into /etc/memcached.conf
    return

def redis():
    # TODO: create activator for redis server WILL BE REMOVED - NOT USED ANYMORE
    # sudo docker run -p 6379:6379 -it --rm redislabs/redistimeseries
    return

def packetbeat():
    """ 
    Setup configuration for Packetbeat, packet shipper.
    Changes:
        - packetbeat.yml
        - packetbeat service restart
    """
    replConfigFile(PACKETBEAT_CONFIG_PATH, "./activators/config/packetbeat.yml")
    subprocess.call(['service', 'packetbeat', 'restart'])
    return

def elk():
    DOCKER_ELK_COMPOSE_PATH = DOCKER_ELK_REPO_PATH + 'docker-compose.yml'

    replConfigFile(DOCKER_ELK_COMPOSE_PATH, "./activators/config/docker-compose.yml")
    # os.rename(DOCKER_ELK_COMPOSE_PATH, DOCKER_ELK_COMPOSE_PATH + ".original")
    # shutil.copy("./activators/config/docker-compose.yml", DOCKER_ELK_COMPOSE_PATH)

    # print("[*] Starting ELKStack...")
    # elkstack = subprocess.Popen(['/bin/bash', './activators/elkstack.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # bufferOutput(elkstack)

def fresh():
    print("[*] Installing required dependencies...")
    depman()
    print("Done.")
    print()
    print("[*] Setting up environment...")
    configs()
    return

def configs():
    print("[*] Creating required directories...")
    dirs()
    print("[*] Enabling MySQL Slow Query Log...")
    slog()
    print("[*] Configuring filebeat module...")
    filebeat()
    print("[*] Configuring auditbeat module...")
    auditbeat()
    print("[*] Configuring packetbeat module...")
    packetbeat()
    print("[*] Configuring bash \"historians\" module...")
    bash()
    print("[*] Updating docker-elk configuration...")
    elk()
    print("[*] Updating Logstash configuration...")
    logstash()

if __name__ == "__main__":
    pass