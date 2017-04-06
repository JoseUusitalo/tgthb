import parse
import find
import ask
import item
import action
import globalvars as g
import get


def give(*args):   
    inputlist, i = parse.checkArgs(args,"Give what to who?","to")
    valid = True
    
    if inputlist:
        itemid = parse.removeDuplicates(find.idFromName(inputlist[:i],"item",["player"]))

        while len(itemid) > 1:
            itemid = ask.which(itemid,"item",["player"])
       
        if len(itemid) == 0:
            print("You do not have that item.")
            valid = False
        elif valid:
            charid = parse.removeDuplicates(find.idFromName(inputlist[i+1:],"people"))
           
            while len(charid) > 1:
                charid = ask.which(charid,"people")
            
            if len(charid) == 0:
                print("That person is not here.")
                valid = False
            elif valid:
                rightPerson = g.criticalItemPeople[g.criticalItem.index(itemid[0])]
                
                if g.debug:
                    print("[DBG] give CRITICAL ITEM",itemid,charid,rightPerson)
                
                if itemid[0] in g.criticalItem and charid[0] == rightPerson:
                    item.transfer(itemid,charid)
                    action.give(itemid[0],charid[0])
                elif itemid[0] == "necklace" and charid[0] == "spgorka":
                    item.transfer(itemid,charid)
                    action.give(itemid[0],charid[0])
                else:
                    print(get.text("dontgive"))