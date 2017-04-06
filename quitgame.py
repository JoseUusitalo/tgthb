import dbconn as db
import globalvars as g
import cmd
import ask

def quitgame(*args):

    if len(args) == 0:
        print("Save before quitting? (Y/N)")
        
        if ask.yn():   # The yes/no check is done in a function that returns True for a positive answer and False for a negative answer.
            cmd.save(True)
        else:
            db.db.rollback()
            print("Game not saved.")
    else:  # Force quit and do not save if quitgame was called with any arguments.
        db.db.rollback()
        print("Game not saved.")
    
    print("\nQuitting game.")
    g.killLoop()
    db.db.close()
    