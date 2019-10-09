import MySQLdb
import os
import shutil
import subprocess
import settings
import yaml
from string import Template

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
    # subprocess.Popen(["docker-compose", "up"], cwd=DOCKER_ELK_REPO_PATH)
    return

def killswitch():
    """ 
    Invoke reset for ELK system, turning off SIEM.
    Changes:
        - All configurations will be reverted back to original
        - All engines will be offline
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
        with open(BASHRC_PATH, 'a') as bashrc:
            bashrc.writelines(config)

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

def all():
    # depman()
    # slog()
    # audit()
    # filebeat()
    bash()
    # logstash()
    return

if __name__ == "__main__":
    bash()