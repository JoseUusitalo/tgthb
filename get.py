import dbconn as db
import parse
import find
import globalvars as g
import sysmsg

def visCheck(locid):
    """String -> Boolean | Returns true if the area is available."""
    
    db.cur.execute("select vis from location where locid = \""+locid+"\";")
    
    if db.cur.fetchall()[0][0] == 1:
        return True
    else:
        return False

def topics(charid):
    db.cur.execute("select topic from dialogue where charid = \""+charid[0]+"\";")
    result = parse.noneStrip(parse.multiTupleListToList(db.cur.fetchall()))
    
    if g.debug:
        print("[DBG] get.topics:",charid,result)

    #print("DEBUG TOPICS:",result)
    
    #if "Greet" in result:
    #    i = result.index("Greet")
    #    del result[i]
    #print("DEBUG TOPICS2:",result)
    
    if len(result) > 0:    
        print("You can talk to "+parse.liToStr(find.nameFromID(charid,"people"))+" about "+parse.naturalList(result,"and")+".")

def allPrints(locid):
    """String -> Pre-formatted string."""
    
    #db.cur.execute("select l.name, l.dsc from location as l where locid = \""+locid+"\";")
    dirnames = ["north","northeast","east","southeast","south","southwest","west","northwest","above","below"]
    locnames = []
    speciallocnames = []
    fullloc = "There is "
    i = 0
    killLoop = False
    locations = []
    directions = []
    
    db.cur.execute("select name,dsc from location where locid =\""+locid+"\";")
    locs = parse.multiTupleListToList(db.cur.fetchall())
    
    db.cur.execute("select name from people where locid =\""+locid+"\" and charid != \"player\";")  # Exclude player from the list.
    people = parse.multiTupleListToList(db.cur.fetchall())
    
    db.cur.execute("select it.name from itemtype as it, item as i where i.locid =\""+locid+"\" and i.typeid = it.typeid;")
    items = parse.multiTupleListToList(db.cur.fetchall())
    
    #db.cur.execute("select n,ne,e,se,s,sw,w,nw,up,down,spec1,spec2,spec3,spec4,spec5,air1,air2,air3,air4,air5,sea1,sea2,sea3,sea4,sea5 from world where fromid = \""+locid+"\";")
    db.cur.execute("select n,ne,e,se,s,sw,w,nw,up,down,spec1,spec2,spec3,spec4,spec5,air1,air2,air3,air4,air5,sea1,sea2,sea3,sea4,sea5 from world where fromid = \""+locid+"\";")
    dirids = parse.multiTupleListToList(db.cur.fetchall())
    
    for idloc in dirids:
        db.cur.execute("select name from location where locid = \""+str(idloc)+"\" and vis != 0;")  # Get all locations from here, exclude hidden ones.
        
        try:
            locname = db.cur.fetchall()[0][0]
        except IndexError:
            locname = None
        
        if g.debug == "verbose":
            print("[DBG] get.allPrints LOCNAME",locname)
        
        if idloc in g.worldTravel:
            if visCheck(idloc):
                locnames.append(locname + " (" + g.countries[g.worldTravel.index(idloc)] + ")")
            else:
                locnames.append(locname)
        elif idloc in g.asiaTravel:
            if visCheck(idloc):
                locnames.append(locname + " (" + g.asiaCountries[g.asiaTravel.index(idloc)] + ")")
            else:
                locnames.append(locname)
        else:
            locnames.append(locname)
    
    slocnames = locnames[10:]
    for name in slocnames:
        if name != None:
            speciallocnames.append(name)
    
    locnames = locnames[:len(locnames)-15]  # Take out the air/boat/special locations.
    
    for a in locnames:
        if a != None:
            locations.append(locnames[i])
            directions.append(dirnames[i])
        i += 1
    
    i = 0
    
    while not killLoop:
        if i >= len(locations):
            killLoop = True
        else:
            if i == len(locations)-1:
                if len(locations) != 1:
                    fullloc += "and "
            
            if i != len(locations):
                if directions[i] == "above" or directions[i] == "below":
                    if i == len(locations)-1:
                        fullloc += str(locations[i] + " " + directions[i])
                    else:
                        fullloc += str(locations[i] + " " + directions[i] + ", ")
                else:
                    if i == len(locations)-1:
                        fullloc += str(locations[i] + " to the " + directions[i])
                    else:
                        fullloc += str(locations[i] + " to the " + directions[i] + ", ")                
        i += 1
    
    areis = " are" if (len(people) > 1) else " is" if (len(people) == 1) else "Nobody is"
    itemstring = (" and " + parse.naturalList(items) + " can be found in the area.") if (len(items) > 0) else "."
    locsstring = fullloc + "." if (fullloc != "There is ") else fullloc + "nowhere to go to."
    travelstring = "\nYou may travel to " + parse.naturalList(speciallocnames, "and") + "." if (len(speciallocnames) > 0) else ""
    
    if g.debug == "verbose":    # Just disabling these prints.
        print("[DBG] get.allPrints AREIS")
        print(areis)
        print("[DBG] get.allPrints ITEMSTRING")
        print(itemstring)
        print("[DBG] get.allPrints LOCSTRING")
        print(locsstring)
        print("[DBG] get.allPrints TRAVELSTRING")
        print(travelstring,end="\n")
    
    print("\n"+locs[0]+"\n"+locs[1]+"\n\n" + parse.naturalList(people, "and") + areis + " here" + itemstring + "\n" + locsstring + travelstring)

def text(txtid):
    """String -> String."""
    
    db.cur.execute("select txt from text where txtid = \""+txtid+"\";")
    result = db.cur.fetchall()
    if db.cur.rowcount > 0:
        for row in result:
            return row[0]+"\n"
    else:
        sysmsg.show("notext")

def dlg(dlgid):
    """String -> String."""
    
    db.cur.execute("select txt from dialogue where dlgid = \""+dlgid+"\";")
    return "\n"+parse.tupleListToList(db.cur.fetchall())[0]

def storeItems(locid):
    """String -> Print"""
    
    seller = g.buyppl[g.buylocs.index(locid)]
    itemidlist = find.listInvItemIDs([seller])
    itemnamelist = find.nameFromID(itemidlist,"item")
    itemvallist = find.listValueByID(itemidlist,"item")
    
    if len(seller) == 0:
        print("The store keeper is not here!")
    else:
        print("The storekeeper is "+find.nameFromID([seller],"people")[0]+" and has "+str(find.listValueByID([seller],"people")[0])+" money. They sell the following items:")
        for i in range(0,len(itemidlist)):
            print("- "+itemnamelist[i]+" ("+str(itemvallist[i])+")")