from queue import PriorityQueue
import time
from colorama import Fore, Back, Style
import gc
import sys

from src.gui import showSolution

#trieda predstavujúca stav uzla
class Stav:
    def __init__(self,cols : int, rows : int, data):
        # optimalizacia --- pre jeden hlavolam sa velkost nemeni -> presunut mimo triedu
        self.rows = rows #pocet riadkov
        self.cols = cols #pocet stlpcov
        self.matrix = data #pozicie hlavolamu

    #vytvori kopiu hlavolamu dát hlavolamu
    def getMatrixCopy(self):
        return self.matrix.copy()
    
    #vrati hraciu plochu -- nekopiruje
    def getMatrix(self):
        return self.matrix
    
    #metody na vratenie velkosti
    def getXY(self):
        return self.cols,self.rows
    def getSize(self):
        return self.rows*self.cols

    #metody na porovnanie veľkosti hlavolamov
    def compareSize(self,rows : int ,cols : int):
        return self.rows == rows and self.cols == cols
        #tu
    def compareSize(self,stav):
        return self.rows == stav.rows and self.cols == stav.cols

class uzol:
    def __init__(self,stav : Stav ,parent, operacia,mode, final : Stav) -> None:
        self.stav = stav    
        self.parent = parent
        self.operacia = operacia    #cislom reprezentovana vykonana operacia
        self.heuristika = 0
        if mode == 0:
            self.heuristika = self.vypocitatVzdialenost(final)  # heuristika 2
        elif mode == 1:
            self.heuristika =  self.vypocitatZleUlozene(final)# heuristika 1
        else:
            self.heuristika =  self.vypocitatZleUlozene(final) + self.vypocitatVzdialenost(final)# heuristika 3

    #pretazenie operatora < pre PriorityQueue
    def __lt__(self,other):
            return self.heuristika < other.heuristika

    #funckia pre gui
    def getHeuristika(self):
        return self.heuristika
        

    def vypocitatZleUlozene(self,finalnyStav):
        result = 0
        pStav = self.stav.getMatrix()
        fStav = finalnyStav.getMatrix()
        #pre kazde policko skontroluje ci cislo v policku v cielovom stave je aj v tomto stave
        for i in range(self.stav.getSize()):
            if fStav[i] != 0: #vynechavame 0
                if pStav[i] != fStav[i]:
                    result+=1   #ak na cislo na indexe v cielovom stave nie je rovanke ako cislo v tomto stave tak pripocitaj jedna
        self.pocetZleUlozenych = result
        return result

    def vypocitatVzdialenost(self,finalnyStav):
        result = 0
        #kopie stavov
        pStav = self.stav.getMatrix()
        fStav = finalnyStav.getMatrix()
        cX,cY = self.stav.getXY() # dlzka riadka 
        #prechadza cisla od 1 po velkost-1
        #preskakujeme 0
        for i in range(1,self.stav.getSize()):
            indexF = fStav.index(i) #index policka v cielovom stave
            indexC = pStav.index(i) #inde policka v pociatocnom stava
            Crow,Ccol = indexC // cX, indexC % cX       #vypocita riadok a stlpec, v ktorom sa nachadza cislo v stave
            Frow,Fcol = indexF // cX, indexF % cX       #vypocita riadok a stlpec, v ktorom sa nachadza cislo v cielovom stave
            result += abs(Crow - Frow) + abs(Ccol - Fcol)   #vypocita manhattansku vzdialenost
        self.sucetOdSpravnychPozicii = result
        return result

    #porovnanie stavov 
    def comp(self, finalnyStav : Stav):
        if not self.stav.compareSize(finalnyStav):
            return False
        pStav = self.stav.getMatrix()
        fStav = finalnyStav.getMatrix()
        if pStav == fStav:
            return True
        return False
    
# ---- pohyby ----
#indexPraz je index v stave na ktoreho pozicii je 0
def hore(stav : Stav, indexPraz : int):
    x,y = stav.getXY()
    nStav = stav.getMatrixCopy()
    #ak na hracej ploche je pod prazdnym miestom este policko
    #resp. ak index prazdenho miesta + dlzka riadka je mensia ako velkost plochy
    if indexPraz + x  < x*y:
        #vymena prazdneho miesta s polickom
        nStav[indexPraz],nStav[indexPraz + x] = nStav[indexPraz + x], nStav[indexPraz]
        novy = Stav(x,y,nStav)
        return novy
    return -1
