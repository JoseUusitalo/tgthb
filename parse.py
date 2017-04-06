import dbconn as db
import sysmsg
import globalvars as g
import math
import get
import find
import cmd

def removeDuplicates(inputlist):
    """List -> List | Remove duplicate entries from a list."""
    
    outputlist = []
    
    for item in inputlist:
        if item not in outputlist:
            outputlist.append(item)
    
    return outputlist

def sanitize(inputstring,name=False):
    """String -> List"""
    badchars = ["    ","¡","¦","§","¨","©","ª","«","¬","­","¯","°","±","²","³","´","¶","·","¸","¹","º","»","¿","!","\"","#","$","%","&","(",")","*","+",",",".","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~"]
    altchars = ["    ","¡","¦","§","¨","©","ª","«","¬","­","¯","°","±","²","³","´","¶","·","¸","¹","º","»","¿","!","\"","#","$","%","&","(",")","*","+",",","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~"]
    cleanstring = ""
    cleaned = []
    
    for inchar in inputstring:                  # For character in string
        if not name:
            if inchar not in badchars:          # Current character not a bad character.
                cleanstring += inchar.lower()   # Add character to clean string as lowercase.
        else:
            if inchar not in altchars:          # Current character not a bad character.
                cleanstring += inchar           # Add character to clean string.
            
    cleanlist = cleanstring.split(" ")          # Split words separated by spaces to a list.
    
    for a in cleanlist:                         # For item in list.
        if a != " " and a != "":                # Current item not empty or whitespace.
            cleaned.append(a)                   # Add item to cleaned list.
    
    return cleaned

def checkArgs(args,ask,require="",delete="",cmd=""):
    """Check whether player input arguments for a command. If not, ask for input and return a word list."""
    
    if g.debug:
        print("[DBG] checkArgs:",args,ask,require,delete,cmd)
    
    valid = False
    i = None
    
    if len(args) > 0 and len(delete) > 0:
        if args[0][0] == delete:
            del args[0][0]          # Delete the first word like "to" in "talk to" or "travel to".
    
    if len(args) > 0 and len(require) == 0:
        plinput = args[0]
        valid = True
        
    elif len(args) > 0 and len(require) > 0:
        plinput = args[0]
        
        if require in plinput:
            i = plinput.index(require)
            valid = True
        else:
            print("You need to use the word \""+require+"\" in your input.")
            valid = False
           
            if cmd == "talk":
                person = removeDuplicates(find.idFromName(plinput,"people"))
                
                if len(person) == 1:
                    get.topics(person)
        
    while not valid:                        # Player didn't input anything!
        print(ask+" (empty to cancel)")     # I.e. "Take what?"
        plinput = sanitize(str(input("> ")))
        
        if g.debug:
            print("[DBG] checkArgs PLINPUT:",plinput)
        
        if len(plinput) > 0 and len(delete) > 0:
            if plinput[0] == delete:
                del plinput[0]          # Delete the first word like "to" in "talk to" or "travel to".
        
        if len(plinput) > 0:                # Player finally input some arguments.
            if len(require) == 0:
                valid = True
            else:
                if require in plinput:
                    i = plinput.index(require)
                    valid = True
                else:
                    print("You need to use the word \""+require+"\" in your input.")
                    valid = False
        else:
            valid = True
    
    if g.debug:
        print("[DBG] checkArgs RETURNS:",plinput)
    
    if len(require) == 0:
        return plinput
    else:
        return plinput, i

def liToStr(inputlist):
    """List [ Data,Data ] -> String ' Data Data '"""
    
    return " ".join([str(a) for a in inputlist])

def tupleListToList(queryOutput):
    """List[ Tuple(Data,Data) ] -> List[ Data,Data ]
    NOTE: Only returns data for the first found record!"""
    
    return [a for a in queryOutput[0]]

def multiTupleListToList(tlist):
    """List[ Tuple(Data,),Tuple(Data,) ] -> List[ Data,Data ]"""
    
    return [a for sublist in tlist for a in sublist]

def noneStrip(inputlist):
    """Remove all None types from a list."""
    
    outputlist = []
    
    for a in inputlist:
        if a != None:
            outputlist.append(a)

    return outputlist

def naturalList(inlist,finalstr="and"):
    """String -> Pre-formatted string."""
    
    liststring = ""                                 # A pretty list separated with commas.
    
    for i in range(len(inlist)):                    # For every name in the list of names.
        if i == len(inlist) - 2:                    # If it's the second last word.
            if len(inlist) > 2:
                liststring += inlist[i] + ", " + finalstr + " "     # Append the finalstr for neatness.
            else:
                liststring += inlist[i] + " " + finalstr + " "
        elif i == len(inlist) - 1:                  # If it's the last word, just append the word.
            liststring += inlist[i]
        else:                                       # Otherwise, a comma.
            liststring += inlist[i] + ", "
    
    return liststring

def verifyCmd(text):
    """String -> Boolean"""
    
    db.cur.execute("select alias from command where alias = \""+text+"\";")
    
    if db.cur.rowcount > 0:     # At least one row was found, command exists.
        return True
    else:                       # Command not found in command list.
        return False

