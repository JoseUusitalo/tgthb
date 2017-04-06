import dbconn as db
import find
import parse
import globalvars as g
import item
import get
import cmd
import gameOver
import ask

# None of the function arguments are lists unless specified!
# The ifs are nested in a futile attempt to shave a nanosecond or two off execution time since these checks are done every command, which is less than ideal.

def topicSwitch(disableid="",enableid="",enableTopic=""):
    db.cur.execute("update dialogue set topic = NULL where dlgid = \""+disableid+"\";")
    db.cur.execute("update dialogue set topic = \""+enableTopic+"\" where dlgid = \""+enableid+"\";")

    if g.debug:
        print("[DBG] action.topicSwitch DISABLED ENABLED TOPIC:",disableid,enableid,enableTopic)
    
def setVis(locid,vis):
    """locid = String | vis = 0/1"""
    
    db.cur.execute("update location set vis = \""+str(vis)+"\" where locid = \""+locid+"\";")

    if g.debug:
        print("[DBG] action.setVis:",locid,vis)
    
def getVis(locid):
    """locid = String"""
    
    db.cur.execute("select vis from location where locid = \""+locid+"\";")
    vis = db.cur.fetchall()[0][0]
    
    if g.debug:
        print("[DBG] action.getVis:",locid,vis)
    
    if vis == 1:    # MySQL booleans return integers.
        return True
    else:
        return False

def checkTopic(dlgid):
    """Returns True if topic is enabled. False for not.
    
    dlgid = String"""
    
    db.cur.execute("select topic from dialogue where dlgid = \""+dlgid+"\";")
    
    if db.cur.fetchall()[0][0] != None:
        return True
    else:
        return False

def buy(itemid,charid):
    if g.debug:
        print("[DBG] action.buy ARGUMENTS:",itemid,charid)
    
    if charid == "intimast":
        if itemid == "tick1" or itemid == "tick2" or itemid == "tick3":
            print(get.dlg("intiwelc"))
            setVis("intrro7",1)
            setVis("intrains",0)
            setVis("nejaratr",0)
            db.cur.execute("update people set locid = \"intrro7\" where charid = \"player\";")
            cmd.look()

def call(charid):
    
    if charid == "spgorka" and g.spgorCalled == "0":
            print(get.dlg("gorcall"))
            db.cur.execute("update save set val = 1 where var = \"spgorCalled\";")
            g.update()
    
    elif charid == "pewayna" and g.spgorCalled == "1":
            if g.pewayCalled == "0":
                print(get.dlg("waycall1"))
                db.cur.execute("update save set val = 1 where var = \"pewayCalled\";")
                g.update()
                db.cur.execute("update people set locid = \"pecusco\" where charid = \"pewayna\";")
    
    else:
        print(get.text("nophone"))

def examine(loc):
    if g.debug:
        print("[DBG] action.examine:",loc)
    
    if loc == "bueleusa":
        if g.buMartFind == "0":
            db.cur.execute("update save set val = 1 where var = \"buMartFind\";")
            g.update()
            print(get.text("exaeleus"))
            db.cur.execute("update item set locid = \"bueleusa\" where itemid = \"martenit\";")
        
    elif loc == "timount":
        print(get.text("examount"))
        db.cur.execute("update location set vis = 1 where locid = \"tioutmon\";")
    
    elif loc == "grfors":
        if g.grforSkin == "0":
            db.cur.execute("update save set val = 1 where var = \"grforSkin\";")
            g.update()
            print(get.text("exafores"))
            db.cur.execute("update item set locid = \"grfors\" where itemid = \"linskin\";")
    
    elif loc == "grbay":
        print(get.text("shipunde"))

    else:
        print(get.text("exanone"))

