import parsers
import sniffers
import threading
from activators import activate
from ui import ledger
import curses
import queue
import signal

logQueue = queue.Queue()
outQueue = queue.Queue()
panel = None

def keyboardInterruptHandler(signal, frame):
    global panel
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    panel.close()
    exit(0)

def logQueMan():
    global panel, logQueue
    while True:
        panel.out2log(logQueue.get())
        panel.refresh()
    return

def outQueMan():
    global panel, outQueue
    while True:
        panel.out2elk(outQueue.get())
        panel.refresh()
    return


def panMan(stdscr):
    global panel
    panel = ledger.MainPanel(stdscr)

    p_thread = threading.Thread(target=panel.run, args=()).start()
    lq_thread = threading.Thread(target=logQueMan, args=()).start()
    oq_thread = threading.Thread(target=outQueMan, args=()).start()

if __name__ == "__main__":

    # --- Dependency and installation management
    # activate.all()

    # --- Thread initialization for every modules
    http = threading.Thread(target=sniffers.http.run, args=["*", "ens33", logQueue, outQueue])
    slog_parser = threading.Thread(target=parsers.slog_parser.run, args=[logQueue, outQueue])
    bash_parser = threading.Thread(target=parsers.bash_parser.run, args=[logQueue, outQueue])

    # --- Begin running modules and sensors
    http.start()
    slog_parser.start()
    bash_parser.start()

    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    # --- Output Synchronization Management

    # queMan(queue)

    # --- UI Management

    curses.wrapper(panMan)

    


