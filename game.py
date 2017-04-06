#         Tales of Gods and Treachery: The Hunt for Bálbrandr
# -------------------------------------------------------------------
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# -------------------------------------------------------------------
# The MPL 2.0 license covers all .py files included in this distrib-
# ution, except for the file initialize.py. The MPL 2.0 license does
# not apply to that file as it has a separate license.

import dbconn as db
import parse
import ask
import globalvars as g
import cmd
import get

#turns = 0

def askPlayerName():    # Ask the player character's name.
    invalid = True      # Go into the loop.
    
    while invalid:
        plname = []                       # Reset old player name.
        plname = parse.sanitize(str(input("Character Name: ")),True)
        newname = parse.liToStr(plname)   # Concatenate list into a single string with item separated by space.
        
        if len(newname) == 0:                # Nothing was input, use default.
            plname = "Andrea Álvarez"
            print("Do you wish to be called "+str(plname)+"? (Y/N)")
            
            if ask.yn():   # The yes/no check is done in a function that returns True for a positive answer and False for a negative answer.
                invalid = False
        elif len(newname) > 64:
            print("Name must be under 64 characters.")
        else:
            print("Do you wish to be called "+str(newname)+"? (Y/N)")
            
            if ask.yn():   # The yes/no check is done in a function that returns True for a positive answer and False for a negative answer.
                invalid = False
                db.cur.execute("update people set name = \""+str(newname)+"\" where charid = \"player\";")
    
def gameLoop():                             # Main game loop.
    global turns
    
    while g.rungame:                        # While the boolean rungame in globalvars.py is True.
        parse.parse(str(input("> ")))       # Parse player input.
        #turns += 1

def runGame():                      # Because functions.
    g.update()                  # Initialize global variables.
    g.initCmdList()             # Initialize command list.
    print(get.text("gtitle2")) # Print title screen.
    #menu()
    
    if g.gameSaved == "0":          # No saved game.
        askPlayerName()             # Ask player name.
        print("\n"+get.text("devtips"))
    
        if parse.sanitize(str(input("Press Enter to continue."))) != None:    # Input anything.
            print("\n"+get.text("intro"))                    # Print intro.
            if parse.sanitize(str(input("Press Enter to continue."))) != None:    # Input anything.
                if g.Chapters == "1":                       # Print chapters?
                    print("\n                 ----    Chapter I: The Hidden Letter    ----")
                cmd.look()      # Look around the first room.
                gameLoop()      # Game
    else:
        cmd.look()          # Look around the first room.
        gameLoop()          # Game

# Welcome to Functions: The Game!
runGame()