def give(itemid,charid):
    if g.debug:
        print("[DBG] action.give:",itemid,charid)
    
    if itemid == "budagger":
        if charid == "spgorka":
            print(get.dlg("gornotme"))
            item.transfer(["budagger"],["player"],["spgorka"],"give")
    
    if itemid == "zlatlett":
        if charid == "spgorka":
            print(get.dlg("gorsupr"))
            topicSwitch("gorhelp","gorlet2","Letter")
            
            if g.spletterRead == "0":
                print(get.dlg("gorwoah"))
                print(get.text("letter"))
                db.cur.execute("update save set val = 1 where var = \"spletterRead\";")
                g.update()
                setVis("grport",1)
    
    if itemid == "martenit":
        if charid == "bumonica":
            print(get.dlg("moniretu"))
            topicSwitch("monica3")
            topicSwitch("mongreet","monica2","Zlatin Panayotov")
    
    if itemid == "fishnet":
        if charid == "tifisher":
            print(get.dlg("tifithan"))
            topicSwitch("fisher1")
            setVis("tipumqu1",1)
    
    if itemid == "pet":
        if charid == "tizlatin":
            print(get.dlg("zlapet2"))
            topicSwitch("zlapet")
            item.transfer(["fjorstei"],["player"],["tizlatin"],"give")   
    
    if itemid == "kolbswor":
        if charid == "grkolbio":
            print(get.dlg("kolthank"))
            topicSwitch("kolrule","kolexch","Hrosskell")
    
    if itemid == "mead":
        if charid == "grlone":
            print(get.dlg("lonesea1"))
            print(get.dlg("lonep1"))
            print(get.dlg("lonemor1"))
    
    if itemid == "mead2":
        if charid == "grlone":
            print(get.dlg("lonesea2"))
            print(get.dlg("lonep2"))
            print(get.dlg("lonemor2"))
    
    if itemid == "mead3":
        if charid == "grlone":
            print(get.dlg("lonesea3"))
            print(get.dlg("lonep3"))
            topicSwitch("","grsail2","Melville Bay")
            setVis("grbay",1)
            
            if g.debug:
                print("[DBG] GRBAY VIS:",getVis("grbay"))
            
    if itemid == "linskin":
        if charid == "grvolur":
            item.transfer(["necklace"],["player"],["grvolur"],"give")
            topicSwitch("volneck")
    
    if itemid == "necklace":
        if charid == "grjens":
            if "kolbswor" in find.listInvItemIDs(["grjens"]):
                print(get.dlg("jensgive"))
                item.transfer(["kolbswor"],["player"],["grjens"],"give")
                topicSwitch("jensword")
                
                if g.Chapters == "1":
                        print("\n                 ----    Chapter VII: Call of the Inca    ----\n")
    
    if itemid == "divesuit":
        if charid == "grportma":
            print(get.dlg("grmawork"))
            db.cur.execute("update people set val = val - 500 where charid = \"grportma\";")
            db.cur.execute("update people set val = val + 500 where charid = \"player\";")
    
    if itemid == "fjorstei":
        if charid == "spgorka":
            print(get.dlg("gorfjo"))
            
            if ask.yn():
                print(get.dlg("gormore"))
                topicSwitch("","gordone","Artifacts")
            else:
                print("\n                    ----    Chapter IX: Fame & Glory    ----\n")
                gameOver.End("artifacts")
    
    if itemid == "guthjorr":
        if charid == "spgorka":
            print(get.dlg("gorgut"))
            
            if ask.yn():
                print(get.dlg("gormore"))
                topicSwitch("","gordone","Artifacts")
            else:
                print("\n                    ----    Chapter IX: Fame & Glory    ----\n")
                gameOver.End("artifacts")
    
    if itemid == "viksword":
        if charid == "spgorka":
            print(get.dlg("gorrep"))
            
            if ask.yn():
                print(get.dlg("gormore"))
                topicSwitch("","gordone","Artifacts")
            else:
                print("\n                    ----    Chapter IX: Fame & Glory    ----\n")
                gameOver.End("artifacts")
    
    if itemid == "necklace":
        if charid == "spgorka":
            print(get.dlg("gornec"))
            
            if ask.yn():
                print(get.dlg("gormore"))
                topicSwitch("","gordone","Artifacts")
            else:
                print("\n                    ----    Chapter IX: Fame & Glory    ----\n")
                gameOver.End("artifacts")
    
