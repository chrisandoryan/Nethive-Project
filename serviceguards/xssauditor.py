import subprocess

proc = None

def run():
    print("[XSSAuditor] Starting XSS Auditor engine...")
    proc = subprocess.Popen("processors/xss_auditor/xss_auditor", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print("[XSSAuditor] Started.")

def stop():
    if proc:
        print("[XSSAuditor] Stopping XSS Auditor engine...")
        proc.kill()
        print("[XSSAuditor] Stopped.")