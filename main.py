import parsers
import sniffers
import threading
from activators import activate
from ui import ledger
import curses
import queue
import signal
from utils import OutputHandler
import os

panel = None
outHand = OutputHandler().getInstance()

def keyboardInterruptHandler(signal, frame):
    global panel
    panel.close()
    os.system("reset")
    exit(0)

def logQueMan():
    """
    Manage and display log output from every sensors
    """
    global panel, outHand
    outHand.sendLog("[*] Waiting for output from sensory...")
    while True:
        panel.out2logger(outHand.loggerQueue.get())
        panel.refresh()
    return

def outQueMan():
    """
    Manage and display stdout/stderr output from engines
    """
    global panel, outHand
    while True:
        panel.out2outerr(outHand.outerrQueue.get())
        panel.refresh()
    return


def panMan(stdscr):
    global panel
    panel = ledger.MainPanel(stdscr)

    p_thread = threading.Thread(target=panel.run, args=()).start()

    # --- Output Synchronization Management
    lq_thread = threading.Thread(target=logQueMan, args=()).start()
    oq_thread = threading.Thread(target=outQueMan, args=()).start()

if __name__ == "__main__":

    # --- Set signal handlers
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    # --- Dependency and configuration management
    activate.configs()

    # --- UI Management
    curses.wrapper(panMan)

    # --- Run required infrastructures
    activate.elk()

    # --- Thread initialization for every modules
    http = threading.Thread(target=sniffers.http.run, args=["*", "ens33"])
    slog_parser = threading.Thread(target=parsers.slog_parser.run, args=())
    bash_parser = threading.Thread(target=parsers.bash_parser.run, args=())

    # --- Begin running modules and its sensors
    http.start()
    slog_parser.start()
    bash_parser.start()
