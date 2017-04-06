import dbconn as db
import globalvars as g
import restart

def load():
    if g.gameSaved == "0":
        print("No save game detected.")
        restart.restart()
    else:
        db.db.rollback()
        print("Save loaded.")