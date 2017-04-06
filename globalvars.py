import dbconn as db

# These are variables that are needed across several functions and py files.

debug = False
rungame = True      # For game loop.
cmdalias = []       # List of command aliases.
cmdlist = []        # List of commands the aliases point to.
columnWidth = 80
essentialPeople = ["bugeorgi","bumonica","grinnkee","grjens","grkolbio","grlone","grportma","grsailor","grvolur","inbusdri","nesherpa","pecook","pewayna","player","spgorka","tachief","taneema","tifisher","timonk2","tizlatin"]
#callLocs = ["grpost","inpost","pepost","tapost","spdiroff"] # Locations where it is possible to call people.
callLocs = ["pepost"]                                   # Locations where it is possible to call people.
callPeople = ["spgorka","pewayna"]                      # People that can be called.
buylocs = ["intrains","nehikesh","grstore","grinn1"]    # Order matters!
buyppl = ["intimast","inshopke","grstore","grinnkee"]   # Order matters!
multiArgCmds = ["give","talk","use","travel"]
rentlocs = ["grmaster","grinn1"]    # Order matters!
rentppl = ["grportma","grinnkee"]   # Order matters!
#turns = 0
#cheatsUsed = 0
immortals = ["grkolbio","peghost"]
cmdMovement = ["north","northeast","east","southeast","south","southwest","west","northwest","up","down","travel"]
cmdInteraction = ["attack","buy","call","drop","examine","give","greet","rent","say","shoot","take","talk","use"]
cmdNoArgs = ["inventory","load","look","quit","restart","save","tips"]
worldTravel = ["buairpor","grport","inairpor","peairpor","peport","spairpor","spport","taport","taairpor"]
countries =  ["Bulgaria","Greenland","India","Peru","Peru","Spain","Spain","Tanzania","Tanzania"]
asiaTravel = ["inbussta","intrains","intrro7","nejaratr","netoti","titone"]
asiaCountries =  ["India","India","India","India","Nepal","Nepal","Tibet"]

# So the player doesn't screw themselves over.
criticalItem = ["budagger","divesuit","fishnet","fjorstei","guthjorr","kolbswor","linskin","martenit","mead","mead2","mead3","necklace","pet","viksword","zlatlett"]
criticalItemPeople = ["spgorka","grportma","tifisher","spgorka","spgorka","grkolbio","grvolur","bumonica","grlone","grlone","grlone","grjens","tizlatin","spgorka","spgorka"]

def killLoop():
    global rungame
    
    rungame = False
    
def initCmdList():      # Initialize command list for later.
    global cmdalias
    global cmdlist
    
    db.cur.execute("select alias,cmd from command;")
    result = db.cur.fetchall()

    for row in result:
        cmdalias.append(row[0])
        cmdlist.append(row[1])
    
    if debug == "verbose":      # No need to print these.
        print("[DBG] globalvars CMDLIST",cmdlist)
        print("[DBG] globalvars CMDALIAS",cmdalias)

def toggleDebug():
    global debug
    
    if debug:
        debug = False
    else:
        debug = True

# I need to initialize all the variables. They are updated with the real values in the function.

savedTurns = 0
wolvesGuided = 0
wearDiveSuit = 0
grFisherCrater = 0
Chapters = 0
firstBulgaria = 0
inTrainRobbed = 0
inTrainRobDone = 0
inTrainBack = 0
spletterRead = 0
zlaGreet = 0
firstTanz = 0
firstPeru = 0
backToIndia = 0
spletterDropped = 0
grkolbOut = 0
buMartFind = 0
grforSkin = 0
grShamanMeet = 0
spgorCalled = 0
pewayCalled = 0
gameSaved = 0

def update():
    global savedTurns
    global wolvesGuided
    global wearDiveSuit
    global grFisherCrater
    global Chapters
    global firstBulgaria
    global inTrainRobbed
    global inTrainRobDone
    global inTrainBack
    global spletterRead
    global zlaGreet
    global firstTanz
    global firstPeru
    global backToIndia
    global spletterDropped
    global grkolbOut
    global buMartFind
    global grforSkin
    global grShamanMeet
    global spgorCalled
    global pewayCalled
    global gameSaved
    
    db.cur.execute("select val from save where var = \"turns\";")
    savedTurns = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"wolvesGuided\";")
    wolvesGuided = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"wearDiveSuit\";")
    wearDiveSuit = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"grFisherCrater\";")
    grFisherCrater = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"chapters\";")
    Chapters = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"firstBulgaria\";")
    firstBulgaria = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"inTrainRobbed\";")
    inTrainRobbed = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"inTrainRobDone\";")
    inTrainRobDone = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"inTrainBack\";")
    inTrainBack = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"spletterRead\";")
    spletterRead = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"zlaGreet\";")
    zlaGreet = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"firstTanz\";")
    firstTanz = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"firstPeru\";")
    firstPeru = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"backToIndia\";")
    backToIndia = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"spletterDropped\";")
    spletterDropped = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"grkolbOut\";")
    grkolbOut = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"buMartFind\";")
    buMartFind = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"grforSkin\";")
    grforSkin = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"grShamanMeet\";")
    grShamanMeet = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"spgorCalled\";")
    spgorCalled = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"pewayCalled\";")
    pewayCalled = db.cur.fetchall()[0][0]
    
    db.cur.execute("select val from save where var = \"gameSaved\";")
    gameSaved = db.cur.fetchall()[0][0]