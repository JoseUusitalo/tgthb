import dbconn as db
import sysmsg
import parse
import globalvars as g
import get

def idFromName(inlist,nameType,charid=[],local=True):
    """Find itemid/charid/locid from a list of words. Returns a list with the IDs.
        
        inlist    List: Search words.
        nameType  String: Name of database table to search from. One per search. Valid values: item/people/location/topic
        charid    List: charid of character whose inventory/topic to search if listType is item or topic.
        local     Boolean: Search in the location where the player currently is?"""
    
    if g.debug:
        print("[DBG] idFromName ARGUMENTS:",inlist,nameType,charid,local)
    
    inputwords = []             # List of input words.
    idlist = []                 # List of output IDs.
    inputlist = inlist.copy()   # Don't ask. It's because of objects and referencing and things that I don't fully understand. With this, you can still print the original input.
    inputname = ""
    
    while len(inputlist) > 0:
        idlist = []         # Empty data for names with more than one word.
        inputname = ""      # Empty data for names with more than one word.
        
        if g.debug:
            print("[DBG] idFromName INPUTLIST:",inputlist)
        
        inputwords.append(inputlist.pop(0))         # Take out first search term from input list.
        
        if g.debug:
            print("[DBG] idFromName INPUTWORDS POPPED:",inputwords)

        checkname = "%".join(a for a in inputwords)  # Add to search string. % is a wildcard.
        
        for letter in checkname:    # For character in string.
            if letter != "'":       # Letter is not '.
                inputname += letter # Add it to the new string.
            else:
                inputname += "%"    # Replace ' with wildcard % so the MySQL queries work.
        
        if g.debug:
            print("[DBG] idFromName INPUTNAME CLEANED:",inputname)

        if nameType == "item":
            if len(charid) > 0:
                db.cur.execute("select item.itemid from item, itemtype where itemtype.name like \"%"+inputname+"%\" and itemtype.typeid = item.typeid;")
                result = parse.multiTupleListToList(db.cur.fetchall())
                
                for a in result:
                    if a in listInvItemIDs(charid):    # If itemid in player inventory.
                        idlist.append(a)
            
            elif len(charid) == 0 and local:
                db.cur.execute("select item.itemid from item, itemtype, people where itemtype.name like \"%"+inputname+"%\" and itemtype.typeid = item.typeid and item.locid = people.locid and people.charid = \"player\";")
                idlist = parse.multiTupleListToList(db.cur.fetchall())
            
            else:                               # Global search.
                db.cur.execute("select item.itemid from item, itemtype where itemtype.name like \"%"+inputname+"%\" and itemtype.typeid = item.typeid;")
                idlist = parse.multiTupleListToList(db.cur.fetchall())             
        
        elif nameType == "people":
            if local:
                db.cur.execute("select charid from people where name like \"%"+inputname+"%\" and locid = \""+plLoc()+"\" and charid != \"player\";")
                idlist = parse.multiTupleListToList(db.cur.fetchall())
            else:
                db.cur.execute("select charid from people where name like \"%"+inputname+"%\" and charid != \"player\";")
                idlist = parse.multiTupleListToList(db.cur.fetchall())
        
        elif nameType == "location":
            db.cur.execute("select locid from location where name like \"%"+inputname+"%\";")
            result = parse.multiTupleListToList(db.cur.fetchall())
            
            if local:
                for a in result:
                    if a in localSpecLoc():
                        if get.visCheck(a):
                            idlist.append(a)
            else:
                idlist = result
        elif nameType == "topic":
            #print("looking topic",inputname,charid[0])
            db.cur.execute("select dlgid from dialogue where topic like \"%"+inputname+"%\" and charid = \""+charid[0]+"\";")
            idlist = parse.multiTupleListToList(db.cur.fetchall())
            #print("potential topics",idlist)
        else:
            sysmsg.show("notype")
    #print("idlist with duplicates",idlist,"and no dupes",parse.removeDuplicates(idlist))
    if g.debug:
        print("[DBG] idFromName RETURNS:",idlist)
    return idlist

