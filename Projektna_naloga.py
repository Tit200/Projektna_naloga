# Projektna: Evidenca_za_dopust


#===================================================================================================
# Importi:

from bottle import redirect, route, get, post, request, run, static_file, template
import os
from datetime import date,datetime
import random
import pickle

#===================================================================================================
# Razredi:


class Izleti:
    '''Razred, ki predstavlja uporabnikove izlete.'''


    def __init__(self, izleti=[]):
        '''To so seznami izletov.'''
        self.izleti = izleti


    def pretekli(self):
        '''To je seznam preteklih izletov.'''
        danes = date.today()
        pretekli_izleti = []
        for izlet in self.izleti:
            if izlet.datum_konec < danes:
                pretekli_izleti.append(izlet)
            else:
                continue
        return pretekli_izleti
    

    def aktualni(self):
        '''To je izlet, ki bodisi traja sedaj bodisi je naslednji v vrsti.'''
        danes = date.today()
        aktualni = None
        for izlet in self.izleti:
            if izlet.datum_konec >= danes:
                if aktualni == None:
                    aktualni = izlet 
                else:
                    if aktualni.datum_zacetek > izlet.datum_zacetek:
                        aktualni = izlet
                    else:
                        continue
            else:
                continue

        return aktualni


    def prihodnji(self):
        '''To je seznam prihodnjih izletov, ki niso aktualni.'''
        danes = date.today()
        prihodnji_izleti = []
        for izlet in self.izleti:
            if izlet.datum_zacetek > danes:
                prihodnji_izleti.append(izlet)
            else:
                continue
        if self.aktualni() in prihodnji_izleti:
            prihodnji_izleti.remove(self.aktualni())
        else:
            pass
        
        return prihodnji_izleti


    def pridobi_izlet(self, st_izleta):
        '''To nam vrne izlet.'''
        return self.izleti[st_izleta]
    

    def dodaj_izlet(self, izlet):
        '''To doda izlet k seznamu vseh izletov.'''
        self.izleti.append(izlet)


    def izbrisi_izlet(self, izlet):
        '''To nam izbriše izlet iz seznama vseh izletov.'''
        self.izleti.remove(izlet)

    
    def vsi(self):
        '''Ta funkcija vrne seznam vseh izletov.'''
        return self.izleti



class Izlet:
    '''Razred, ki predstavlja točno določen izlet in funkcije, 
    ki se nanj lahko izvajajo.'''


    def __init__(self, zacetno_stanje, destinacija, datum_zacetek, datum_konec):
        '''To je trenuten aktiven izlet.'''
        self.zacetno_stanje = zacetno_stanje
        self.trenutno_stanje = zacetno_stanje
        self.destinacija = destinacija
        self.datum_zacetek = datum_zacetek
        self.datum_konec = datum_konec

        self.porabil_danes = 0
        self.nakupi = [] 


    def dodaj_nakup(self, nakup):
        '''To doda nakup izletu.'''
        self.nakupi.append(nakup) 
        self.trenutno_stanje = self.trenutno_stanje - nakup.cena * nakup.kolicina 

    
    def izbrisi_nakup(self, st_nakupa):
        '''To izbriše nakup izletu.'''
        self.trenutno_stanje = self.trenutno_stanje + (self.nakupi[st_nakupa].cena * self.nakupi[st_nakupa].kolicina) 
        del self.nakupi[st_nakupa]
        

    def skupna_poraba(self):
        '''Količina denarja, ki smo ga do sedaj porabili.'''
        denar = 0
        for nakup in self.nakupi:
            denar += nakup.kolicina * nakup.cena 

        return denar


    def skupna_poraba_procenti(self):
        '''Delež skupne porabe v procentih'''
        return (self.skupna_poraba() / self.zacetno_stanje) * 100 

       

class Nakup:
    '''Razred, za nakupe v izletu.'''

    def __init__(self, izdelek_ali_storitev, cena, kolicina):
        ''' To predstavlja en nakup. '''
        self.izdelek_ali_storitev = izdelek_ali_storitev
        self.cena = cena
        self.kolicina = kolicina


#===================================================================================================
# Spletna stran:

@get('/<id_uporabnika>')
def vsi_izleti(id_uporabnika):
    print("id uporabnika je " + id_uporabnika)
    if int(id_uporabnika) in vsi_uporabniki:

        izleti = vsi_uporabniki[int(id_uporabnika)]
        
        return template('views/vsi_izleti.html', id_uporabnika = id_uporabnika, izleti=izleti)
    else:
        return index(True)  


