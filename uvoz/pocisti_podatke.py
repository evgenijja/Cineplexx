import csv
import os

#=====================================================================================================

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


#=======================================================================================================
    
# za dvorano nardimo posebej, ker ima dva ključa in če bi nardil samo za številke nam jih ostane zelo malo

def pocisti_podatke_dvorana(csv_datoteka):
    with open('podatki/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        print('dolzina {} prej:'.format(csv_datoteka), len(vsi_podatki))
        razlicni_podatki = {}
        for i in range(len(vsi_podatki)):
            kljuc = (vsi_podatki[i][0], vsi_podatki[i][2]) # stevilka in ime kinota
            if kljuc not in razlicni_podatki:
                razlicni_podatki[kljuc] = vsi_podatki[i][1]
        print('dolzina {} potem:'.format(csv_datoteka), len(razlicni_podatki))
    os.remove('podatki/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko

    # na novo nardim datoteko in zapišem nove podatke
    with open('podatki/{0}.csv'.format(csv_datoteka), 'w', encoding="UTF-8") as f:
        for key in razlicni_podatki.keys():
            f.write("%s, %s, %s\n" % (key[0], razlicni_podatki[key], key[1]))
            #print('spisal za {}'.format(key))
    #return 'uspel pocistiti {}'.format(csv_datoteka)
    f.close()
      
#============================================================================================================

def pocisti_podatke_zanr(csv_datoteka):
    with open('podatki/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        print('dolzina {} prej:'.format(csv_datoteka), len(vsi_podatki))
        razlicni_podatki = []
        for i in range(len(vsi_podatki)):
            element = vsi_podatki[i] # stevilka in ime kinota
            if element not in razlicni_podatki:
                razlicni_podatki.append(vsi_podatki[i])
        print('dolzina {} potem:'.format(csv_datoteka), len(razlicni_podatki))
    os.remove('podatki/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko

    # na novo nardim datoteko in zapišem nove podatke
    with open('podatki/{0}.csv'.format(csv_datoteka), 'w', encoding="UTF-8") as f:
        for i in range(len(razlicni_podatki)):
            f.write("%s\n" % (razlicni_podatki[i][0]))
            #print('spisal za {}'.format(key))
    #return 'uspel pocistiti {}'.format(csv_datoteka)
    f.close()


#============================================================================================================


def pocisti_karte(csv_datoteka):
    with open('podatki/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        #print(vsi_podatki)
        #vsi_podatki = csvfile
        print('dolzina {} prej:'.format(csv_datoteka), len(vsi_podatki))
        razlicni_podatki = {}


    for podatek in vsi_podatki:
        print(podatek)
            #print(podatek[0])
            #print(podatek[1:])
        if podatek == []:
            continue
        elif podatek[-1] == '' or podatek[-1] == '\n':
            continue
        else:
            if podatek[0] not in razlicni_podatki:
                razlicni_podatki[podatek[0]] = podatek[1:]
    print(razlicni_podatki)
    print('dolzina {} potem:'.format(csv_datoteka), len(razlicni_podatki))
    #os.remove('podatki/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko
    
    # na novo nardim datoteko in zapišem nove podatke
    with open('podatki/{0}.csv'.format(csv_datoteka), 'w', encoding="UTF-8") as f:
        for key in razlicni_podatki.keys():
            f.write("%s, %s\n" % (key, ','.join(razlicni_podatki[key])))
            #print('spisal za {}'.format(key))
    #return 'uspel pocistiti {}'.format(csv_datoteka)
    f.close()
      
#============================================================================================================

def pocisti_dvorane(csv_datoteka): # dela tud za ima_zanr
    with open('podatki/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        #print(vsi_podatki)
        #vsi_podatki = csvfile
        print('dolzina {} prej:'.format(csv_datoteka), len(vsi_podatki))
        razlicni_podatki = []



    for podatek in vsi_podatki:
        print(podatek)
            #print(podatek[0])
            #print(podatek[1:])
        if podatek == []:
            continue
        elif podatek[-1].replace(' ', '').replace(';', '') == '' or podatek[-1].replace(' ', '') == '\n':
            continue
        else:
            razlicni_podatki.append(podatek)
    print(len(razlicni_podatki))
    print('dolzina {} potem:'.format(csv_datoteka), len(razlicni_podatki))
    os.remove('podatki/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko
    
    # na novo nardim datoteko in zapišem nove podatke
    with open('podatki/{0}.csv'.format(csv_datoteka), 'w', encoding="UTF-8") as f:
        for i in range(len(razlicni_podatki)):
            f.write("%s, %s\n" % (razlicni_podatki[i][0], ','.join(razlicni_podatki[i][1:])))
            #print('spisal za {}'.format(key))
    #return 'uspel pocistiti {}'.format(csv_datoteka)
    f.close()

#=====================================================================================


def pocisti_vrti(csv_datoteka): # dela tud za ima_zanr
    with open('podatki/{0}.csv'.format(csv_datoteka), encoding="UTF-8") as csvfile:
        
        podatki = csv.reader(csvfile)
        vsi_podatki = [vrstica for vrstica in podatki] # seznam ločenih podatkov [ime, ključ]
        #print(vsi_podatki)
        #vsi_podatki = csvfile
        print('dolzina {} prej:'.format(csv_datoteka), len(vsi_podatki))
        razlicni_podatki = []



    for podatek in vsi_podatki:
        print(podatek)
            #print(podatek[0])
            #print(podatek[1:])
        if podatek == []:
            continue
        elif podatek[-1].replace(' ', '').replace(';', '') == '' or podatek[-1].replace(' ', '') == '\n':
            continue
        elif podatek[-2].replace(' ', '').replace(';', '') == '' or podatek[-2].replace(' ', '') == '\n':
            continue
        else:
            razlicni_podatki.append(podatek)
    print(len(razlicni_podatki))
    print('dolzina {} potem:'.format(csv_datoteka), len(razlicni_podatki))
    os.remove('podatki/{0}.csv'.format(csv_datoteka)) # zbrišem staro datoteko
    
    # na novo nardim datoteko in zapišem nove podatke
    with open('podatki/{0}.csv'.format(csv_datoteka), 'w', encoding="UTF-8") as f:
        for i in range(len(razlicni_podatki)):
            f.write("%s, %s\n" % (razlicni_podatki[i][0], ','.join(razlicni_podatki[i][1:])))
            #print('spisal za {}'.format(key))
    #return 'uspel pocistiti {}'.format(csv_datoteka)
    f.close()

#=====================================================================================


# tale pa zbriše use vrstice, kjer so nas kej zafrknile vejice

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

#========================================================================================================

# pokličemo

##pocisti_podatke('kino')
##pocisti_podatke('prigrizek')
#3pocisti_podatke('film')
##pocisti_podatke_zanr('zanr')
####

##pocisti_podatke('karta')
##pocisti_podatke('na_voljo')
#pocisti_podatke('vrti')
##pocisti_podatke('ima_zanr')



##pocisti_vejice('kino')
##pocisti_vejice('prigrizek')
##pocisti_vejice('film')
##pocisti_vejice('zanr')

##pocisti_vejice('dvorana')
##pocisti_vejice('karta')
##pocisti_vejice('na_voljo')
#pocisti_vejice('vrti')
##pocisti_vejice('ima_zanr')

##pocisti_karte('karta')
##pocisti_dvorane('dvorana')
#pocisti_dvorane('ima_zanr')
##pocisti_podatke_dvorana('dvorana')
pocisti_vrti('vrti')












