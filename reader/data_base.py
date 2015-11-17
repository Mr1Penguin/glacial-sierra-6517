import psycopg2

conn = 0
curr = 0

def activate_base():
    try :
        global conn
        global curr
        conn = psycopg2.connect("dbname='mnreader' user='mpreader' password='MPreader'")
        curr = conn.cursor()
    except Exception, e:
        print "Igor is mooooodaq. Well played."
        psycopg2.errorcodes.lookup(e.pgcode)
