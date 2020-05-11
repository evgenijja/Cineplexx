# uvozimo ustrezne podatke za povezavo
import auth


# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import csv
import sqlite3

#===============================================================================

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
        id INTEGER NOT NULL PRIMARY KEY,
	zanr TEXT NOT NULL,
	naslov TEXT NOT NULL,
	ocena FLOAT,
	rezija TEXT NOT NULL,
	leto TEXT,
	dolzina INTEGER NOT NULL,
	distributer TEXT
        );
    """)
    conn.commit()


#================================================================================================

# funkcija za uvoz preko csv

def uvoziCSV(csv_tabela): # sprejme 'kino', 'karta' ...
    with open('podatki4/{0}.csv'.format(csv_tabela), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        for i in range(len(vrstice)): 
            trenutna_vrstica2 = [] # pomožni seznam ki ga bomo spremenil v tuple
            for j in range(len(vrstice[i])): # vrstice[i][j] so posamezni podatki npr za dani kino
                trenutna_vrstica = () # to bo naš tuple ki bo šel v insert
                trenutna_vrstica2.append(vrstice[i][j])
                
            # tegale se lotmo ker nas ustavi če je v katerem elementu ' saj potem string piše kot ""
            # ko probamo vnest "" v bazo se obesi
            # če odstranmo ' se lepo spremeni v string '' je pa res da s tem spremenimo ime
            for i in range(len(trenutna_vrstica2)):
                if "'" in trenutna_vrstica2[i]:
                    trenutna_vrstica2[i] = str((trenutna_vrstica2[i]).replace("'", ""))

            trenutna_vrstica = tuple(trenutna_vrstica2)
            print(trenutna_vrstica) # tole printamo kar gre potem v insert
                
            cur.execute("INSERT INTO {0} ({1}) VALUES {2}".format(csv_tabela, ",".join(glava), trenutna_vrstica))
            conn.commit()
            #print("INSERT INTO {0} ({1}) VALUES {2}".format(csv_tabela, ",".join(glava), trenutna_vrstica))
        print('uvoženo {0}'.format(csv_tabela))
        
#======================================================================================================

## poskus uvoza preko sql

### tale funkcija za naredit tabele načeloma dela ampak nism zihr če skup z zgornjo kodo...
### tole rabmo za nardit tabele
##def uvoziSQL(datoteka):
##    with open(datoteka, encoding="UTF-8") as f:
##        koda = f.read()
##        #print(koda)
##        cur.execute(koda)
##        print('narjene prazne tabele')
##    conn.commit()
##

### tale funkcija ne dela - ustavi se ker se nekateri ključi ponavljajo
### posebej bi blo treba nardit še za sql funkcijo pocisti_podatke
##def uvoziSQL_stavki(sql_tabela):
##    with open('podatki2/{0}.sql'.format(sql_tabela), encoding="utf-8-sig") as sqlfile:
##        sql = sqlfile.read()
##        #print(sql.split(';'))
##        #sql2 = sql.split(';')
##        #print(sql2)
##        koda = "{}".format(sql)
##        #print(sql)
##        #print(koda)
##        #print(koda)
##        cur.execute('{}'.format(koda))
##        print('uvoženo {0}'.format(sql_tabela))
##        conn.commit()
        
#=============================================================================================

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

uvoziCSV('kino') # dela
uvoziCSV('dvorana') # za to bi blo treba dodat še sklic na kino
#uvoziCSV('film') # ne dela ker nagajajo vejice
#uvoziCSV('prigrizek') # ne dela ker nagajajo vejice
#uvoziCSV('na_voljo') # ne morem pognat ker se sklicuje na prigrizek
#uvoziCSV('karta') # isti hudič


##uvoziSQL('cineplexx.sql') # tabele bi verjetno lahko naredili tudi tako

###to bi uporabili za uvoz preko sql
##uvoziSQL_stavki('kino')
##uvoziSQL_stavki('prigrizek')
##uvoziSQL_stavki('dvorana')
##uvoziSQL_stavki('karta')
##uvoziSQL_stavki('film')
##uvoziSQL_stavki('na_voljo')

conn.close()



















