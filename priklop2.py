#!/usr/bin/python
# -*- encoding: utf-8 -*-


# uvozimo bottle.py
from bottle import *
import hashlib

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

debug(True)

import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

def rtemplate(*largs, **kwargs):
    """
    Izpis predloge s podajanjem spremenljivke ROOT z osnovnim URL-jem.
    """
    return template(ROOT=ROOT, *largs, **kwargs)

#==================================================================================

static_dir = "./static"

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)


@get('/')
def index():
    return rtemplate('home.html')

@get('/zacetna_stran/')
def zacetna_get():  
    return redirect('/')


@get('/prijava')
def prijavno_okno():
    return rtemplate('prijava.html')

@get('/zavrnjeno')
def zavrnjeno_okno():
    return rtemplate('home.html')

@get('/odjava')
def prijavno_okno():
    return rtemplate('home.html')

    
@post('/prijava') # or @route('/prijava', method='POST')
def prijava():
    uime = request.forms.get('uime')
    geslo = request.forms.get('geslo')
    if preveri(uime, geslo):
        return rtemplate('home2.html')
    else:
        return rtemplate('dostop.html')

def preveri(uime, geslo):
    return uime=="js" and geslo=="123"

@get('/kinoti')
def kinoti():
    cur.execute("SELECT * FROM kino")
    return rtemplate('kinoti.html', kino=cur)

@get('/kinoti/<x:int>')
def kinoti():
    cur.execute("SELECT * FROM kino WHERE ime == %s", [x])
    return rtemplate('kinoti.html', kino=cur)

@get('/na_voljo')
def na_voljo():
    cur.execute("SELECT * FROM na_voljo")
    return rtemplate('na_voljo.html', na_voljo=cur)

@get('/karte')
def karte():
    cur.execute("SELECT * FROM karta")
    return rtemplate('karta.html', karta=cur)

@get('/prigrizek1/<x:int>')
def prigrizek(x):
    cur.execute("SELECT * FROM prigrizek WHERE cena < %s", [x])
    return rtemplate('prigrizek.html', prigrizek=cur)

@get('/prigrizek2/<x:int>')
def prigrizek(x):
    cur.execute("SELECT * FROM prigrizek WHERE cena > %s", [x])
    return rtemplate('prigrizek.html', prigrizek=cur)


@get('/dvorane/') 
def dvorane():
    cur.execute("SELECT * FROM dvorana")
    return rtemplate('dvorana.html', dvorana=cur)

@get('/vrti')
def vrti():
    cur.execute("SELECT * FROM vrti")
    return rtemplate('vrti.html', vrti=cur)

##@get('/film') 
##def film():
##    cur.execute("SELECT * FROM film")
##    return rtemplate('film.html', film=cur)

@get('/filmi1/<x:int>') 
def filmi(x):
    cur.execute("SELECT * FROM film WHERE ocena < %s", [x])
    return rtemplate('film.html', film=cur)

@get('/filmi2/<x:int>') 
def filmi(x):
    cur.execute("SELECT * FROM film WHERE ocena > %s", [x])
    return rtemplate('film.html', film=cur)


@get('/zanr') 
def vrti():
    cur.execute("SELECT * FROM zanr")
    return rtemplate('zanr.html', zanr=cur)

@get('/ima_zanr') 
def vrti():
    cur.execute("SELECT * FROM ima_zanr")
    return rtemplate('ima_zanr.html', ima_zanr=cur)


#===============================================================================
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#
# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
#run(host='localhost', port=SERVER_PORT, debug(True))
run(host='localhost', port= SERVER_PORT)