def cmdStrip(oldlist,alt):
    """List -> List"""
    
    preps = ["the","a","abaft","abeam","aboard","about","above","absent","across","afore","after","against","along","alongside","amid","amidst","among","amongst","an","anenst","apropos","apud","around","as","aside","astride","at","athwart","atop","barring","before","behind","below","beneath","beside","besides","between","beyond","but","by","circa","concerning","despite","during","except","excluding","failing","following","for","forenenst","from","given","in","including","inside","into","like","mid","midst","minus","modulo","near","next","notwithstanding","of","off","on","onto","opposite","outside","over","pace","past","per","plus","pro","qua","regarding","round","sans","since","than","through","thru","throughout","thruout","till","times","to","toward","towards","under","underneath","unlike","until","unto","upon","versus","via","vice","with","within","without","worth"]
    prepsalt = ["the","a","abaft","abeam","aboard","above","absent","across","afore","after","against","along","alongside","amid","amidst","among","amongst","an","anenst","apropos","apud","around","as","aside","astride","at","athwart","atop","barring","before","behind","below","beneath","beside","besides","between","beyond","but","by","circa","concerning","despite","during","except","excluding","failing","following","for","forenenst","from","given","in","including","inside","into","like","mid","midst","minus","modulo","near","next","notwithstanding","off","onto","opposite","outside","over","pace","past","per","plus","pro","qua","regarding","round","sans","since","than","through","thru","throughout","thruout","till","times","toward","towards","under","underneath","unlike","until","unto","upon","versus","via","vice","within","without","worth"]
    newlist = []
    
    for word in oldlist:                # For every word in the input list.
        if not alt:                     # Do not use alternate list that doesn't have to and about?
            if word not in preps:       # Current word not a preposition. If it is, do nothing.
                newlist.append(word)    # Add word to newlist.
        else:
            if word not in prepsalt:
                newlist.append(word)
        
    return newlist                      # Return the new list without prepositions.

def expandCmd(plinput):
    """Alias to command. Returns a word list."""
    
    if len(plinput) > 0:                                    # Something was input.
        if verifyCmd(plinput):                                 # The function returns True if the command exists. Do the thing!
            return g.cmdlist[g.cmdalias.index(plinput)]     # Replace player input command alias with the real command.
        else:                                               # Unknown command.
            sysmsg.show("invalidcmd",plinput[0])
    else:                                                   # Nothing was input.
        sysmsg.show("emptycmd")    

def parse(plinput):
    """String -> List."""
    wordlist = sanitize(plinput)   # Sanitize player input, take out whitespace, return a list of words.
    
    if len(wordlist) > 0:                                   # Something was input.
        if verifyCmd(wordlist[0]):                             # The function returns True if the command exists.
            func = expandCmd(wordlist.pop(0))               # Delete data from list at index 0. Place data into variable func.
            
            if func not in g.multiArgCmds:     # Some special cases.
                wordlist = cmdStrip(wordlist,False)
            else:
                wordlist = cmdStrip(wordlist,True)                     # Use alternate stripping for these commands.
            
            if g.debug:
                    print("[DBG] parse STRIPPED INPUT:",func,wordlist)
                
            if func != "quit" and func != "help":           # Special cases are needed because "quit" and "help" are Python reserved name.
                if wordlist:                                # Returns True is wordlist is not empty.
                    #try:                                    # Try to do: getattr(cmd, func)(wordlist)
                    getattr(cmd, func)(wordlist)        # Is the same as: cmd.func(wordlist)
                    #except AttributeError:                  # getattr(cmd, func)(wordlist) failed with a Python error, do this instead:
                    #    sysmsg.show("unimplementedcmd",func)
                else:                                       # wordlist is empty so we're calling the function with no arguments since none were given.
                    #try:                                    # Try to do: getattr(cmd, func)()
                    getattr(cmd, func)()                # Is the same as: cmd.func() | For example the user input "look" will call the function named "look" in cmd.py with no arguments.
                    #except AttributeError:                  # getattr(cmd, func)() failed with a Python error, do this instead:
                    #    sysmsg.show("unimplementedcmd",func)
            elif func == "help":    # Help command.
                cmd.helpcmd(wordlist)
            elif func == "quit":    # Quit command.
                cmd.quitgame()
            else:
                sysmsg.show("cmdcheck")
        else:                   # Unknown command.
            sysmsg.show("invalidcmd",wordlist[0])
    else:                       # Nothing  was input.
        sysmsg.show("emptycmd")

def printFC(text,width=g.columnWidth):
    """Doesn't work because of newlines: Remove spaces from start of line, if there are any."""
    text = str(text)
    length = len(text)
    i = 0
    
    if length > width:
        divs = int(math.floor(length/width))
        
        while i <= divs:
            if text[i*width-1] == " " and text[i*width] != " ":
                text = text[:width] + "" + text[(width+1):]
            i += 1
    print(text)