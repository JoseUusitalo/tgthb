import parse
import find
import sysmsg
import globalvars as g

def which(idlist,listType="",charid=[]):
    """When a query returned more than one result and you need to ask which one to use. Returns a list with a single item.
        
        idlist    List: List of IDs.
        listType  String: Type of IDs. Valid values: item/people/location/topic
        charid    List: charid of character whose inventory/topic to search if listType is item or topic."""
    
    if g.debug:
        print("[DBG] ask.which:",idlist,listType,charid)
    
    valid = False
    
    names = find.nameFromID(idlist,listType)
    
    while not valid:
        if g.debug:
            print("[DBG] ask.which NAMES",names)
        
        if len(names) > 1 and len(set(names)) == 1:    # Two things listed, they have the same name -> same type, use the first one.
            if g.debug:
                print("[DBG] ask.which FOUND ONLY ONE UNIQUE IN:",names)
            
            plinput = idlist[:1]
            valid = True
        
        elif len(charid) == 0 and not valid:
            print("Did you mean "+parse.naturalList(names, "or")+"? (empty to cancel)")
            plinput = find.idFromName(parse.sanitize(str(input("> "))),listType)
            
            if g.debug:
                print("[DBG] ask.which PLINPUT:",plinput)
            
            if len(plinput) == 1 or len(plinput) == 0:
                valid = True
            else:
                names = find.nameFromID(plinput,listType)
        
        elif len(charid) > 0 and not valid:
                print("Did you mean "+parse.naturalList(names, "or")+"? (empty to cancel)")
                plinput = find.idFromName(parse.sanitize(str(input("> "))),listType,charid)

                if g.debug:
                    print("[DBG] ask.which PLINPUT:",plinput)
                
                if len(plinput) == 1 or len(plinput) == 0:
                    valid = True
                else:
                    names = find.nameFromID(plinput,listType)
        else:
            sysmsg.show("argerror")
    
    if g.debug:
        print("[DBG] ask.which RETURNS:",plinput)
    
    return plinput

def yn():
    positive = ["y","Y","1","yes","YES","Yes","ok","OK","Ok","agree","AGREE","Agree","yup","YUP"]
    negative = ["n","N","0","no","NO","No","decline","Decline","DECLINE","nope","NOPE"]
    invalid = True
    
    while invalid:    
        ans = parse.sanitize(str(input("> ")))
        
        if ans:
            if ans[0] in positive:
                invalid = False
                return True
            elif ans[0] in negative:
                invalid = False
                return False
            else:
                print("Please type either yes or no.")
        else:
            print("Please type either yes or no.")