import parse
import find
import item
import ask
import action
import globalvars as g

def buy(*args):
    if find.plLoc() in g.buylocs:
        inputlist = parse.checkArgs(args,"Buy what?","","buy")

        if inputlist:
            count = 0
            
            seller = [g.buyppl[g.buylocs.index(find.plLoc())]]
            itemid = parse.removeDuplicates(find.idFromName(inputlist,"item",seller,False))
            
            if g.debug:
                print("[DBG] buy SELLER HAS:",itemid)
            
            while len(itemid) > 1:
                itemid = ask.which(itemid,"item",seller)
            
            if g.debug:
                print("[DBG] buy BUYING:",itemid)
            
            if len(itemid) == 1 :
                fromSlot = find.invSlotByItemID(itemid,seller)
                
                if fromSlot != 0:               # Found item in inventory.
                    val = find.listValueByID(itemid,"item")[0]
                    string = " to buy "+find.nameFromID(itemid,"item")[0]
                    
                    if item.valTrans(val,["player"],seller,string):  # Player has enough money.
                        item.transfer(itemid,["player"],seller,"buy",val)
                        action.buy(itemid[0],seller[0])
                        count += 1
            else:
                if count < 1:                       # Not an elegant solution but it works. (When found many items.)
                    print("There is no",parse.liToStr(inputlist),"to buy here.")
                count += 1
    else:
        print("There's nothing to buy here.")