import parse
import find
import action
import ask
import get

def greet(*args):
    inputlist = parse.checkArgs(args,"Greet who?","","greet")
    
    if inputlist:
        charid = find.idFromName(inputlist,"people")
    
        while len(charid) > 1:
            charid = ask.which(charid,"people")
        
        if charid:
            if len(charid) > 1:
                greet(ask.which(charid),"people")
            else:
                action.greet(charid[0])
                get.topics(charid)
        else:
            print("That person is not here.")