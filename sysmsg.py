def show(msgid, inputtext=None):   # inputtext used when the input command needs to printed.
    # List if system message IDs.
    msgidlist = ["invalidcmd",
                 "emptycmd",
                 "unimplementedcmd",
                 "emptyarg",
                 "nonuniqueid",
                 "nullcmd",
                 "emptylist",
                 "cmdcheck",
                 "wrongid",
                 "invalidtable",
                 "noaction",
                 "notype",
                 "argerror",
                 "notext",
                 "logicerror"]

    # System messages.
    msglist = ["I do not understand \""+str(inputtext)+"\".",
               "Please type a command.",
               "The command "+str(inputtext)+" has not been implemented yet.",
               "Please type some arguments.",
               "FATAL ERROR 1: NON-UNIQUE ID "+str(inputtext)+" FOUND",
               "ERROR 1: INPUT LIST NULL",
               "ERROR 2: MYSQL QUERY RETURNED NOTHING",
               "ERROR 3: COMMAND CHECK FAILED",
               "ERROR 4: INCORRECT ID \""+str(inputtext)+"\"",
               "ERROR 5: INVALID TABLE NAME \""+str(inputtext)+"\"",
               "ERROR 6: UNSPECIFIED ACTION",
               "ERROR 7: INVALID NAME TYPE",
               "ERROR 8: MISSING OR INVALID ARGUMENTS",
               "ERROR 9: TEXT NOT FOUND",
               "ERROR 10: UNEXPECTED LOGICAL OUTCOME"]
    
    if msgid in msgidlist:
        # Print: Content at index in msglist
        # Where: Index = Index of input (msgid variable) in msgidlist
        # msgidlist indexes match msglist indexes making this possible.
        print(msglist[msgidlist.index(msgid)])
    else:
        print("ERROR 0: SYSTEM MESSAGE NOT FOUND")  # I.e. a typo.
