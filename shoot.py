import dbconn as db
import parse
import find
import ask
import death
import action
import globalvars as g

def shoot(*args):
    if "revolver" in find.listInvItemIDs() and "bullets" in find.listInvItemIDs():
        
        objectid = parse.checkArgs(args,"Shoot what?","","shoot")
    
        if objectid:   
            person = find.idFromName(objectid,"people")
                
            while len(person) > 1:
                print(person)
                person = ask.which(person,"people")
            
            if len(person) != 0 and person[0] in g.immortals:
                print("You shot "+find.nameFromID(person, "people")[0]+".")
                action.shoot(person[0])
            elif person:
                if g.debug:
                    print("[DBG] shoot KILL",person)
                
                db.cur.execute("update people set hp = 0 where charid = \""+person[0]+"\";")
                name = find.nameFromID(person, "people")
                print("You shot",name[0], "dead!")
                death.death(person)
                action.shoot(person[0])
                
            else:
                print("Stop shooting like a maniac.")
            
    elif "revolver" and not "bullets" in find.listInvItemIDs():
        print("You don't have any bullets.")
    elif "bullets" and not "revolver" in find.listInvItemIDs():
        print("You don't have your revolver.")
    else:
        print("You cannot shoot without a loaded revolver.")
