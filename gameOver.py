import cmd
import time
import get
import find
import globalvars as g

def slowPrint(text,sleep):
    for char in text:
        print(char,end="")
        time.sleep(sleep)

def End(endType):
    """Takes a string as an argument and ends the game."""
    
    if endType == "essential":
        print(get.text("essentia"))
        cmd.quitgame(True)
        print("\n                          ----    GAME OVER    ----")
    
    elif endType == "death":
        print(get.text("death"))
        cmd.quitgame(True)
        print("\n                          ----    GAME OVER    ----")
    
    elif endType == "win":
        print("\nA WINNER IS YOU!\n")
        cmd.quitgame(True)
        
    elif endType == "artifacts":
        gorkainv = find.listInvItemIDs(["spgorka"])
        plinv = find.listInvItemIDs()
        
        if g.debug:
            print("[DBG] gameOver GORKA INV",gorkainv)
            print("[DBG] gameOver PL INV",plinv)
        
        if "necklace" in gorkainv:
            print(get.text("endneckl"))
        
        if "viksword" in gorkainv:
            print(get.text("endrepli"))
        
        if "fjorstei" in gorkainv:
            print(get.text("endfjors"))
        
        if "guthjorr" in gorkainv:
            print(get.text("endguthh"))
        
        if "guthjorr" in plinv:
            print(get.text("endkguth"))
            
        if "fjorstei" in plinv:
            print(get.text("endkfjor"))
    
        cmd.quitgame(True)
        print("\n                           ----    YOU WIN    ----")
    

    elif endType == "immortality":
        print(get.text("immortal"))
        time.sleep(22)
        
        ending = get.text("ending")
        
        for char in ending:
            if char == "@":
                print("\n\n",end="")
                time.sleep(2)
            elif char == ">":
                time.sleep(0.75)
            elif char == "|":
                print(",",end="")
                time.sleep(1)
            elif char == ":":
                time.sleep(0.04)
            elif char == "-":
                time.sleep(0.06)
            elif char == "1":
                print("\n\n",end="")
                time.sleep(2.25)
            elif char == "2":
                print("\n\n",end="")
                time.sleep(2.5)
            elif char == "3":
                print("\n\n",end="")
                time.sleep(2.75)
            elif char == "4":
                time.sleep(2)
                print(".",end="")
            elif char == "5":
                time.sleep(4)
                print("\n")
                time.sleep(4)
            else:
                print(char,end="")
                time.sleep(0.04)
        
        cmd.quitgame(True)
