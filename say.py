import parse
import action
import find

def say(*args):
    inputlist = parse.checkArgs(args,"Say what?","","say")
    
    if inputlist:
        name = find.nameFromID(["player"],"people")
        print(name[0],"says \""+parse.liToStr(inputlist)+"\"")
        action.say(inputlist,find.plLoc())