@post('/<id_uporabnika>/izlet/<st_izleta>')
def dodaj_nakup(id_uporabnika, st_izleta):
    izleti = vsi_uporabniki[int(id_uporabnika)] 

    ime_izdelka_ali_storitve = request.forms.get('ime_izdelka_ali_storitve')
    cena = int(request.forms.get('cena'))
    kolicina = int(request.forms.get('kolicina'))

    nakup = Nakup(ime_izdelka_ali_storitve, cena, kolicina)

    izletek = izleti.pridobi_izlet(int(st_izleta))
    izletek.dodaj_nakup(nakup)
  
    return izlet(id_uporabnika, st_izleta)


@route('/slika')
def slika():
    return static_file('resources/SLIKA.jfif', root=os.path.dirname(__file__) )


@route('/slika2')
def slika2():
    return static_file('resources/SLIKA2.jfif', root=os.path.dirname(__file__) )


@route('/favicon.ico')
def ikona():
    return static_file('resources/favicon.ico', root=os.path.dirname(__file__) )


@get('/<id_uporabnika>/izlet/<st_izleta>')
def izlet(id_uporabnika, st_izleta):

    izleti = vsi_uporabniki[int(id_uporabnika)] 

    return template('views/izlet.html',id_uporabnika = id_uporabnika, izlet = izleti.pridobi_izlet(int(st_izleta)), st_izleta = st_izleta)


@get('/<id_uporabnika>/izlet/<st_izleta>/izbrisi/<st_nakupa>')
def izbris_nakupa(id_uporabnika, st_izleta, st_nakupa):

    izleti = vsi_uporabniki[int(id_uporabnika)] 
    izleti.pridobi_izlet(int(st_izleta)).izbrisi_nakup(int(st_nakupa))
    
    return izlet(id_uporabnika, st_izleta)


@get('/<id_uporabnika>/urejanje')
def urejanje(id_uporabnika):
    return template('views/urejanje.html',id_uporabnika=id_uporabnika)
    

@post('/<id_uporabnika>/urejanje')
def dodaj_izlet(id_uporabnika):

    ime_izleta = request.forms.get('destinacija')
    
    od = datetime.strptime(request.forms.get('od'), "%Y-%m-%d").date()
    do = datetime.strptime(request.forms.get('do'), "%Y-%m-%d").date()
    zacetno_stanje = int(request.forms.get('zacetno_stanje'))

    nov_izlet = Izlet(zacetno_stanje, ime_izleta, od, do)
    izleti = vsi_uporabniki[int(id_uporabnika)]

    izleti.dodaj_izlet(nov_izlet)

    st_izleta = izleti.vsi().index(nov_izlet)

    redirect(f"/{id_uporabnika}/izlet/{st_izleta}")  


@post('/')
def izberi_uporabnika():
    
    pridobljen_id = request.forms.get('id_uporabnika')
    
    redirect(f"/{pridobljen_id}")  


@get('/')
def index(ne_obstaja=False):
    return template('views/index.html', ne_obstaja=ne_obstaja)

   
@get('/generiraj')
def generiraj_uporabnika():

    id = random.randint(100000000000,999999999999)

    while id in vsi_uporabniki:
        id = random.randint(100000000000,999999999999)

    vsi_uporabniki[id]=Izleti() 

    redirect(f"/{id}")     


@get('/<id_uporabnika>/izlet/<st_izleta>/izbrisi_izlet')
def izbris_izleta(id_uporabnika, st_izleta):

    izleti = vsi_uporabniki[int(id_uporabnika)] 
    izlet = izleti.pridobi_izlet(int(st_izleta))
    
    izleti.izbrisi_izlet(izlet)

    return vsi_izleti(id_uporabnika)                           


#===================================================================================================
# Shranjevanje podatkov:

#Ta koda je namenjena temu, da se podatki kot so: Izleti, nakupi, uporabniški ID-ji,
# ob izklopu VS-code'a ne izgubijo.

with open('podatki.txt', 'rb') as podatki:
    vsi_uporabniki=pickle.load(podatki)

run(host='localhost', port=8080)

with open('podatki.txt', 'wb') as podatki:
    pickle.dump(vsi_uporabniki, podatki, protocol=pickle.HIGHEST_PROTOCOL)

