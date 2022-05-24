from time import process_time
from types import NoneType
from src.mapa import Mapa
import random

currentSeed = 0
seed = False

def resetCurrentSeed():
    global currentSeed
    currentSeed = 0

def enableTest3():
    global seed
    seed = True

def disableTest3():
    global seed
    seed = False

#Trieda pre frekvencu pamat
class FrequencyTable:
    def __init__(self,mapa : Mapa):
        self.table = []
        #pre kazdu poziciu pohybu vytvorime pole vsetkych pozicii zaciatkov
        for i in range((mapa.x+mapa.y)):
            self.table.append([])
            #zaciatky nastavime na nulu
            for j in range(2*(mapa.x+mapa.y)):
                self.table[i].append(0)


    #pripocitanie vyskytu pociatku number na pozicii movePos
    def addOccurance(self,number,movePos):
        self.table[movePos][number]+=1
    
    #vypocitanie penalizacie cisla na pozicii movePos
    #<1,0> - 1 - nepouzite 0 - pouzivane stale
    #predstavuje percentualne zastupenie cisla na pozicii
    def calcPenalty(self,number,movePos):
        num = self.table[movePos][number]
        sumOfAll = 0;
        for value in self.table[movePos]:
            sumOfAll+= value;
        if sumOfAll == 0:
            return 1
        return 1 - num/sumOfAll


def generujCestu(mapa : Mapa, frequency : FrequencyTable = None):
    pohyby = [-1]*(mapa.x+mapa.y+len(mapa.stones))
    obvod = 2*mapa.x + 2*mapa.y
    movePool =  [i for i in range(obvod)] #pole obsahujuce vsetky mozne pociatocne pozicie 
    frequencyValue = {}
    for i in range(mapa.x+mapa.y):
        #ak nepouzivame frekvencnu pamat
        if frequency == None:
            #nahodne vyber prvok z pociatocnych pozicii a vloz ho do vektora pohybov
            rand = random.randint(0,len(movePool)-1)
            pohyby[i] = movePool.pop(rand)
        else:
            #vytvori dict kde kazda pozicia ma svoje ohodnotenie pouzivanie 100 - este nepouzite 0 - pouzivane stale
            frequencyValue = {key:100*frequency.calcPenalty(key,i) for key in range(obvod)}

            #nahodne pomiesanie hodnot
            #aby boli unikatnejsie vektory
            #ak by sme zoradili frequencyValue pred tymto tak by sme mohli dostat 0,1,2,3,4,5.... ako vektor
            keys = list(frequencyValue.keys())
            random.shuffle(keys)
            freq = {key:frequencyValue[key] for key in keys}


            #usporiadanie klucov podla ich penalizacie
            frequencyValue = [key for key,val in sorted(freq.items(), key = lambda ele : ele[1], reverse= True)]
            poh = frequencyValue.pop(0)

            #asi nepotrebne
            while poh in pohyby: #ak uz sa hodnota v vektore nachadza vytiahni inu
                poh = frequencyValue.pop(0)

            pohyby[i] = poh


    for i in range(mapa.x+mapa.y,len(pohyby)):
        pohyby[i] = random.randint(0,1)
    return pohyby



