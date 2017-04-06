import ask
import initialize
import cmd
#import game

def restart():
    print("Recreate database from scratch and restart the game? (Y/N)")
    
    if ask.yn():            # The yes/no check is done in a function that returns True for a positive answer and False for a negative answer.
        initialize.Database()
        initialize.Data()
        cmd.quitgame(True)
        #game.runGame()     # It's a shame I can't auto restart the game.