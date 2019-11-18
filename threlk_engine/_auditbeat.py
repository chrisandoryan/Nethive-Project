SYSTEM_MODIFICATION_FLAG = "SYSMOD"
ROLE_AND_AUTH_FLAG = "RNA"
FILE_INTERACTION_FLAG = "FILE"
EXTRA_WATCHLIST_FLAG = "EXTRA"
NETWORK_ACTIVITY_FLAG = "NETACT"

AUDIT_TRAIL_TAGS = {
    SYSTEM_MODIFICATION_FLAG: {
        "SOFTWARE_MANAGEMENT": [
            "software_mgmt"
        ],
        "POWER_STATE": [
            "power"
        ],
        "STARTUP_SCRIPTS": [
            "init"
        ],
        "KERNEL_INTERACTION": [
            "sysctl",
            "modules",
            "modprobe",
            "KEXEC"
        ],
        "CRON": [
            "cron"
        ],
        "FILESYSTEM": [
            "mount",
            "swap",
            "specialfiles"
        ],
        "TIME": [
            "time",
            "localtime"
        ],
        "SERVICE_MANAGEMENT": [
            "systemd"
        ]
    },
    ROLE_AND_AUTH_FLAG: {
        "PRIVILEGE_ABUSE": [
            "power_abuse"
        ],
        "RNA_INFO_CHANGE": [
            "sudoers_modification",
            "group_modification",
            "user_modification",
            "login",
            "etcgroup",
            "etcpasswd",
            "opasswd"
        ],
        "SWITCH_ACCOUNT": [
            "priv_esc"
        ],
        "ROOT_COMMAND_EXEC": [
            "rootcmd"
        ],
        "MAC_CHANGE": [
            "mac_policy"
        ],
        "SERVICE_LOGINS": [
            "session",
            "sshd",
            "pam"
        ]
    },
    FILE_INTERACTION_FLAG: {
        "CRITICAL_RESOURCE_ACCESS": [
            "unauthedfileaccess"
        ],
        "UNSUCCESS_INTERACTION": [
            "file_access",
            "file_creation",
            "file_modification"
        ],
        "DAC_CHANGE": [
            "perm_mod"
        ]
    },
    NETWORK_ACTIVITY_FLAG: {
        "NETWORK_MODIFICATION": [
            "hostname_change",
            "network_modifications",
            "etcissue"
        ]
    },
    EXTRA_WATCHLIST_FLAG: {
        "SUSPICIOUS_BINARY": [
            "susp_activity",
            "sbin_susp"
        ],
        "RECON_COMMAND": [
            "recon"
        ],
        "32BIT_API_EXPLOIT": [
            "32bit_api"
        ],
        "PTRACE_CODE_INJECTION": [
            "tracing",
            "code_injection",
            "register_injection"
        ],
        "USER_SUPPLIED_CHECK": [],
    }

}

def process():

    return

def categorize_message(beats):
    for key, value in AUDIT_TRAIL_TAGS.items():
        print("{} => {}".format(key, value))
    return

def extract_tags(beat_packet):
    try:
        return beat_packet['tags'][0]
    except Exception as e:
        return ""

if __name__ == "__main__":
    categorize_message(10)