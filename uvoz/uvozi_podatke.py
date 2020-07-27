# uvozimo ustrezne podatke za povezavo
import auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
from psycopg2 import sql
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import csv
import sqlite3

#===================================================================================================

# te funkcije nam naredijo tabele

def izbrisi():
    cur.execute("""
        DROP TABLE IF EXISTS kino CASCADE;
        drop table IF EXISTS prigrizek CASCADE;
        drop table IF EXISTS na_voljo CASCADE;
        drop table IF EXISTS dvorana CASCADE;
        drop table IF EXISTS karta CASCADE;
        drop table IF EXISTS film CASCADE;
    """)
    conn.commit()

def ustvari_kino():
    cur.execute("""
        DROP TABLE IF EXISTS kino CASCADE;
        CREATE TABLE IF NOT EXISTS kino(
        ime TEXT  PRIMARY KEY  NOT NULL,
        kraj TEXT
        );
    """)
    conn.commit()

def ustvari_prigrizek():
    cur.execute("""
        DROP TABLE IF EXISTS prigrizek CASCADE;
        CREATE TABLE IF NOT EXISTS prigrizek(
        ime TEXT NOT NULL PRIMARY KEY UNIQUE,
	cena FLOAT NOT NULL
        );
    """)
    conn.commit()

def ustvari_na_voljo():
    cur.execute("""
        DROP TABLE IF EXISTS na_voljo CASCADE;
        CREATE TABLE IF NOT EXISTS na_voljo(
        kino_ime TEXT REFERENCES kino(ime) ON DELETE CASCADE,
	prigrizek_ime TEXT REFERENCES prigrizek(ime) ON DELETE CASCADE
        );
    """)
    conn.commit()

def ustvari_karto():
    cur.execute("""
        DROP TABLE IF EXISTS karta CASCADE;
        CREATE TABLE IF NOT EXISTS karta(
        id INTEGER PRIMARY KEY NOT NULL,
        trajanje TEXT,
        tehnologija TEXT,
        osnovna_cena FLOAT,
        popust TEXT, 
        kino_ime TEXT REFERENCES kino(ime) ON DELETE CASCADE
        );
    """)
    conn.commit()

def ustvari_dvorano():
    cur.execute("""
        DROP TABLE IF EXISTS dvorana CASCADE;
        CREATE TABLE IF NOT EXISTS dvorana(
        stevilka INTEGER,
	kapaciteta INTEGER,
	kino_ime TEXT NOT NULL REFERENCES kino(ime) ON DELETE CASCADE,
	PRIMARY KEY(stevilka, kino_ime)
        );
    """)
    conn.commit()

def ustvari_film():
    cur.execute("""
        DROP TABLE IF EXISTS film CASCADE;
        CREATE TABLE IF NOT EXISTS film(
        id INTEGER NOT NULL PRIMARY KEY,
        naslov TEXT NOT NULL,
        rezija TEXT NOT NULL,
	ocena FLOAT,
	distributer TEXT,
	dolzina INTEGER NOT NULL,
	leto TEXT
        );
    """)
    conn.commit()

def ustvari_vrti():
    cur.execute("""
        DROP TABLE IF EXISTS vrti CASCADE;
        CREATE TABLE IF NOT EXISTS vrti(
        cas TIME,
        tehnologija TEXT,
        film_id INTEGER REFERENCES film(id),
        kino_ime TEXT REFERENCES kino(ime)
        );
    """)
    conn.commit()

def ustvari_zanr():
    cur.execute("""
        DROP TABLE IF EXISTS zanr CASCADE;
        CREATE TABLE IF NOT EXISTS zanr(
        ime TEXT PRIMARY KEY NOT NULL
        );
    """)
    conn.commit()

def ustvari_ima_zanr():
    cur.execute("""
        DROP TABLE IF EXISTS ima_zanr CASCADE;
        CREATE TABLE IF NOT EXISTS ima_zanr(
        film_id INTEGER REFERENCES film(id) NOT NULL,
        ime_zanra TEXT REFERENCES zanr(ime)
        );
    """)
    conn.commit()

#================================================================================================

### uvoz preko CSV
            
def uvoziCSV(csv_tabela): # sprejme 'kino', 'karta' ...
    with open('podatki_csv/{0}.csv'.format(csv_tabela), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        
        # preberi prvo vrstico iz CSV
        glava = next(podatki)

        # tole dodam zaradi ene napake ki mi jo vrača ..
        nova_glava = []
        for i in range(len(glava)):
            if '\ufeff' in glava[i]:
                glava[i] = glava[i].replace('\ufeff', '')
                
            #print(str(element))
            glava[i] = str(glava[i]).replace(' ', '').replace(';', '')
            if glava[i] != '':
                #print(glava[i])
                nova_glava.append(glava[i])
        print(nova_glava)
            
        # pripravi predlogo za vstavljanje stolpcev
        stolpci = '(%s)' % ', '.join(['{}'] * len(nova_glava))
        
        # pripravi predlogo za vstavljanje podatkov
        vrednosti = '(%s)' % ', '.join(['%s'] * len(nova_glava))

        # vstavi ime tabele in stolpcev
        poizvedba = sql.SQL(" ".join(["INSERT INTO {}", stolpci, "VALUES", vrednosti])) \
            .format(sql.Identifier(csv_tabela), *(sql.Identifier(stolpec) for stolpec in nova_glava))
        print(poizvedba)

        # gre čez ostale vrstice eno po eno - ne prebere celotne datoteke takoj!
        for vrstica in podatki:
            
            if len(vrstica) == 0: #or len(vrstica) == 1:
                continue
            
            for i in range(len(vrstica)):
                vrstica[i] = str(vrstica[i]).replace(' ', '').replace(';', '')
            cur.execute(poizvedba, vrstica) # izvede poizvedbo

    # izvede se po uspešnem uvozu - če gre prej kaj narobe, naj se vse zavrže!
    conn.commit()
    print('uvoženo {0}'.format(csv_tabela))


#======================================================================================================

# priklop (v datoteko auth.py vstavi svoje podatke)
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# naredimo tabele
izbrisi()
ustvari_kino()
ustvari_prigrizek()
ustvari_dvorano()
ustvari_karto()
ustvari_na_voljo()
ustvari_film()
ustvari_vrti()
ustvari_zanr()
ustvari_ima_zanr()

# napolnimo tabele

uvoziCSV('prigrizek') 
uvoziCSV('kino')
uvoziCSV('na_voljo')
uvoziCSV('karta')
uvoziCSV('film')
uvoziCSV('dvorana') 
uvoziCSV('vrti')
uvoziCSV('zanr')
uvoziCSV('ima_zanr')




conn.close()



















