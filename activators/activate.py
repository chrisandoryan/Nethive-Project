import MySQLdb

def slog():
    db = MySQLdb.connect("hostname","user","pass","db")
    cursor = db.cursor()
    for line in open("slog.sql"):
        cursor.execute(line)
    db.close()
    return

def audit():
    return
    
def run():
    slog()
    
    return