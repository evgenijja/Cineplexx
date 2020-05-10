# uvozimo ustrezne podatke za povezavo
import auth
import time

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import csv

conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def uvoziSQL(datoteka):
    with open("podatki/{}".format(datoteka)) as f:
        koda = f.read()
        cur.execute(koda)
        conn.commit()

#conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
#cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

uvoziSQL('cineplexx.sql')
uvoziSQL('karta.sql')
uvoziSQL('film.sql')
uvoziSQL('prigrizek.sql')
uvoziSQL('kino.sql')
uvoziSQL('dvorana.sql')
uvoziSQL('na_voljo.sql')


