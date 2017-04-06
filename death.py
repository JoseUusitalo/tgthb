import find
import dbconn as db
import globalvars as g
import gameOver
import parse

def death(charid):
    if g.debug:
        print("[DBG] death",charid[0])
    
    db.cur.execute("update people set locid = NULL where charid = \""+charid[0]+"\";")
    deadinv = parse.noneStrip(find.listInvItemIDs(charid, True))
    
    db.cur.execute("select val from people where charid = \""+charid[0]+"\";")
    deadval = parse.tupleListToList(db.cur.fetchall())
    
    plloc = find.plLoc()
    
    if g.debug:
        print("DEBUG death DEADINV",deadinv)   
        print("DEBUG death DEADVAL",deadval) 
    
    if len(deadinv) > 0:
        for i in range(1,len(deadinv)):
            db.cur.execute("update inventory set item"+str(i)+" = NULL where charid = \""+charid[0]+"\";")
    
    if len(deadinv) > 0:
        for a in deadinv:
            db.cur.execute("update item set locid = \""+plloc+"\" where itemid = \""+a+"\";")
    
    print("You found "+str(deadval[0])+" money on "+find.nameFromID(charid,"people")[0]+"\'s body.")
    db.cur.execute("update people set val = val + \""+str(deadval[0])+"\" where charid = \"player\";")
    
    if charid[0] in g.essentialPeople:  # This must be at the bottom to prevent errors.
        gameOver.End("essential")