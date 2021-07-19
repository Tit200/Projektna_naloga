# Projektna: Evidenca_za_dopust

from bottle import Request, get, post, request, run, template


 
class Izleti:

    def __init__(self, pretekli, trenutni, prihodnji):
        ''' To so seznami izletov. '''
        self.pretekli = pretekli
        self.trenutni = trenutni
        self.prihodnji = prihodnji 
    

class Izlet:

    def __init__(self, zacetno_stanje, destinacija):
        ''' To je trenuten aktiven izlet. '''
        self.zacetno_stanje = zacetno_stanje
        self.trenutno_stanje = zacetno_stanje
        self.destinacija = destinacija

        self.porabil_danes = 0
        self.nakupi = [] 

    def dodaj_nakup(self, nakup):

        self.nakupi.append(nakup) 
        self.trenutno_stanje = self.trenutno_stanje - nakup.cena * nakup.kolicina 

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








izlet_v_izolo = Izlet(300, "Izola")
izlet_v_izolo.dodaj_nakup(Nakup("pivo", 2.2, 4))
izlet_v_izolo.dodaj_nakup(Nakup("kokakola", 1.7, 3))

izlet_v_paris = Izlet(400, "Paris")
izlet_v_paris.dodaj_nakup(Nakup("mona'lisa_fake", 10000, 1))
izlet_v_paris.dodaj_nakup(Nakup("kokakola", 1.7, 3))

izlet_v_hrvasko = Izlet(250, "Hrvaska")
izlet_v_hrvasko.dodaj_nakup(Nakup("pivo", 2.2, 20))
izlet_v_hrvasko.dodaj_nakup(Nakup("kokakola", 1.7, 3))


izleti = Izleti([izlet_v_izolo], izlet_v_hrvasko, [izlet_v_paris])



@get('/')
def index():
    return template('index.html', izleti=izleti)

@post('/')
def dodaj_nakup():

    ime_izdelka_ali_storitve = request.forms.get('ime_izdelka_ali_storitve')
    cena = int(request.forms.get('cena'))
    kolicina = int(request.forms.get('kolicina'))

    nakup = Nakup(ime_izdelka_ali_storitve, cena, kolicina)
    izleti.trenutni.dodaj_nakup(nakup)
  
    return template('index.html', izleti=izleti)













































run(host='localhost', port=8080)