def vygenerujNasledovnikov(moves, mapa,pocet, rand : int = 0, swaps : int = 0):
    nasledovnici = [];
    obvod = 2*(mapa.x + mapa.y)
    #ETAPA 1
    #vytvorenie nasledovnikov vymenou pociatocnych indexov
    if swaps == 1:
        #for i in range(1,mapa.x + mapa.y):
        for i in range(1,pocet):
            kopia = list(moves)
            kopia[i],kopia[i-1] = kopia[i-1],kopia[i]
            nasledovnici.append(kopia)
    elif swaps > 1:
       for i in range(0,pocet):
            for j in range(i+1,pocet):
                kopia = moves.copy()
                kopia[i],kopia[j] = kopia[j],kopia[i]
                nasledovnici.append(kopia)
    movePool = []
    global currentSeed
    global seed
    #vytvorenie move poolo ktory neobashuje hodnoty ktore nie su v pohybovom vektore po vykonany pocet
    #ETAPA 2
    for i in range(obvod):
        if i not in moves[:pocet]:
            movePool.append(i)
    if rand == 1:
        #vyber index, ktory hrabac vykonal
        if seed:
            random.seed(currentSeed)
            currentSeed +=1 
            if currentSeed ==  10000:
                currentSeed = 0
        randIndex = random.randint(0,(pocet)-1)
        for i in movePool:
            k = list(moves)
            #ak sa cislo i nachadza vo v pohybovom vektore, resp. bolo toto cislo nevykonane
            if i in moves[:mapa.x+mapa.y]:
                l = moves.index(i)
                k[randIndex],k[l] = i,k[randIndex]
            else:         #ak nie tak ho tam iba zapis
                k[randIndex] = i
            nasledovnici.append(k)
    elif rand == 2:
        #for i in range(1,mapa.x + mapa.y):
        for i in range(pocet):
            kopia = list(moves)

            #TEST 3 uprava
            if seed:
                random.seed(currentSeed)
                currentSeed +=1 
                if currentSeed ==  10000:
                    currentSeed = 0
            #generovanie nahodnych nasledovnikov
            #generuje sa vzdy jeden nasledovnik na index i
            cislo = random.choice(movePool)
            if cislo in moves[:mapa.x+mapa.y]:
                l = moves.index(cislo)
                kopia[i],kopia[l] = cislo,kopia[i]
            else:         
                kopia[i] = cislo
            nasledovnici.append(kopia)
    else:
            for i in range(pocet):
            #for i in range(pocet):
                #generovanie vsetkych moznych nasledovnikov v okoli
                for cislo in movePool:
                    kopia = list(moves)
                    if cislo in moves[:mapa.x+mapa.y]:
                        l = moves.index(cislo)
                        kopia[i],kopia[l] = cislo,kopia[i]
                    else:         
                        kopia[i] = cislo
                    nasledovnici.append(kopia)


    #ETAPA 3 premena otacani
    for i in range(mapa.x+mapa.y,len(moves)):
        kopia = list(moves)
        #prehadzovanie hodnot otoceni z nul na jednotky a naopak
        kopia[i] = 0 if kopia[i] == 1 else 1
        nasledovnici.append(kopia)

    #TEST 3 uprava
    if seed:
        random.seed(currentSeed)
        currentSeed +=1 
        if currentSeed ==  10000:
            currentSeed = 0

    random.shuffle(nasledovnici)
    return nasledovnici



def najdiNajlepsi(nasledovnici,tabuList, mapa : Mapa,currentBestFitness, chooseWorseIn : bool = False):
    najlepsi = []
    najlepsiFitness = 0
    najpocet = 0
    noInTabu = []
    for kandidat in nasledovnici:   #pre kazdeho kandidata 
        if kandidat not in tabuList:
            kandFitness,pocet = mapa.fitness(kandidat)    #vypocitaj jeho fitness
            noInTabu.append((kandidat,kandFitness,pocet))
            if kandFitness > najlepsiFitness: #skontroluj ci je lepsi ako predchadzajuci najlepsi kandidat
                #nastav ako noveho najlepsieho kandidata
                najlepsi = kandidat
                najlepsiFitness = kandFitness
                najpocet = pocet

    #force na vyber horsieho riesenia ktore nie je v tabu liste ale nema ohodnotenie
    if chooseWorseIn and random.randint(0,50) == 0 and najlepsiFitness == currentBestFitness:
       noInTabu.sort(key= lambda x: x[1])
       najlepsi,najlepsiFitness,najpocet = noInTabu[len(noInTabu)*2//3]
    return (najlepsi,najlepsiFitness,najpocet)
