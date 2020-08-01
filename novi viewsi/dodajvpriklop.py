#============================================= dodano ===================================================================

@get('/karte/karte2d')
def karte():
    cur.execute("SELECT * FROM karta WHERE tehnologija = '2D'")
    return rtemplate('karta.html', karta=cur)

@get('/karte/karte3d')
def karte():
    cur.execute("SELECT * FROM karta WHERE tehnologija = '3D'")
    return rtemplate('karta.html', karta=cur)

@get('/film') 
def film():
    cur.execute("SELECT * FROM film")
    return rtemplate('film.html', film=cur)

@get('/film/<x:int>') 
def filmi(x):
    cur.execute("SELECT * FROM film WHERE ocena > %s", [x])
    return rtemplate('film.html', film=cur)

@get('/ima_zanr/<x>') 
def film_zanr(x):
    cur.execute("SELECT * FROM ima_zanr WHERE ime_zanra = %s", [x])
    return rtemplate('ima_zanr.html', ima_zanr=cur)

@get('/filmid/<x:int>')
def film_id(x):
    cur.execute("SELECT * FROM film WHERE id = %s", [x])
    return rtemplate('film.html', film=cur)
    


#========================================================================================================================
