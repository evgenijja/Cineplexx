import csv
import os

#datoteka ki odstrani podatke s podvojenimi ključi

def pocisti_podatke(csv_datoteka):
    with open('podatki4/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        print(len(vsi_podatki))
        razlicni_podatki = {}
        for podatek in vsi_podatki:
            if podatek[0] not in razlicni_podatki:
                razlicni_podatki[podatek[0]] = podatek[1:]
        print(len(razlicni_podatki))
    os.remove('podatki4/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko
    
    # na novo nardim datoteko in zapišem nove podatke
    with open('podatki4/{0}.csv'.format(csv_datoteka), 'w', encoding="UTF-8") as f:
        for key in razlicni_podatki.keys():
            f.write("%s, %s\n" % (key, ','.join(razlicni_podatki[key])))
            #print('spisal za {}'.format(key))
    return 'uspel pocistiti {}'.format(csv_datoteka)

pocisti_podatke('kino')
pocisti_podatke('prigrizek')
pocisti_podatke('dvorana')
pocisti_podatke('film')
pocisti_podatke('karta')
pocisti_podatke('na_voljo')
