import dbconn as db
import get
import action
import find
import parse

def move(mdir):
    db.cur.execute("select "+mdir+" from world where fromid = \""+find.plLoc()+"\";")
    newloc = parse.tupleListToList(db.cur.fetchall())
    
    if newloc[0] == None:
        print("You can't go there.")
    else:
        vis = get.visCheck(newloc[0])
        if vis == False:
            print("You cannot go there!")
        elif vis == True:
            charid = "player"
            db.cur.execute("update people set locid = \""+newloc[0]+"\" where charid = \""+charid+"\";")
            get.allPrints(newloc[0])    # From the new location: automatically print location description, items, people, and available movement
            action.move(newloc[0])
    
def north(*args):
    move("n")
def northeast(*args):
    move("ne")
def east(*args):
    move("e")
def southeast(*args):
    move("se")
def south(*args):
    move("s")
def southwest(*args):
    move("sw")
def west(*args):
    move("w")
def northwest(*args):
    move("nw")
def up(*args):
    move("up")
def down(*args):
    move("down")
