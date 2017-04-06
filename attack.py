import dbconn as db
import parse
import find
import ask

def attack(*args):
    objectid = parse.checkArgs(args,"Who do you want to attack?","","attack")
    
    if objectid:
        person = find.idFromName(objectid,"people")
            
        while len(person) > 1:
            print(person)
            person = ask.which(person,"people")
        
        if person:
            db.cur.execute("update people set hp = hp-10 where charid = \""+person[0]+"\";")
            name = find.nameFromID(person,"people")
            print("You gave",name[0], "a black eye.")
            
        else:
            print("Stop waving your hands around pointlessly!")