def dole(stav : Stav,indexPraz : int):
    x,y = stav.getXY()
    nStav = stav.getMatrixCopy()
    #ak na hracej ploche je nad prazdnym miestom este policko
    #resp. ak index prazdenho miesta - dlzka riadka je vacsia alebo rovna 0
    if indexPraz - x > -1:
        nStav[indexPraz],nStav[indexPraz - x] = nStav[indexPraz - x], nStav[indexPraz]
        novy = Stav(x,y,nStav)
        return novy
    return -1
def vlavo(stav : Stav,indexPraz : int):
    x,y = stav.getXY()
    nStav = stav.getMatrixCopy()
    i = indexPraz % x #vypocitat kde v riadku sa prazdne miesto nachdza
    #ak na hracej ploche je vpravo od prazdneho miesta este policko
    #resp. ak index prazdenho miesta +1 je mensia ako dlzka riadka
    if i + 1 < x:
        nStav[indexPraz],nStav[indexPraz + 1] = nStav[indexPraz + 1 ], nStav[indexPraz]
        novy = Stav(x,y,nStav)
        return novy
    return -1
def vpravo(stav : Stav,indexPraz : int):
    x,y = stav.getXY()
    nStav = stav.getMatrixCopy()
    i = indexPraz % x
    #ak na hracej ploche je vlavo od prazdneho miesta este policko
    #resp. ak index prazdenho miesta -1 je vacsia alebo rovna 0
    if i - 1 > -1:
        nStav[indexPraz],nStav[indexPraz - 1] = nStav[indexPraz - 1 ], nStav[indexPraz]
        novy = Stav(x,y,nStav)
        return novy
    return -1

# Hlavna funkcia na hladanie riesenia
    #mode
    #0 - vzdialenost od spravenej pozicie
    #1 - zle ulozena heuristika
    #2 - vzdialenost od spravenej pozicie + zle ulozena heuristika
def search(pociatocny,cielovy,mode):
    operacie = [hore,dole,vlavo,vpravo] #referencie na funkcie operacii
    #vytvorenie pociatocneho uzla
    pociatnyUzol = uzol(pociatocny,0,-1,mode,cielovy)
    pocetVytvorenychUzlov= 1;
    #vytvorenie prioritneho radu a pridanie pociatocenho uzla
    queue = PriorityQueue()
    queue.put(pociatnyUzol)
    spracovane = []     #pole pre spracovane uzly
    while not queue.empty(): #pokial rad nie je prazdny
        node = queue.get()
        #zistenie ci vybraty stav nie je cielovy
        if node.comp(cielovy):
            spracovane.append(node) #pridaj prave spracovavany do spracovanych
            return [node, pocetVytvorenychUzlov,len(spracovane)]
        
        index0 = node.stav.getMatrix().index(0) #najdenie indexu prazdneho miesta
        #vytvorenie vsetkych pohybov
        for  i in range(4):
            nStav = operacie[i](node.stav,index0)
            #ak sa pohyb podarilo vykonat
            if nStav != -1:
                skipQueue = False # premmena na zistenie ci pohyb nebude pridany do radu
                for sp in spracovane: #skontrolovanie ci vytvoreny uzol nebol uz spracovany
                    if sp.comp(nStav):
                        skipQueue = True
                if not skipQueue: #ak nebol
                    #kontrola ci rovnaky uzol necaka na spracovanie
                    for j in range(len(queue.queue)):
                        if queue.queue[j].comp(nStav):
                            skipQueue = True
                #ak nebol ani v spracovanych ani nespracovanych, tak ho pridaj do radu
                if not skipQueue:
                    queue.put(uzol(nStav,node,i, mode,cielovy))
                    pocetVytvorenychUzlov+=1;
        #pridaj prave spracovavany do spracovanych
        spracovane.append(node)

    return [None,pocetVytvorenychUzlov,len(spracovane)]

