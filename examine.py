import dbconn as db
import find
import action
import ask
import get
import parse
import globalvars as g

#Get description from an object
def examine(*args):
    place = False
    
    if len(args) == 0:
        place = True
    elif len(args) != 0 and args[0][0] == "here" or args[0][0] == "area":
        place = True
    else:
        inputlist = args[0]
    
    if not place:
        invitem = find.idFromName(inputlist,"item",["player"])
        if g.debug:
            print("[DBG] examine ITEM INV:",invitem)
        
        #if not invitem:
        locitem = find.idFromName(inputlist,"item")
        if g.debug:
            print("[DBG] examine ITEM LOCAL:",locitem)
        
        person = find.idFromName(inputlist,"people")
        if g.debug:
            print("[DBG] examine PERSON:",person)
           
        while len(invitem) > 1:
            invitem = ask.which(invitem,"item",["player"])
            if g.debug:
                print("[DBG] examine ITEM INV LOOP:",invitem)
             
        while len(locitem) > 1:
            locitem = ask.which(locitem,"item")
            if g.debug:
                print("[DBG] examine ITEM LOCAL LOOP:",locitem)

        while len(person) > 1:
            person = ask.which(person,"people")
            if g.debug:
                print("[DBG] examine PERSON LOOP:",person)
        
        if g.debug:
            print("[DBG] examine FOUND:",locitem,invitem,person)
        
        if invitem:
            db.cur.execute("select dsc from itemtype, item where item.itemid = \""+invitem[0]+"\" and item.typeid = itemtype.typeid;")
            result = parse.tupleListToList(db.cur.fetchall())
            if result:
                print(result[0])
        
        elif locitem:
            db.cur.execute("select dsc from itemtype, item where item.itemid = \""+locitem[0]+"\" and item.typeid = itemtype.typeid;")
            result = parse.tupleListToList(db.cur.fetchall())
            if result:
                print(result[0])
        
        elif person:
            db.cur.execute("select dsc from people where people.charid = \""+person[0]+"\";")
            result = parse.tupleListToList(db.cur.fetchall())
            if result:
                print(result[0])
            get.topics(person)
        else:
            print("You cannot examine that.")
    elif place:
        action.examine(find.plLoc())
    else:
        print("ERROR")





