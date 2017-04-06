import find
import dbconn as db
import globalvars as g

#Show player's inventory
def inventory(*args):
    itemlistIDs = find.listInvItemIDs()
    itemnamelist = find.nameFromID(itemlistIDs,"item")
    db.cur.execute("select val from people where charid = \"player\";")
    val = db.cur.fetchall()[0][0]
    
    print("You have",val,"money and you are carrying:")
    for i in itemnamelist:
        if i != None:
            print("-", i)
    if g.debug:
        print("[DBG] inventory FULL:",itemlistIDs)
    print()