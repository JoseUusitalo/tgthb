import dbconn as db
import globalvars as g
import sysmsg
import parse

def helpcmd(*args):
    if not args[0]:  # Returns True when the list given as argument (which is in the args list in index 0) is empty. In other words the player input help and nothing else.
        print("\nCATEGORIZED COMMAND LIST\n------------------------\nUse \"help <command>\" to see the all the aliases of a specific command or \"help full\" for a full, uncategorized list.\n") # \n is shorthand for new line.
        print("\nMOVEMENT\n--------")
        maxmove = max(len(s) for s in g.cmdMovement)
        maxinter = max(len(s) for s in g.cmdInteraction)
        maxnoargs = max(len(s) for s in g.cmdNoArgs)
        
        for command in g.cmdMovement:
            db.cur.execute("select alias, dsc from command where alias = \""+str(command)+"\";")
            result = db.cur.fetchall()
            
            if db.cur.rowcount > 0:                                     # MySQL query returned something.
                for row in result:
                    
                    spacelist = [" "] * (maxmove - len(row[0]) + 1)  # Create a list filled with " " of length "length of longest command - length of current command + 1".
                    spacer = "".join(str(a) for a in spacelist)        # Concatenate created list into a string to use a spacer when priting.
                    print(row[0]+spacer+row[1])                     # Print a pretty command list.
            else:                                                       # This should not happen.
                sysmsg.show("emptylist")
        
        print("\nINTERACTION\n-----------")
        
        for command in g.cmdInteraction:
            db.cur.execute("select alias, dsc from command where alias = \""+str(command)+"\";")
            result = db.cur.fetchall()
            
            if db.cur.rowcount > 0:                                     # MySQL query returned something.
                for row in result:
                    spacelist = [" "] * (maxinter - len(row[0]) + 1)  # Create a list filled with " " of length "length of longest command - length of current command + 1".
                    spacer = "".join(str(a) for a in spacelist)        # Concatenate created list into a string to use a spacer when priting.
                    print(row[0]+spacer+row[1])                     # Print a pretty command list.
            else:                                                       # This should not happen.
                sysmsg.show("emptylist")
        
        print("\nNO ARGUMENTS\n------------")
        
        for command in g.cmdNoArgs:
            db.cur.execute("select alias, dsc from command where alias = \""+str(command)+"\";")
            result = db.cur.fetchall()
            
            if db.cur.rowcount > 0:                                     # MySQL query returned something.
                for row in result:
                    spacelist = [" "] * (maxnoargs - len(row[0]) + 1)  # Create a list filled with " " of length "length of longest command - length of current command + 1".
                    spacer = "".join(str(a) for a in spacelist)        # Concatenate created list into a string to use a spacer when priting.
                    print(row[0]+spacer+row[1])                     # Print a pretty command list.
            else:                                                       # This should not happen.
                sysmsg.show("emptylist")
        print()                                                         # For clarity.
    
    elif args[0][0] == "full":  # Returns True when the list given as argument (which is in the args list in index 0) is empty. In other words the player input help and nothing else.
        db.cur.execute("select alias, dsc from command;")
        result = db.cur.fetchall()
        
        print("\nFULL COMMAND LIST\n-----------------\nUse \"help <command>\" to see the description of a specific command and it's aliases or just \"help\" for a categorized list.\n") # \n is shorthand for new line.
        
        if db.cur.rowcount > 0:                                     # MySQL query returned something.
            #maxlength = max(len(a[0]) for a in result)              # Get the length of the longest command.
            
            for row in result:
                #spacer = " " * (maxlength - len(row[0]) + 1)        # Create a string filled with spaces "length of longest command - length of current command + 1" times.
                print(row[0]+" : "+row[1]+"\n")                         # Print a pretty command list.
            print()                                                 # For clarity.
        else:                                                       # This should not happen.
            sysmsg.show("emptylist")
    
    elif args[0][0] == "move" or args[0][0] == "movement" or args[0][0] == "moving":          # Special case for the clueless player. args[0][0] refers to the command player wants help with.
        #maxlength = max(len(a) for a in movement)                   # Get the length of the longest command.
        
        for command in g.cmdMovement:
            db.cur.execute("select alias, dsc from command where cmd = \""+str(command)+"\";")
            result = db.cur.fetchall()
            
            if db.cur.rowcount > 0:                                     # MySQL query returned something.
                for row in result:
                    #spacelist = [" "] * (maxlength - len(row[0]) + 1)   # Create a list filled with " " of length "length of longest command - length of current command + 1".
                    #spacer = "".join(str(a) for a in spacelist)         # Concatenate created list into a string to use a spacer when priting.
                    print(row[0]+" : "+row[1]+"\n")                         # Print a pretty command list.
            else:                                                       # This should not happen.
                sysmsg.show("emptylist")
        print()                                                         # For clarity.
    
    else:
        if parse.verifyCmd(args[0][0]):                                        # The function returns True if the command exists.
            command = g.cmdlist[g.cmdalias.index(args[0][0])]
            db.cur.execute("select alias, dsc from command where cmd = \""+str(command)+"\";")
            result = db.cur.fetchall()
            
            if db.cur.rowcount > 1:                                     # MySQL query returned something.
                #maxlength = max(len(a[0]) for a in result)              # Get the length of the longest command.
                
                for row in result:
                    #spacelist = [" "] * (maxlength - len(row[0]) + 1)   # Create a list filled with " " of length "length of longest command - length of current command + 1".
                    #spacer = "".join(str(a) for a in spacelist)         # Concatenate created list into a string to use a spacer when priting.
                    print(row[0]+" : "+row[1]+"\n")                         # Print a pretty command list.
                print()                         # For clarity.
            elif db.cur.rowcount == 1:          # MySQL query returned 1 line.
                for row in result:
                    print(row[0]+" : "+row[1])  # Print the command with a simple spacer.
                print()                         # For clarity.
            else:                               # This should not happen.
                sysmsg.show("emptylist")
        else:                                   # Unknown command.
            sysmsg.show("invalidcmd",args[0][0])