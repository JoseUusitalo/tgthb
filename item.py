import dbconn as db
import find
import sysmsg
import globalvars as g

def transfer(itemid,toid,fromid=["player"],action="give",val=""):
    toSlot = find.invSlotByItemID(None,toid)
    
    if toSlot < 11:
        fromSlot = find.invSlotByItemID(itemid,fromid)
        
        db.cur.execute("update inventory set item"+str(toSlot)+" = \""+itemid[0]+"\" where charid = \""+toid[0]+"\";")
        db.cur.execute("update inventory set item"+str(fromSlot)+" = NULL where charid = \""+fromid[0]+"\";")
    else:
        print("That character's inventory is full.")
    
    if action == "give":
        print(find.nameFromID(itemid,"item")[0]+" given to "+find.nameFromID(toid,"people")[0]+".")
    elif action == "buy":
        print(find.nameFromID(itemid,"item")[0]+" bought from "+find.nameFromID(fromid,"people")[0]+" for "+str(val)+".")
    elif action == "rent":
        print(find.nameFromID(itemid,"item")[0]+" rented from "+find.nameFromID(fromid,"people")[0]+" for "+str(val)+".")
    else:
        sysmsg.show("noaction")

def valTrans(val,fromchar,tochar,failtext):
    """Returns True if fromchar has enough money to transfer to tochar. Returns False, prints how much money is needed, and failtext if they do not have enough."""
    
    if g.debug:
        print("[DBG] valTrans ARGS+FROMVAL:",val,fromchar,tochar,failtext,find.charMoney(fromchar))
        
    if val <= find.charMoney(fromchar):  # Player has enough money.
        db.cur.execute("update people set val = val - "+str(val)+" where charid = \""+fromchar[0]+"\";")
        
        if tochar:
            db.cur.execute("update people set val = val + "+str(val)+" where charid = \""+tochar[0]+"\";")
        
        return True
    else:
        dif = val-find.charMoney(fromchar)
        print("You need",dif,"more money"+str(failtext)+".")
        
        return False