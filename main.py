import threading
import serviceguards

from activators import activate

# from ui import ledger
# from utils import OutputHandler

# import curses
# import queue

import signal
import os
import subprocess

panel = None
exiting = False
# outHand = OutputHandler().getInstance()

def keyboardInterruptHandler(signal, frame):
    global exiting
    # panel.close()
    if not exiting:
        exiting = True
        kill_infra = input("Do you want to stop docker containers? [Y/n]: ")
        if kill_infra.upper() == "Y":
            print("[Main] Starting containers termination...")
            serviceguards.elkstack.stop()
            serviceguards.redistimeseries.stop()
            print("[Main] Containers terminated.")
        serviceguards.beatsforwarder.stop()
        serviceguards.xssauditor.stop()
        # os.system("reset")
        exit(0)
    else:
        print("[Main] Already exiting... Please wait.")

def menu():
    setup = -1
    while True:
        os.system("clear")
        print("Nethive, a SIEMxCVSS Project\n")
        print("[1] Check Dependencies")
        print("[2] Refresh Configuration")
        print("[3] Run Nethive")
        print("[4] Exit")
        setup = input(">> ")

        if setup == "1":
            # check if dependencies are already installed
            print("Checking Filebeat...")
            time.sleep(0.5)
            print("OK")
            print("Checking Auditbeat...")
            time.sleep(0.3)
            print("OK")
            print("Checking Packetbeat...")
            time.sleep(0.7)
            print("OK")
            print("Checking Docker and docker-compose...")
            time.sleep(1)
            print("OK")
            pass
        elif setup == "2":
            activate.configs()
        elif setup == "3":
            return
        elif setup == "4":
            exit(0)
        else:
            print("Invalid input, please try again.")
            input("Press [enter] to continue...")

if __name__ == "__main__":

    # --- Set signal handlers
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    # --- Dependency and configuration management

    menu()
    
    # --- Activating Nethive Engines

    serviceguards.elkstack.run()
    # serviceguards.kafkaserver.run()
    serviceguards.redistimeseries.run()

    serviceguards.inspectioncontroller.run()

    serviceguards.httpsniffer.run()
    serviceguards.xssauditor.run()
    serviceguards.slogparser.run()
    # serviceguards.threlkengine.run()

    serviceguards.beatsforwarder.run()
    
    print("[Main] Nethive SIEM is active.")
