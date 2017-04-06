import parse
import find
import ask
import action
import get

def talk(*args):
    inputlist, i = parse.checkArgs(args,"Talk to who about what?","about","to","talk")
    valid = True
    
    if inputlist:
        charid = parse.removeDuplicates(find.idFromName(inputlist[:i],"people"))
        
        while len(charid) > 1:
            charid = ask.which(charid,"people")
        
        if len(charid) == 0:
            print("That person is not here.")
            valid = False
        elif valid:
            dialogid = parse.removeDuplicates(find.idFromName(inputlist[i+1:],"topic",charid,False))
            
            while len(dialogid) > 1:
                dialogid = ask.which(dialogid,"topic",charid)
            
            if len(dialogid) == 0:
                print(find.nameFromID(charid,"people")[0] + " doesn't seem to know anything about that.")
                valid = False
            elif valid:
                print(get.dlg(dialogid[0]))
                action.talk(charid[0],dialogid[0])