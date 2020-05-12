import csv
import os

#datoteka ki odstrani podatke s podvojenimi ključi

def pocisti_podatke(csv_datoteka):
    with open('podatki/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        print('dolzina {} prej:'.format(csv_datoteka), len(vsi_podatki))
        razlicni_podatki = {}
        for podatek in vsi_podatki:
            #print(podatek[0])
            #print(podatek[1:])
            if podatek[0] not in razlicni_podatki:
                razlicni_podatki[podatek[0]] = podatek[1:]
        print('dolzina {} potem:'.format(csv_datoteka), len(razlicni_podatki))
    os.remove('podatki/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko
    
    # na novo nardim datoteko in zapišem nove podatke
    with open('podatki/{0}.csv'.format(csv_datoteka), 'w', encoding="UTF-8") as f:
        for key in razlicni_podatki.keys():
            f.write("%s, %s\n" % (key, ','.join(razlicni_podatki[key])))
            #print('spisal za {}'.format(key))
    #return 'uspel pocistiti {}'.format(csv_datoteka)
    f.close()


##        
##

##def pocisti_podatke_sql(sql_datoteka):
##    # Open and read the file as a single buffer
##    with open('podatki/{0}.sql'.format(sql_datoteka), encoding="utf-8") as sqlfile:
##        sql = sqlfile.read()
##        
##        koda = "{}".format(sql)
##        koda2 = (str(koda))
##        koda2.replace('insert into','')
##        koda2.replace('\ninsert','')
##        koda2.replace('insert','')
##        koda2.replace('values','')
##        print(koda2)
##        #stevec = 0
##        #for element in koda:
##         #   stevec += 1
##        #print(stevec)
##        #print(koda)
        

def pocisti_vejice(csv_datoteka):
    with open('podatki/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        print('dolzina {} prej:'.format(csv_datoteka), len(vsi_podatki))
        glava = vsi_podatki[0]
        ok_podatki = []
        for i in range(len(vsi_podatki)):
            if len(vsi_podatki[i]) == len(glava):
                ok_podatki.append(vsi_podatki[i])
        print('dolzina {} potem:'.format(csv_datoteka),len(ok_podatki))
        zapomni_glavo = glava
    csvfile.close()
    os.remove('podatki/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko


    # na novo zapišem isto datoteko samo s kul podatki :)
    with open('podatki/{0}.csv'.format(csv_datoteka), 'w', encoding="utf8") as csv_dat:
        writer = csv.writer(csv_dat)
        #writer.writeheader()
        for podatek in ok_podatki:
            writer.writerow(podatek)
    csv_dat.close()    
        
pocisti_podatke('kino')
pocisti_podatke('prigrizek')
pocisti_podatke('dvorana')
pocisti_podatke('film')
pocisti_podatke('karta')
pocisti_podatke('na_voljo')



pocisti_vejice('kino')
pocisti_vejice('prigrizek')
pocisti_vejice('dvorana')
pocisti_vejice('film')
pocisti_vejice('karta')
pocisti_vejice('na_voljo')











