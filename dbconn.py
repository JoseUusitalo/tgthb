import mysql.connector
import initialize
import globalvars as g

try:
    db = mysql.connector.connect(host="localhost",user="tgthbdbusr",passwd="tgthbdbpass",db="TGTHB",buffered=True)
    cur = db.cursor()
    
    if g.debug:
        print("[MYSQL] Database connection created. Connection open.")
    
    # It sucks but this is executed every time anything with the database is done. Definitely not ideal.
    cur.execute("select * from command;")
    if cur.rowcount < 1:
        if g.debug:
            print("[MYSQL] Data missing. Inserting data.")
        initialize.Data()
        db.commit()

except mysql.connector.ProgrammingError as e:
    if e.errno == 1049:
        print("Please run the included user.sql to create the database and the database user in order to play this game.")
    elif e.errno == 1146:
        initialize.Database()
        initialize.Data()
    else:
        print("[MYSQL] MYSQL CONNECTOR ERROR: {}".format(e))
