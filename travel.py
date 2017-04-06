import dbconn as db
import parse
import find
import get
import action
import cmd
import ask
import globalvars as g
import item

def travel(*args):
    inputlist = parse.checkArgs(args,"Travel where?","","to")
    
    if inputlist:
        charid = "player"
        toid = find.idFromName(inputlist,"location",[],True)
        
        while len(toid) > 1:
            toid = ask.which(toid,"location")
        
        if toid:
            if get.visCheck(toid[0]):
                if toid[0] in g.worldTravel and find.plLoc() in g.worldTravel:
                    if item.valTrans(200,["player"],[]," to travel to "+find.nameFromID(toid,"location")[0]):
                        print("You pay the standard fare of 200.")
                        db.cur.execute("update people set val = val - 200 where charid = \"player\";")
                        print("Traveling to "+find.nameFromID(toid,"location")[0]+".")
                        
                        if toid[0] == "buairpor" and g.firstBulgaria == "1" and g.Chapters == "1":
                            print("\n             ----    Chapter II: Tracking Zlatin Panayotov    ----")
                            db.cur.execute("update save set val = 0 where var = \"firstBulgaria\";")
                            g.update()
                            
                        elif toid[0] == "taport" or toid[0] == "taairpor" and g.firstTanz == "1" and g.Chapters == "1":
                            print("\n                 ----    Chapter III: Retrieving Beast    ----")
                            db.cur.execute("update save set val = 0 where var = \"firstTanz\";")
                            g.update()
                        
                        elif toid[0] == "inairpor" and g.backToIndia == "1" and g.Chapters == "1":
                            print("\n                   ----    Chapter IV: The Fjǫrsteinn    ----")
                            db.cur.execute("update save set val = 0 where var = \"backToIndia\";")
                            g.update()
                            
                        elif toid[0] == "grport" and g.grFisherCrater == "0" and g.Chapters == "1":
                            print("\n                 ----    Chapter V: The Fabled Guðhjǫrr    ----\n")
                            # Variable update handled in action.
                        
                        elif toid[0] == "peport" and g.firstPeru == "1"  and g.Chapters == "1":
                            print("\n                  ----    Chapter VIII: The Guðhjǫrr    ----")
                            db.cur.execute("update save set val = 0 where var = \"firstPeru\";")
                            g.update()
                        
                        action.travel(find.plLoc(),toid[0])
                        db.cur.execute("update people set locid = \""+toid[0]+"\" where charid = \""+charid+"\";")
                        cmd.look()
                
                elif toid[0] == "netoti" or toid[0] == "inbussta":      # Bus fare.
                    if item.valTrans(20,["player"],["inbusdri"]," to take the bus"):
                        print("You pay the bus fare of 20 money.")
                        db.cur.execute("update people set val = val - 20 where charid = \"player\";")
                        action.travel(find.plLoc(),toid[0])
                        db.cur.execute("update people set locid = \""+toid[0]+"\" where charid = \""+charid+"\";")
                        cmd.look()
                
                elif toid[0] == "pecave2" or toid[0] == "pecave":                      # INTO THE PIT WITH YOU!
                    if "flalight" in find.listInvItemIDs():     # Flashlight check AKA. FU PL
                        dundundun = True
                    else:
                        dundundun = False
                    
                    if g.debug:
                        print("[DBG] travel FLASHLIGHT CHECK:",dundundun,toid[0])
    
                    if dundundun:                               # Why would you pick it up?
                        action.setVis("pecave2",0)
                        action.setVis("pecave",1)
                        print("Traveling to the "+find.nameFromID(["pecave"],"location")[0]+".")
                        action.travel(find.plLoc(),"pecave")
                        db.cur.execute("update people set locid = \"pecave\" where charid = \""+charid+"\";")
                        cmd.look()
                    else:
                        action.setVis("pecave",0)
                        action.setVis("pecave2",1)
                        print("Traveling to the "+find.nameFromID(["pecave2"],"location")[0]+".")
                        action.travel(find.plLoc(),"pecave2")
                        db.cur.execute("update people set locid = \"pecave2\" where charid = \""+charid+"\";")
                        cmd.look()
                else:
                    print("Traveling to "+find.nameFromID(toid,"location")[0]+".")
                    action.travel(find.plLoc(),toid[0])
                    db.cur.execute("update people set locid = \""+toid[0]+"\" where charid = \""+charid+"\";")
                    cmd.look()
            else:
                print("You can't travel there.")
        else:
            print("You can't travel there.")