#funkcia na spracovanie nacitaneho riadku
def parseRaw(line : str):
    line = line.strip('\n')
    #ak riadok je prazdny alebo prvy znak je #
    if len(line) == 0 or line[0] =="#": return -1,None,None,None,None
    #ak prvy znak v riadku je ! jedna sa o funkciu
    if line[0] == "!": 
        line = line.lower()
        if "show" in line:
            return 2,"show",None,None,None
        elif "block" in line:
            return 3,"block",None,None,None
        elif "average" in line:
            if "endaverage" in line:
                return 4, "average", False,None,None
            return 4,"average",True,None,None
        elif "skip" in line:
            if "end" in line:
                return 5,"skip", False,None,None
            return 5,"skip",True,None,None
    #ak riadok obsahuje dve rovna sa a x, tak sa jedna o hlavolam
    elif line.count("=") == 2 and line.count("x") == 1:
        size,pstav,fstav = line.split('=')
        rows,cols = size.split('x')
        s = int(rows)*int(cols)-1
        #ak sa nevytvori hlavolam aspon o velkosti 2 policok alebo velkost je zadana v zapornych cislach
        if int(rows)*int(cols) <2 or int(rows) < 0 or int(cols) < 0:
            printError("Error - badSize")
            return -1,None,None,None,None
        #kontrola ci obsahuje pocet ciarok aka je velkost plochy
        if pstav.count(',') == s and fstav.count(',') == s:
            #vracia udaje o hlavolame
            return 0,rows, cols, pstav.split(','), fstav.split(',')

    return -1,None,None,None,None

#vytvorenie pociatocneho,cieloveho stavu z dat z parseRaw 
def parseInput(inp,rows,col):
    result = []
    hasZero = False
    for c in inp:
        if c == '0':
            hasZero= True
        result.append(int(c))
    #ak stav neobsahuje nulu nie je korektny
    if not hasZero:
        printError("bez nuly")
        sys.exit(1)
    return Stav(int(col),int(rows),result)


#kontrola korektnosti hracej plochy
def checkInput(inp, size):
    if len(inp) != size:
        print("nie je ",size,", ale ", len(inp))
        return False
    #kontrola ci vsetky nacitane znaky su cisla
    for i in inp:    
        if not i.isdigit():
            print("nie su cisla")
            return False
    contains = [0] * size
    #kontrola ci obsahuje vsetky cisla od 0 po velkost -1
    for i in range(len(inp)):
        j = int(inp[i])
        #ak cislo je vacsie ako plocha
        if j >= size:
            print("obsahuje cislo vacsie ako je maximum pre plochu")
            return False
        if contains[j] == 0:
            contains[j] = 1
        else:
            #ak sa nejake cislo opakuje viac ako raz
            print("obsahuje viac rovnakych cisel")
            return False
    #ak nejake cislo sa nenachadza v zozname
    for n in contains:
        if n != 1:
            return False

    return True

#vracia vysledok uzla, pocetUzlov ku vysledku (hlbku), a retazec obsahujuci kroky riesenia
def getResult(uzol):
    opsStrings = ["hore","dole","vlavo","vpravo"]
    sv = "vysledok", uzol.stav.getMatrix()
    outputString = "\n¦"
    count = 1
    #prechadza vsetky rodicovske uzly a pripisuje opraciu akou sme sa k nej dostali
    while uzol.parent != 0:
        count+=1
        outputString = " -> " +opsStrings[uzol.operacia] + outputString 
        uzol = uzol.parent
    #pripis pociatocneho uzla
    outputString = "0" + outputString
    return sv,count, outputString


#spusti hladanie a vypise vysledky
#vracia informacie potrebne pre dalsie funkcie suborov
def printSearch(pociatocnyStav,cielovyStav,mode):
    start = time.time()
    vysledok = search(pociatocnyStav,cielovyStav,mode)
    end = time.time()
    print("¦ vysledok najdeny za:", round(end - start,6) , "s") 
    if isinstance(vysledok[0],uzol):
        vys,countPath,cesta = getResult(vysledok[0])
        print("¦ ----", vys,"-----")
        print("¦ ",cesta)
        print("¦ ")
        print("¦ pocet vytvorenych uzlov: ", vysledok[1])
        print("¦ pocet spracovanych uzlov: ",vysledok[2])
        print("¦ pocet uzlov ku vysledku: ", countPath, "(",countPath -1, "- hlbka)")
        print('¦')
        return countPath,vysledok[1],vysledok[2],end-start,vysledok[0]
    else:
        print("¦ vysledok sa nenasiel")
        print('¦')
        return -1,None,None,None,None


def printInfo(msg):
    print(Fore.YELLOW +">>> INFO --- " + msg + Style.RESET_ALL)

def printError(msg):
    print(Fore.RED + ">>> ERROR --- "+msg + Style.RESET_ALL)

