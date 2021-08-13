# Projektna: Evidenca_za_dopust

from bottle import route, get, post, request, run, static_file, template
import os
from datetime import date 

class Izleti:

    def __init__(self, izleti=[]):
        ''' To so seznami izletov. '''
        self.izleti = izleti

    def pretekli(self):
        ''' To je seznam preteklih izletov.'''
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
        ''' To je seznam prihodnjih izletov, ki niso aktualni.'''
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
        self.izleti.append(izlet)

    
    def vsi(self):
        return self.izleti

    #def remove_izlet#
    

class Izlet:

    def __init__(self, zacetno_stanje, destinacija, datum_zacetek, datum_konec):
        ''' To je trenuten aktiven izlet. '''
        self.zacetno_stanje = zacetno_stanje
        self.trenutno_stanje = zacetno_stanje
        self.destinacija = destinacija
        self.datum_zacetek = datum_zacetek
        self.datum_konec = datum_konec

        self.porabil_danes = 0
        self.nakupi = [] 

    def dodaj_nakup(self, nakup):

        self.nakupi.append(nakup) 
        self.trenutno_stanje = self.trenutno_stanje - nakup.cena * nakup.kolicina 

    
    def izbrisi_nakup(self, st_nakupa):

        self.trenutno_stanje = self.trenutno_stanje + (self.nakupi[st_nakupa].cena * self.nakupi[st_nakupa].kolicina) 
        del self.nakupi[st_nakupa]
        



    def skupna_poraba(self):

        denar = 0
        for nakup in self.nakupi:
            denar += nakup.kolicina * nakup.cena 

        return denar
    
    def skupna_poraba_procenti(self):

        return (self.skupna_poraba() / self.zacetno_stanje) * 100 


        
class Nakup:

    def __init__(self, izdelek_ali_storitev, cena, kolicina):
        ''' To predstavlja en nakup. '''
        self.izdelek_ali_storitev = izdelek_ali_storitev
        self.cena = cena
        self.kolicina = kolicina








izlet_v_izolo = Izlet(300, "Izola", date(2020,3,25), date(2020,4,20))
izlet_v_izolo.dodaj_nakup(Nakup("pivo", 2.2, 4))
izlet_v_izolo.dodaj_nakup(Nakup("kokakola", 1.7, 3))

izlet_v_paris = Izlet(400, "Paris", date(2022,4,23), date(2022,5,1))
izlet_v_paris.dodaj_nakup(Nakup("mona'lisa_fake", 10000, 1))
izlet_v_paris.dodaj_nakup(Nakup("kokakola", 1.7, 3))

izlet_v_hrvasko = Izlet(250, "Hrvaska", date(2021,7,20), date(2021,7,30))
izlet_v_hrvasko.dodaj_nakup(Nakup("pivo", 2.2, 20))
izlet_v_hrvasko.dodaj_nakup(Nakup("kokakola", 1.7, 3))

izlet_v_rusijo = Izlet(250, "Rusija", date(2023,7,20), date(2023,7,30))
izlet_v_rusijo.dodaj_nakup(Nakup("vodka", 2.2, 20))
izlet_v_rusijo.dodaj_nakup(Nakup("Medved", 1.7, 3))


izleti = Izleti([izlet_v_izolo, izlet_v_hrvasko, izlet_v_paris, izlet_v_rusijo])

vsi_uporabniki = {}
vsi_uporabniki[123] = izleti


@get('/<id_uporabnika>')
def index(id_uporabnika):
    if int(id_uporabnika) in vsi_uporabniki:

        izleti = vsi_uporabniki[int(id_uporabnika)]

        
        return template('index.html', id_uporabnika = id_uporabnika, izleti=izleti)
    else:
        return f"Uporabnik {id_uporabnika} ne obstaja."

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
    return static_file('SLIKA.jfif', root=os.path.dirname(__file__) )


@get('/<id_uporabnika>/izlet/<st_izleta>')
def izlet(id_uporabnika, st_izleta):

    izleti = vsi_uporabniki[int(id_uporabnika)] 

    return template('izlet.html',id_uporabnika = id_uporabnika, izlet = izleti.pridobi_izlet(int(st_izleta)), st_izleta = st_izleta)



@get('/<id_uporabnika>/izlet/<st_izleta>/izbrisi/<st_nakupa>')
def izbris_nakupa(id_uporabnika, st_izleta, st_nakupa):

    izleti = vsi_uporabniki[int(id_uporabnika)] 

    izleti.pridobi_izlet(int(st_izleta)).izbrisi_nakup(int(st_nakupa))
    return izlet(id_uporabnika, st_izleta)



































run(host='localhost', port=8080)




