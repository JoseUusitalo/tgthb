import dbconn as db
import parse
import find
import item
import action
import ask
import globalvars as g

def rent(*args):
    if find.plLoc() in g.rentlocs:
        inputlist = parse.checkArgs(args,"Rent what?","","rent")

        if g.debug:
            print("[DBG] rent INPUTLIST:",inputlist)
        
        if inputlist:
            count = 0
            seller = [g.rentppl[g.rentlocs.index(find.plLoc())]]
            
            if g.debug:
                print("[DBG] rent ARGS:",seller,find.plLoc())
            
            if find.plLoc() == "grinn1":
                if inputlist[0] == "room":
                    if action.checkTopic("kolrule") and item.valTrans(100,["player"],["grinnkee"]," to rent a room"):     # Player has spoken to Kolbiorn and has enough money.
                        db.cur.execute("update people set val = val - 100 where charid = \"player\";")
                        db.cur.execute("update people set val = val + 100 where charid = \""+seller[0]+"\";")
                        
                        action.rent("",seller[0],True)
                        count += 1
                else:
                    if count < 1:                       # Not an elegant solution but it works. (When found many items.)
                        print("There is no",parse.liToStr(inputlist),"to rent here.")
                    count += 1
            
            elif seller[0] == "grportma":
                if action.getVis("grbay"):         # Player knows about ship.
                    itemid = parse.removeDuplicates(find.idFromName(inputlist,"item",seller,False))
                    
                    if g.debug:
                        print("[DBG] rent SELLER HAS:",itemid)
                    
                    while len(itemid) > 1:
                        itemid = ask.which(itemid,"item",seller)
                    
                    if g.debug:
                        print("[DBG] rent BUYING:",itemid)
                    
                    if len(itemid) == 1 :
                        fromSlot = find.invSlotByItemID(itemid,seller)
                        
                        if fromSlot != 0:               # Found item in inventory.
                            val = find.listValueByID(itemid,"item")[0]
                            string = " to rent "+find.nameFromID(itemid,"item")[0]
                            
                            if item.valTrans(val,["player"],seller,string):  # Player has enough money.
                                item.transfer(itemid,["player"],seller,"rent",val)
                                action.rent(itemid[0],seller[0])
                                count += 1
                else:
                    if count < 1:                       # Not an elegant solution but it works. (When found many items.)
                        print("\"What would I need that for?\" you think to yourself.")
                    count += 1
                    
                    if g.debug:
                        print("[DBG] rent BAY VIS:",action.getVis("grbay"))
        else:
            if count < 1:                       # Not an elegant solution but it works. (When found many items.)
                print("There is no",parse.liToStr(inputlist),"to rent here.")
            count += 1
    else:
        print("There's nothing to rent here.")