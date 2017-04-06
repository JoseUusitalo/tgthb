import dbconn as db
import parse
import find
import ask
import globalvars as g
import action

def take(*args):
    inputlist = parse.checkArgs(args,"Take what?","","take")
    
    if inputlist:
        charid = "player"
        itemid = parse.removeDuplicates(find.idFromName(inputlist,"item"))
        
        while len(itemid) > 1:
            itemid = ask.which(itemid,"item")
        
        if len(itemid) != 0 and itemid[0] == "altar":
            print("\"That is way too heavy to carry, let alone move.\"")
        
        elif itemid:
            slot = find.invSlotByItemID(None)
            
            if g.debug:
                print("[DBG] take TO SLOT:",slot)
            
            if slot != 0:
                db.cur.execute("update item set locid = \"INV\" where itemid = \""+itemid[0]+"\";")
                db.cur.execute("update inventory set item"+str(slot)+" = \""+itemid[0]+"\" where charid = \""+charid+"\";")
                print(find.nameFromID(itemid,"item")[0]+" taken.")
                action.take(itemid[0])
            else:
                print("Your inventory is full.")
        else:
            print(parse.liToStr(inputlist)+" is not here.")