def greet(charid):
    db.cur.execute("select txt from dialogue where topic = \"Greet\" and charid = \""+charid+"\";")
    
    try:
        result = parse.tupleListToList(db.cur.fetchall())
        print(result[0])
    except IndexError:
        print(find.nameFromID([charid],"people")[0]+" ignores you.")
    
    if charid == "grdead":
        if g.grkolbOut == "0":
            db.cur.execute("update save set val = 1 where var = \"grkolbOut\";")
            g.update()
            db.cur.execute("update people set locid = \"grship\" where charid = \"grkolbio\";")
            topicSwitch("grdedgre")

    if charid == "pewayna":
        if checkTopic("waygreet"):
            print(get.dlg("waymyth"))
            topicSwitch("waygreet","waygre2","Greet")
            setVis("pevillag",1)

def move(locid):
    
    if locid in g.buylocs:
        get.storeItems(locid)
    
    if locid == "intrrest":
        if g.inTrainRobbed == "0":
            db.cur.execute("update save set val = 1 where var = \"inTrainRobbed\";")
            g.update()
            print(get.text("robresta"))
            db.cur.execute("update people set locid = \"intrrest\" where name = \"Robber\";")
    
    if locid == "intrsle1":
        if g.inTrainRobbed == "1" and g.inTrainRobDone == "0":
            print(get.text("robescap"))
            setVis("intrrest",0)    # I don't want to make another global variable for this.
            
    if locid == "intrro2":
        if g.inTrainRobbed == "1" and g.inTrainRobDone == "0":
            print(get.text("robhide"))
            db.cur.execute("update save set val = 1 where var = \"inTrainRobDone\";")
            g.update()
            db.cur.execute("update people set locid = NULL where name = \"Robber\";")
            setVis("nejaratr",1)
            setVis("intrsle2",1)
            setVis("intrrest",1)
    
    if locid == "intrsle2":
        if g.inTrainRobbed == "1" and g.inTrainRobDone == "0":
            print(get.text("robburst"))
            db.cur.execute("update people set locid = \"intrsle2\" where charid = \"inrob1\";")
            setVis("intrsle2",0)    # I don't want to make another global variable for this.
            
    if locid == "intrro7":
        if g.inTrainRobbed == "1" and g.inTrainRobDone == "0":
            gameOver.slowPrint(get.text("killrob1"),0.03)
            gameOver.End("death")
    
    if locid == "tipumqu1" or locid == "tipumqu2" or locid == "tipumqu3":
        print(get.text("tifiboat"))
    
    if locid == "titserom" and g.zlaGreet == "0":
        print(get.dlg("zlagreet"))
        db.cur.execute("update save set val = 1 where var = \"zlaGreet\";")
        g.update()
    
    if locid == "gredgecr":
        if g.wolvesGuided == "1":
            if g.grShamanMeet == "0":
                print(get.text("wolftrai"))
                db.cur.execute("update people set locid = \"grlair2\" where name = \"Tribal Wolf\";")
    
    if locid == "grlair2":
        if g.grShamanMeet == "0":
            db.cur.execute("update save set val = 1 where var = \"grShamanMeet\";")
            g.update()
    
    if locid == "pepost":
        print(get.text("phonthin"))
    
def rent(itemid,seller,room=False):
    if g.debug:
        print("[DBG] action.rent:",itemid,seller,room)
    
    if itemid == "divesuit":
        print(get.text("usesuit"))
        setVis("grship",1)
    elif room:
        db.cur.execute("select name,dsc from location where locid =\"grinnroo\";")
        locs = parse.multiTupleListToList(db.cur.fetchall())
        print(locs)
        print("\n"+locs[0]+"\n"+locs[1])
        print(get.text("sleepinn"))
        setVis("grjensho",1)