def nameFromID(inlist,nameType):
    """Find item/char/loc names from a list of IDs. Returns a list with the names."""
    
    inputwords = []             # List of input words.
    namelist = []               # List of output IDs.
    invalid = False             # Invalid input name?
    done = False                # Done with the search?
    inputlist = inlist.copy()   # Don't ask. It's because of objects and referencing and things that I don't fully understand. With this, you can still print the original input.
    
    while invalid == False and done == False and len(inputlist) > 0:   # Keep searching until we come across an invalid input item or we are done with the search.
        inputwords = []
        
        inputwords.append(inputlist.pop(0))         # Take out first search term from input list.
        inputid = "%".join(a for a in inputwords)  # Add to search string.
        
        if nameType == "item":
            db.cur.execute("select itemtype.name from item, itemtype where item.itemid = \""+inputid+"\" and itemtype.typeid = item.typeid;")
            result = parse.multiTupleListToList(db.cur.fetchall())
            
            for a in result:
                namelist.append(a)
        elif nameType == "people":
            db.cur.execute("select name from people where charid = \""+inputid+"\";")
            result = parse.multiTupleListToList(db.cur.fetchall())
            
            for a in result:
                namelist.append(a)
        elif nameType == "location":  
            db.cur.execute("select name from location where locid =\""+inputid+"\";")
            result = parse.multiTupleListToList(db.cur.fetchall())
            
            for a in result:
                namelist.append(a)
        elif nameType == "topic":
            #print("looking topic",inputname,charid[0])
            db.cur.execute("select topic from dialogue where dlgid = \""+inputid+"\";")
            result = parse.multiTupleListToList(db.cur.fetchall())
            
            for a in result:
                namelist.append(a)
            #print("potential topics",idlist)
        else:
            sysmsg.show("notype")
    #print("namelist with duplicates",namelist,"and without",parse.removeDuplicates(namelist))
    return namelist

def listInvItemIDs(charid=["player"],full=False):
    """List -> List | Returns a list with the item IDs in an inventory by charid. Full returns None values as well."""
    
    IDlist = []
    itemlist = []
    
    for i in range(1,11):
        sql = "select item.itemid from item, inventory where inventory.charid = \""+charid[0]+"\" and inventory.item"+str(i)+" = item.itemid;"
        db.cur.execute(sql)
        result = db.cur.fetchall()
        try:
            itemlist.append(result[0][0])
        except IndexError:
            itemlist.append(None)
    if not full:
        for i in itemlist:
            if i != None:
                IDlist.append(i)
        return IDlist
    else:
        return itemlist

def invSlotByItemID(itemid,charid=["player"]):
    """List -> Integer. Check None for empty slot, returns 0 for no empty slots."""
    if g.debug:
        print("[DBG] invSlotByItemID SLOT:",itemid,charid)
    
    try:
        if itemid == None or not itemid:
            return listInvItemIDs(charid,True).index(None)+1 
        else:
            return listInvItemIDs(charid,True).index(itemid[0])+1  
    except ValueError:
        return 0

def listValueByID(idlist,table="item"):
    """List -> List"""
    
    vallist = []
    
    if table == "item":
        for a in idlist:
            db.cur.execute("select itemtype.val from item, itemtype where item.itemid = \""+a+"\" and item.typeid = itemtype.typeid;")
            vallist.append(db.cur.fetchall()[0][0])
            
        return vallist
    elif table == "people":
        for a in idlist:
            db.cur.execute("select val from people where charid = \""+a+"\";")
            vallist.append(db.cur.fetchall()[0][0])
            
        return vallist
    else:
        sysmsg.show("notype")

def plLoc():
    """Returns the locid of the player location as a string."""
    
    db.cur.execute("select locid from people where charid = \"player\";")
    return db.cur.fetchall()[0][0]

def localSpecLoc():
    """Find special locations that can be traveled to from the player's location."""
    
    db.cur.execute("select spec1,spec2,spec3,spec4,spec5,air1,air2,air3,air4,air5,sea1,sea2,sea3,sea4,sea5 from world where fromid = \""+plLoc()+"\";")
    return parse.tupleListToList(db.cur.fetchall())
    
def itemValue(itemid):
    """List -> Integer"""
    
    db.cur.execute("select itemtype.val from item, itemtype where item.itemid = \""+itemid[0]+"\" and item.typeid = itemtype.typeid;")
    return db.cur.fetchall()[0][0]

def charMoney(charid=["player"]):
    """List -> Integer"""
    
    db.cur.execute("select val from people where charid = \""+charid[0]+"\";")
    return db.cur.fetchall()[0][0]

def oldvalCheck(val,charid=["player"]):
    """Returns True if charid has at least val money."""
    
    db.cur.execute("select val from people where charid = \""+charid[0]+"\";")
    
    if db.cur.fetchall()[0][0] >= val:
        return True
    else:
        return False
