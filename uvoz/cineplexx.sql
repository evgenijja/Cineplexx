DROP TABLE IF EXISTS kino;  
DROP TABLE IF EXISTS karta;
DROP TABLE IF EXISTS prigrizek;
DROP TABLE IF EXISTS na_voljo;
DROP TABLE IF EXISTS dvorana;
DROP TABLE IF EXISTS film;


CREATE TABLE prigrizek(
	ime TEXT NOT NULL PRIMARY KEY UNIQUE,
	cena FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS kino(
    ime TEXT PRIMARY KEY NOT NULL,
    kraj TEXT NOT NULL
);



CREATE TABLE na_voljo(
	kino_ime TEXT PRIMARY KEY REFERENCES kino(ime) ON DELETE CASCADE,
	prigrizek_ime TEXT REFERENCES prigrizek(ime) ON DELETE CASCADE
);


CREATE TABLE karta(
    id INTEGER PRIMARY KEY NOT NULL,
    trajanje TEXT,
    tehnologija TEXT,
    osnovna_cena FLOAT,
    popust TEXT, 
    prodaja TEXT REFERENCES kino(ime) ON DELETE CASCADE
);

CREATE TABLE dvorana(
	stevilka INTEGER PRIMARY KEY NOT NULL,
	kapaciteta INTEGER
);

CREATE TABLE film(
	id INTEGER NOT NULL PRIMARY KEY,
	zanr TEXT NOT NULL,
	naslov TEXT NOT NULL,
	ocena FLOAT,
	rezija TEXT NOT NULL,
	leto TEXT,
	dolzina INTEGER NOT NULL,
	distributer TEXT
)





