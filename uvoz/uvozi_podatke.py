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
        na_voljo_kino TEXT REFERENCES kino(ime) ON DELETE CASCADE,
	na_voljo_prigrizek TEXT REFERENCES prigrizek(ime) ON DELETE CASCADE
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
        prodaja TEXT REFERENCES kino(ime) ON DELETE CASCADE
        );
    """)
    conn.commit()

def ustvari_dvorano():
    cur.execute("""
        DROP TABLE IF EXISTS dvorana CASCADE;
        CREATE TABLE IF NOT EXISTS dvorana(
        stevilka INTEGER,
	kapaciteta INTEGER,
	
	PRIMARY KEY(kapaciteta)
        );
    """)
    conn.commit()
# tukej je kljuc kapaciteta ceprov bi morala bit stevilka
# fora je da mamo v stolpcih najprej kapaciteto js pa sm funkcijo pocisti_podatke spisala tko, da kljuc vedno postav kot prvi stolpec
# plus
# tle bi blo treba tole še dodat, ker je šibka entiteta in je določena s številko in kinotom
# ima_dvorano TEXT NOT NULL REFERENCES kino(ime) ON DELETE CASCADE, ?????

def ustvari_film():
    cur.execute("""
        DROP TABLE IF EXISTS film CASCADE;
        CREATE TABLE IF NOT EXISTS film(
        naslov TEXT NOT NULL,
        zanr TEXT NOT NULL,
        rezija TEXT NOT NULL,
        ID INTEGER NOT NULL PRIMARY KEY,
	ocena FLOAT,
	distributer TEXT,
	dolzina INTEGER NOT NULL,
	leto TEXT
        );
    """)
    conn.commit()


#================================================================================================


### uvoz preko CSV

##with open('podatki/film.csv', encoding="UTF-8") as csvfile:
##        podatki = csv.reader(csvfile)
##        stevilke = []
##        #print(podatki)
##        for film in podatki:
##            if len(film) in stevilke:
##                continue
##            else:
##                stevilke.append(len(film))
##        print(stevilke)

            
def uvoziCSV(csv_tabela): # sprejme 'kino', 'karta' ...
    with open('podatki/{0}.csv'.format(csv_tabela), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        #print(podatki)
        
            
        
        # preberi prvo vrstico iz CSV
        glava = next(podatki)
        

        # tole dodam zaradi ene napake ki mi jo vrača ..
        for i in range(len(glava)):
            #print(str(element))
            glava[i] = str(glava[i]).replace(' ', '')
        #print(glava)
        

        # pripravi predlogo za vstavljanje stolpcev
        stolpci = '(%s)' % ', '.join(['{}'] * len(glava))
        

        # pripravi predlogo za vstavljanje podatkov
        vrednosti = '(%s)' % ', '.join(['%s'] * len(glava))

        # vstavi ime tabele in stolpcev
        poizvedba = sql.SQL(" ".join(["INSERT INTO {}", stolpci, "VALUES", vrednosti])) \
            .format(sql.Identifier(csv_tabela), *(sql.Identifier(stolpec) for stolpec in glava))
        print(poizvedba)
        #print(vrstica)

        # gre čez ostale vrstice eno po eno - ne prebere celotne datoteke takoj!
        for vrstica in podatki:
            if len(vrstica) == 0:
                continue
            
            print(vrstica)
            for i in range(len(vrstica)):
                #print(str(element))
                vrstica[i] = str(vrstica[i]).replace(' ', '')
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

# napolnimo tabele
uvoziCSV('prigrizek') 
uvoziCSV('kino')
uvoziCSV('na_voljo')
uvoziCSV('karta')
uvoziCSV('dvorana') # dela ampak za to bi blo treba dodat še sklic na kino
uvoziCSV('film')


conn.close()



















