import sniffers
import os
import settings
import threading

def run():
    print("[HTTPSniffer] Starting HTTPSniffer Engine...")
    http_sniffer = threading.Thread(target=sniffers.http.run, args=["*", os.getenv("LISTEN_IFACE")])
    http_sniffer.start()
    print("[HTTPSniffer] Started.")
