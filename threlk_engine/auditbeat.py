SYSTEM_MODIFICATION_FLAG = "SYSTEM_MODIFICATION"
ROLE_AND_AUTH_FLAG = "ROLE_AND_AUTH"
FILE_INTERACTION_FLAG = "FILE_INTERACTION"
MISC_WATCHLIST_FLAG = "MISC_WATCHLIST"
NETWORK_ACTIVITY_FLAG = "NETWORK_ACTIVITY"

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
    MISC_WATCHLIST_FLAG: {
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

def parse(hits):
    for hit in hits:
        print(hit)
        print()
        package = {}
        try:
            data = hit['_source']
            major_tag, minor_tag = categorize_message(data['tags'][0])
            package = {
                "elastic_id": hit['_id'],
                "tag": data['tags'][0],
                "trail_tag": {
                    "major": major_tag,
                    "minor": minor_tag
                },
                "summary": data['auditd']['summary'],
                "hostname": data['host']['name'],
                "user": {
                    "id": data['user']['id'],
                    "name": data['user']['name'],
                    "group": data['user']['group']
                },
                "process": data['process'],
            }
        except Exception as e:
            pass
        yield package

def categorize_message(tag):
    for major_key, major_tags in AUDIT_TRAIL_TAGS.items():
        for minor_key, minor_tags in major_tags.items():
            if tag in minor_tags:
                return (major_key, minor_key)