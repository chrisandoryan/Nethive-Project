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
# outHand = OutputHandler().getInstance()

def keyboardInterruptHandler(signal, frame):
    # global panel
    # panel.close()
    serviceguards.elkstack.stop()
    serviceguards.beatsforwarder.stop()
    serviceguards.xssauditor.stop()
    serviceguards.redistimeseries.stop()
    os.system("reset")
    exit(0)

    
# def logQueMan():
#     """
#     Manage and display log output from every sensors
#     """
#     global panel, outHand
#     outHand.sendLog("[*] Waiting for output from sensory...")
#     while True:
#         out = outHand.loggerQueue.get()
#         print(out)
#         if panel is not None:
#             panel.out2logger(out)
#             panel.refresh()
#     return

# def outQueMan():
#     """
#     Manage and display stdout/stderr output from engines
#     """
#     global panel, outHand
#     while True:
#         out = outHand.outerrQueue.get()
#         print(out)
#         if panel is not None:
#             panel.out2outerr(out)
#             panel.refresh()
#     return

# def panMan(stdscr):
#     global panel
#     # panel = ledger.MainPanel(stdscr)

#     # p_thread = threading.Thread(target=panel.run, args=()).start()

if __name__ == "__main__":

    # --- Set signal handlers
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    # --- Dependency and configuration management

    print("Nethive, a SIEMxCVSS Project\n")
    print("[1] Fresh Installation")
    print("[2] Refresh Configuration")
    print("[3] Just-Start-This-Thing")
    setup = input(">> ")

    if setup == "1":
        activate.fresh()
    elif setup == "2":
        activate.configs()
    elif setup == "3":
        pass
    else:
        print("Invalid input, please try again.")

    # --- UI Management
    # curses.wrapper(panMan)

    # --- Output Synchronization Management
    # lq_thread = threading.Thread(target=logQueMan, args=()).start()
    # oq_thread = threading.Thread(target=outQueMan, args=()).start()

    # --- Activating all sensories

    serviceguards.elkstack.run()

    serviceguards.inspectioncontroller.run()
    serviceguards.beatsforwarder.run()

    serviceguards.httpsniffer.run()
    serviceguards.xssauditor.run()
    serviceguards.slogparser.run()
    serviceguards.redistimeseries.run()
    serviceguards.threlkengine.run()

    print("[Main] Nethive SIEM is active.")