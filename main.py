import parsers
import sniffers
import threading
import observers
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
        out = outHand.loggerQueue.get()
        print(out)
        if panel is not None:
            panel.out2logger(out)
            panel.refresh()
    return

def outQueMan():
    """
    Manage and display stdout/stderr output from engines
    """
    global panel, outHand
    while True:
        out = outHand.outerrQueue.get()
        print(out)
        if panel is not None:
            panel.out2outerr(out)
            panel.refresh()
    return


def panMan(stdscr):
    global panel
    # panel = ledger.MainPanel(stdscr)

    # p_thread = threading.Thread(target=panel.run, args=()).start()

if __name__ == "__main__":

    # --- Set signal handlers
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    # --- Dependency and configuration management
    # activate.configs()
    activate.slog()
    activate.filebeat()
    activate.auditbeat()
    activate.packetbeat()
    activate.logstash()
    activate.elk()

    # --- UI Management
    curses.wrapper(panMan)

    # --- Output Synchronization Management
    # lq_thread = threading.Thread(target=logQueMan, args=()).start()
    # oq_thread = threading.Thread(target=outQueMan, args=()).start()

    # --- Run required infrastructures
    # activate.elk()

    # --- Thread initialization for every modules
    http = threading.Thread(target=sniffers.http.run, args=["*", os.getenv("LISTEN_IFACE")])
    slog_parser = threading.Thread(target=parsers.slog_parser.run, args=())
    bash_parser = threading.Thread(target=parsers.bash_parser.run, args=())
    sql_response_observer = threading.Thread(target=observers.sql_response.run, args=())
    packetbeat_receiver = threading.Thread(target=parsers.packetbeat_receiver.run, args=())
    # packetbeat_parser = threading.Thread(target=parsers.packetbeat_parser.run, args=())
    # sql_response_interceptor = threading.Thread(target=parsers.sql_response_interceptor.run, args=())

    # --- Begin running modules and its sensors
    http.start()
    slog_parser.start()
    bash_parser.start()
    sql_response_observer.start()
    packetbeat_receiver.start()
    # packetbeat_parser.start()
    # sql_response_interceptor.start()
