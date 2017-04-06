import parse
import find
import action
import ask
import globalvars as g

def use(*args):
    two = True
    valid = True
    
    if len(args) == 0:
        inputlist = parse.checkArgs(args,"Use what?","","use")
    else:
        inputlist = args[0]
    
    if g.debug:
        print("[DBG] use INPUTLIST:",inputlist)
        
    try:
        i = inputlist.index("on")
        two = True
    except ValueError:
        try:
            i = inputlist.index("with")
            two = True
        except ValueError:
            two = False
    
    if g.debug and two:
        print("[DBG] use INDEX:",i)
    
    if not two:
        item1 = parse.removeDuplicates(find.idFromName(inputlist,"item",["player"]))
        
        while len(item1) > 1:
            item1 = ask.which(item1,"item",["player"])

        if len(item1) == 0:
            print("You have no such item.")
        else:
            action.use(item1[0])
    else:
        item1 = parse.removeDuplicates(find.idFromName(inputlist[:i],"item",["player"]))
        
        while len(item1) > 1:
            item1 = ask.which(item1,"item",["player"])
            
        if len(item1) == 0:
            print("You do not have that item.")
            valid = False
        
        if g.debug:
            print("[DBG] use ITEM1:",item1,valid)
        
        if valid:
            
            item2 = parse.removeDuplicates(find.idFromName(inputlist[i+1:],"item"))
            
            if not item2:
                item2 = parse.removeDuplicates(find.idFromName(inputlist[i+1:],"item",["player"]))
            
            if g.debug:
                print("[DBG] use ITEM2:",item2)
            
            while len(item2) > 1:
                item2 = ask.which(item2,"item")
            
            if len(item2) == 0:
                print("That item is not here.")
                valid = False
            elif valid:
                action.use(item1[0],item2[0])