def say(inputlist,loc):
    if loc == "grfornw":
        words = ["mother","father","master","leader","chief"]
        if inputlist[0] in words:
            if g.wolvesGuided == "0":
                print("\nYou say the words \""+parse.liToStr(inputlist)+"\". The ears of both wolves perk up and they freeze. They slowly walk towards you and the other one lets out a slight howl. They brush your knees as they walk past you towards the edge of the crater. You turn around and see the wolves staring at you, waiting.\n")
                db.cur.execute("update save set val = 1 where var = \"wolvesGuided\";")
                g.update()
                db.cur.execute("update people set locid = \"gredgecr\" where name = \"Tribal Wolf\";")
                setVis("grlair1",1)
    
    if inputlist[0] == "cheat":
        if len(inputlist) > 1:
            if inputlist[1] == "loadsamoney":
                print("MONEY MONEY MONEY")
                db.cur.execute("update people set val = val + 1000000 where charid = \"player\";")
                #g.cheatsUsed += 1
            
    if inputlist[0] == "dev":
        #if inputlist[0] == "eval":
        #    eval(input("EVAL: "))
    
        #if inputlist[0] == "exec":
        #    exec(input("EXEC: "))
        
        if inputlist[1] == "debug":
            g.toggleDebug()
            print("[DEV] Debug messages toggled.")
        
        if inputlist[1] == "win":
            gameOver.End("immortality")
        
        if inputlist[1] == "tele":
            db.cur.execute("select locid from location;")
            ids = parse.multiTupleListToList(db.cur.fetchall())
            
            if inputlist[2] in ids:
                print("WOOPWOOPWOOP")
                db.cur.execute("update people set locid = \""+inputlist[2]+"\" where charid = \"player\";")
                cmd.look()
                #g.cheatsUsed += 1
            else:
                print("[DEV] locid \""+inputlist[2]+"\" not found.")
        
        if inputlist[1] == "get":
            print("GET OVER HERE")
            empty = find.invSlotByItemID(None)
            
            db.cur.execute("select itemid from item;")
            ids = parse.multiTupleListToList(db.cur.fetchall())
            
            if inputlist[2] in ids:
                if empty != 0:
                    db.cur.execute("update inventory set item"+str(empty)+" = \""+inputlist[2]+"\";")
                    #g.cheatsUsed += 1
                else:
                    print("[DEV] INVENTORY FULL")
            else:
                print("[DEV] itemid \""+inputlist[2]+"\" not found.")

        if inputlist[1] == "vis":
            print("ICANSEEDEADPEOPLE")
            db.cur.execute("update location set vis = 1;")
            print("[DEV] All locations visible.")

def shoot(charid):
    if charid == "inrob1" or charid == "inrob2" or charid == "inrob3":
        if find.plLoc() == "intrrest":
            gameOver.slowPrint(get.text("killrob2"),0.03)
            gameOver.End("death")
        elif find.plLoc() == "intrsle2":
            gameOver.slowPrint(get.text("killrob3"),0.03)
            gameOver.End("death")
    
    if charid == "tarhino":
        if find.plLoc() == "tanatr3":
            topicSwitch("chief1","chief2","Lake Monster")
    
    if charid == "grwolf" or charid == "grwolf2":
        if find.plLoc() == "grlair2":
            gameOver.slowPrint(get.text("killvolu"),0.03)
            gameOver.End("death")

    if charid == "grkolbio":
        print(get.text("kolpleas"))
    
    if charid == "peghost":
        print(get.text("peghhaha"))
    
    if charid == "peskele":
        print(get.text("skelboom"))

