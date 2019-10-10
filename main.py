import parsers
import sniffers
import threading
from activators import activate
from ui import ledger
import curses
import queue

def queMan(queue):
    while True:
        print(queue.get())
    return

if __name__ == "__main__":
    # --- Output Management
    queue = queue.Queue()

    # --- Dependency and installation management
    # activate.all()

    # --- Thread initialization for every modules
    http = threading.Thread(target=sniffers.http.run, args=["*", "ens33", queue])
    slog_parser = threading.Thread(target=parsers.slog_parser.run, args=[queue])
    bash_parser = threading.Thread(target=parsers.bash_parser.run, args=[queue])

    # --- Begin running modules and sensors
    http.start()
    slog_parser.start()
    bash_parser.start()

    queMan(queue)

    # --- UI Management
    # curses.wrapper(ledger.run)


