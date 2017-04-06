import parse
import find
import ask
import action
import globalvars as g

def call(*args):
    if find.plLoc() in g.callLocs:
        inputlist = parse.checkArgs(args,"Call who?","","call")
    
        if inputlist:
            charid = parse.removeDuplicates(find.idFromName(inputlist,"people",[],False))
            
            while len(charid) > 1:
                charid = ask.which(charid,"people")
            
            if g.debug:
                print("[DBG] call CHARID:",charid)
            
            if charid:
                if charid[0] in g.callPeople:
                    print("Calling "+find.nameFromID(charid,"people")[0]+".")
                    action.call(charid[0])
                else:
                    print("You can't call "+find.nameFromID(charid,"people")[0]+".")
            else:
                print("You can't call that person.")
    else:
        print("There is no phone here.")