def talk(charid,dlgid):
    if g.debug:
        print("[DBG] action.talk:",charid,dlgid)
    
    if charid == "spgorka":
        if dlgid == "gorhelp":
            if ask.yn():
                if "budagger" in find.listInvItemIDs():
                    print(get.dlg("gorhhold"))
                    
                    if ask.yn():
                            print(get.dlg("gorhh2"))
                            print(get.text("gordagg"))
                            topicSwitch("gorhelp")
                            
                            if g.spletterDropped == "0":
                                db.cur.execute("update save set val = 1 where var = \"spletterDropped\";")
                                g.update()
                                db.cur.execute("update item set locid = \""+find.plLoc()+"\" where itemid = \"zlatlett\";")
                    else:
                        print(get.dlg("gorhh3"))
                        print(get.text("gordagg"))
                        topicSwitch("gorhelp")
                        
                        if g.spletterDropped == "0":
                            db.cur.execute("update save set val = 1 where var = \"spletterDropped\";")
                            g.update()
                            db.cur.execute("update item set locid = \""+find.plLoc()+"\" where itemid = \"zlatlett\";")
                else:
                    print(get.dlg("gornodag"))
            else:
                print(get.dlg("gorsigh"))
        
        if dlgid == "gorlet2":
            db.cur.execute("update people set val = val + 4125 where charid = \"player\";")
            topicSwitch("gorlet2")
            topicSwitch("gorgreet","gorgre2","Greet")
            setVis("buairpor",1)
        
        if dlgid == "gordone":
            if ask.yn():
                print(get.dlg("gormore"))
            else:
                gameOver.End("artifacts")
    
    if charid == "bugeorgi":
        if dlgid == "georgi1":      # Traveling
            if item.valTrans(10,["player"],["bugeorgi"]," to take the cab"):
                db.cur.execute("update people set locid = \"bueleusa\" where charid = \"player\";")
                db.cur.execute("update people set locid = \"bueleusa\" where charid = \"bugeorgi\";")
                topicSwitch("georgi1","georgi2","Airport")
                cmd.look()
        if dlgid == "georgi2":
            if item.valTrans(10,["player"],["bugeorgi"]," to take the cab"):
                db.cur.execute("update people set locid = \"buairpor\" where charid = \"player\";")
                db.cur.execute("update people set locid = \"buairpor\" where charid = \"bugeorgi\";")
                topicSwitch("georgi2","georgi1","Eleusa Monastery")
                cmd.look()
    
    if charid == "bumonica":
        if dlgid == "monica2":
            setVis("inairpor",1)
    
    if charid == "timonk2":
        if dlgid == "monk2":
            setVis("timonyar",1)
    
    if charid == "tizlatin":
        if dlgid == "zlagem":
            if ask.yn():
                print(get.dlg("zlamyth"))
            else:
                print(get.dlg("zlanmyth"))
                item.transfer(["vikbok2"],["player"],["tizlatin"],"give")
            topicSwitch("zlagem","zlapet","Fjörsteinn")
        
        if dlgid == "zlapet":
            setVis("taairpor",1)
            setVis("taport",1)
    
    if charid == "taneema":
        if dlgid == "neema":
            db.cur.execute("update people set locid = \"taarusha\" where charid = \"player\";")
            db.cur.execute("update people set locid = \"taarusha\" where charid = \"taneema\";")
            topicSwitch("neema","neema1","Airport")
            cmd.look()
        if dlgid == "neema1":
            db.cur.execute("update people set locid = \"taoutair\" where charid = \"player\";")
            db.cur.execute("update people set locid = \"taoutair\" where charid = \"taneema\";")
            topicSwitch("neema1","neema","Lake Natron")
            cmd.look()
    
    if charid == "tachief":
        if dlgid == "chief2":
            item.transfer(["pet"],["player"],["tachief"],"give")
            topicSwitch("chief2")
            db.cur.execute("update save set val = 1 where var = \"backToIndia\";")
            g.update()

    if charid == "grjens":
        if dlgid == "jensword":
            if ask.yn():
                if item.valTrans(1200,["player"],["grjens"]," to buy the sword"):
                    item.transfer(["kolbswor"],["player"],["grjens"],"buy",1200)
                    print(get.dlg("jensty"))
                    topicSwitch("jensword")
                    
                    if g.Chapters == "1":
                        print("\n                 ----    Chapter VII: Call of the Inca    ----\n")  # Oh my goodness I didn't even realize the pun when I came up with this title.
            else:
                print(get.dlg("jensalt"))
                if g.Chapters == "1":
                    print("\n                ----    Chapter VI: Necklace of a Shaman    ----\n")
    
    if charid == "grsailor":
        if dlgid == "grsail2":      # Traveling
            if item.valTrans(70,["player"],["grsailor"]," to sail"):
                db.cur.execute("update people set locid = \"grbay\" where charid = \"player\";")
                db.cur.execute("update people set locid = \"grbay\" where charid = \"grsailor\";")
                topicSwitch("grsail2","grsail3","Back to Port")
                cmd.look()
                print(get.text("shiphere"))
        if dlgid == "grsail3":
            db.cur.execute("update people set locid = \"grport\" where charid = \"player\";")
            db.cur.execute("update people set locid = \"grport\" where charid = \"grsailor\";")
            topicSwitch("grsail3","grsail2","Melville Bay")
            cmd.look()
    
    if charid == "grkolbio":
        if dlgid == "kolrule":      # Tell about stolen sword.
            db.cur.execute("update people set locid = NULL where charid = \"grlone\";")
            topicSwitch("","innlone","Lone Patron")
        
        if dlgid == "kolexch":      # Player asks about stuff.
            db.cur.execute("update people set locid = NULL where charid = \"grkolbio\";")
            topicSwitch("kolexch")
            setVis("peport",1)
    
    if charid == "grinnkee":
        if dlgid == "innlone":          # Tell about Jens.
            topicSwitch("","innroom1","Room")

    if charid == "pecook":
        if dlgid == "deusexma":         # LET THERE BE TREASURE!
            topicSwitch("deusexma")
            setVis("pecave2",1)         # Why would you pick it up?
    
