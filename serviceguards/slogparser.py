import parsers
import threading

def run():
    print("[SlogParser] Starting SlogParser Engine...")
    slog_parser = threading.Thread(target=parsers.slog_parser.run, args=())
    slog_parser.start()
    print("[SlogParser] Started.")