def main():
    printInfo("otvara sa ")
    try:
        pociatocneStavyFile = open("stavy.txt","r")
    except FileNotFoundError:
        printError("Subor sa nenasiel")
        return 1
    printInfo("subor otvoreny")


    riadky = [] #funkcie a pociatocne riadky
    skip = False
    #spracovanie riadkov
    for riadok in pociatocneStavyFile:
        succ, rows,cols, Pstav, Fstav = parseRaw(riadok)
        if succ == -1: continue # vynechavany riadok
        if succ == 5: #skip funkcia
            skip = cols
            continue
        if skip: continue #ak je skip zapnuty preskakuj

        if succ == 2 or succ == 3: #funkcie show a block
            #rows - nazov funkcie
            riadky.append(rows)
        elif succ == 4: #funckia average
            #rows - nazov funkcie
            #cols - Zapnut vypnut
            riadky.append((rows,cols))
            #ak nejde o ziadnu funkciu tak sa jedna o hlavolam
        elif checkInput(Pstav,int(rows)*int(cols)) and  checkInput(Fstav,int(rows)*int(cols)):
            riadky.append((parseInput(Pstav,rows,cols),parseInput(Fstav,rows,cols)))  #pridanie pociatocneho stavu a cieloveho stavu
        else:
            printError("zle zadany stav")
            return 1
    
    pociatocneStavyFile.close()
    show = False
    collect = False
    averageData = []
    riadky.reverse() #otoc riadky tak aby zodpovedali nacitanemu suboru

    while len(riadky) != 0:
        riadok = riadky.pop()   #vyber riadok
        #ak sa jedna o riadok so stavmi tak ho spracuj
        if isinstance(riadok,tuple) and isinstance(riadok[0],Stav):
            print("====",riadok[0].rows,"x",riadok[0].cols,"=",riadok[0].getMatrix(), "====")
            print("¦ Hueristika 1. podla poctu zle ulozenych cisiel: ")
            cesta1,strom1,spra1,time1,node1 = printSearch(riadok[0],riadok[1],1)
            print("¦ Hueristika 2. podla vzdialenosti k spravnemu miestu: ")
            cesta2,strom2,spra2,time2,node2 = printSearch(riadok[0],riadok[1],0)
            print("¦ Hueristika 3. kombinacia oboch: ")
            cesta3,strom3,spra3,time3,node3 = printSearch(riadok[0],riadok[1],2)
            #ak je nastavena vizualizacia riesenia pre riadok
            if show:
                if cesta1 != -1 and cesta2 != -1 and cesta3 != -1:
                    showSolution(node1,node2,node3)
                show = False
            print()
            #ak je nastaveny zber udajov pre priemery
            if collect:
                averageData.append([(cesta1,strom1,spra1,time1),(cesta2,strom2,spra2,time2),(cesta3,strom3,spra3,time3)])
            #vymazanie uzlov
            del node1
            del node2
            del node3
            #zber nerefernecovanych dat
            gc.collect()

        #ak sa jedna o funkcie "show" alebo block
        elif isinstance(riadok,str):
            if riadok == "show":
                show = True #nastav vizualizaciu
            elif riadok == "block":
                printInfo("waiting for input....")
                input() #pockaj na vstup
            else:
                printError("Invalid function")
        elif isinstance(riadok,tuple):
            if "average" in riadok[0]:
                collect = riadok[1]
                #ak boli zbierane data a je collect nastaveny na false
                if len(averageData) > 0 and collect == False:
                    print(averageData)
                    #pole ktore obsahuje priemery z heuristik
                    #[[heu1],[heu2],[heu3]]
                    #[[cesta,vytvorene,spracovane,cas]]
                    average = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                    #urob sucet nad vsetkymi datami
                    for row in averageData:
                        for i in range(3):
                            for j in range(4):
                                average[i][j] += row[i][j]
                    #s kazdym cislom vyrob priemr
                    for i in range(3):
                        for j in range(4):
                            average[i][j] /= len(averageData)
                            average[i][j] = round(average[i][j],3)
                    print("=============================================")
                    print("Priemery: ")
                    for i in range(3):
                        print("Heuristika", i+1,".")
                        print("dlzka cesty:", average[i][0])
                        print("pocet vytvorenych:", average[i][1])
                        print("pocet spracovanych:", average[i][2])
                        print("cas:", average[i][3])
                        print("------------")

                    print("=============================================")

                    #vycisti polia
                    averageData.clear()
                    average.clear()

                    printInfo("waiting for input....")
                    input() #pockaj na vstup


        else:
            print("Error")

    return 0

main()