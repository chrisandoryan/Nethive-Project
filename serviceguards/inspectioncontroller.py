import processors
import threading

def run():
    print("[Inspection Controller] Starting Inspection Controller...")
    inspection_controller = threading.Thread(target=processors.inspection_controller.run, args=())
    inspection_controller.start()
    print("[Inspection Controller] Started.")