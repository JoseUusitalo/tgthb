import dbconn as db
import parse
import find
import ask

def drop(*args):
    inputlist = parse.checkArgs(args,"Drop what?","","drop")
    
    if inputlist:
        charid = "player"
        itemid = parse.removeDuplicates(find.idFromName(inputlist,"item",["player"]))
        
        while len(itemid) > 1:
            itemid = ask.which(itemid,"item",["player"])
        
        if itemid:
            if len(itemid) != 0:
                slot = find.invSlotByItemID(itemid)
                loc = find.plLoc()
                db.cur.execute("update inventory set item"+str(slot)+" = NULL where charid = \""+charid+"\";")
                db.cur.execute("update item set locid = \""+loc+"\" where itemid = \""+itemid[0]+"\";")
                print(find.nameFromID(itemid,"item")[0]+" dropped.")
            else:
                print("You do not have "+" ".join(inputlist)+".")
        else:
            print("You do not have "+parse.liToStr(inputlist)+".")