from threlk_engine import engine
import threading

def run():
    threlk = threading.Thread(target=engine.start, args=())
    threlk.start()
    return