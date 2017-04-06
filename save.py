import dbconn as db
import ask
import globalvars as g

def save(*args):

    if len(args) == 0:
        print("Would you like to save your game? (Y/N)")
        if ask.yn():
            db.cur.execute("update save set val = 1 where var = \"gameSaved\";")
            g.update()
            db.db.commit()
            print("\nGame saved.")
        else:
            print("Game not saved.")
    else:       # Force save
        print("\nGame saved.")
        db.cur.execute("update save set val = 1 where var = \"gameSaved\";")
        g.update()
        db.db.commit()