def take(itemid):
    if g.debug:
        print("[DBG] action.take",itemid)
    
    if itemid == "viksword":
        db.cur.execute("select hp from people where charid = \"peskele\";")
        hp = db.cur.fetchall()[0][0]
        
        if g.debug:
            print("[DBG] action.take SKELETON HP",hp,type(hp))
        
        if hp != 0:
            gameOver.slowPrint(get.text("killskel"),0.03)
            gameOver.End("death")
    
def travel(fromid,toid):
    if g.debug:
        print("[DBG] action.travel",fromid,toid)
        
    if toid == "nejaratr":
        if fromid == "intrro7":
            setVis("intrains",1)
    
    if toid == "grport":
        if g.grFisherCrater == "0":
            print(get.text("grwelcom"))
            db.cur.execute("update save set val = 1 where var = \"grFisherCrater\";")
            g.update()

    if toid == "pecave" or toid == "pecave2":
        if fromid == "pevillag":
            db.cur.execute("update people set locid = NULL where charid = \"pecook\";")   # Aaaand woosh he goes!

def use(obj1,obj2=""):
    if obj1 == "budagger" and obj2 == "archtool" or obj1 == "archtool" and obj2 == "budagger":
            print(get.text("archdagg"))
    
    elif obj1 == "budagger":
        if g.spletterDropped == "0":
            db.cur.execute("update save set val = 1 where var = \"spletterDropped\";")
            g.update()
            print(get.text("usedagg"))
            db.cur.execute("update item set locid = \""+find.plLoc()+"\" where itemid = \"zlatlett\";")
            topicSwitch("gorhelp")
                
    elif obj1 == "zlatlett" and obj2 == "dicnorse" or obj2 == "zlatlett" and obj1 == "dicnorse":
        db.cur.execute("update save set val = 1 where var = \"spletterRead\";")
        g.update()
        print(get.text("letter"))
        setVis("buairpor",1)
    
    elif obj1 == "zlatlett":
        print(get.text("uselett"))
    
    elif obj1 == "dicnorse":
        print(get.text("dictonor"))
    
    elif obj1 == "archtool":
        print(get.text("usearch"))
        
    elif obj1 == "vikbok1" or obj1 == "vikbok2":
        print(get.text("vikbook"))
        setVis("grport",1)
    
    elif obj1 == "viksword" and obj2 == "archtool" or obj1 == "archtool" and obj2 == "viksword":    # Somehow the game became a test in the player's attention span and reading comprehension.
        print(get.text("archfake"))
    
    elif obj1 == "viksword" and obj2 == "altar" or obj1 == "altar" and obj2 == "viksword":          # This idea was a bit more obvious in the original story.
        print(get.text("innuendo"))
        db.cur.execute("update item set locid = \"pecave\" where itemid = \"guthjorr\";")
        
        slot = find.invSlotByItemID(["viksword"])
        db.cur.execute("update inventory set item"+str(slot)+" = NULL where charid = \"player\";")  # Making another global variable is such a drag.
    
    elif obj1 == "viksword":
        print("This artifact is most certainly very interesting but looks like an ordinary sword on the surface.")
    
    elif obj1 == "guthjorr" and obj2 == "fjorstei" or obj1 == "fjorstei" and obj2 == "guthjorr":    # ENDING 1
        print("\n                    ----    Chapter X: Engiandlátæv    ----\n")
        gameOver.End("immortality")
    
    else:
        print(get.text("archbleh"))
