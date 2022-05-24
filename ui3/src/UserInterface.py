from src.mapa import Mapa
import random

def menu():
    while True:
        print("vyberte si z možnosti:")
        print("0 - exit")
        print("p - parametre tabu search algoritmu")
        print("n - nacitaj mapu")
        print("1 - test s frequency memory")
        print("2 - porovnanie preskakovania neplatnych krokov vs nepreskakovanie")
        print("3 - postupne zvacsovanie tabu listu a poctu maximalneho poctu do najdenia lepsieho riesenia")
        moznost = input("$ ")
        return moznost


def parametreTabuSearch(parametre):
    strings =[
        "Velkost tabu listu: ",
        "Nahodny nasledovnici: ",
        "max. pocet iteracii bez vylepsenia: ",
        "maximalny pocet opakovani hladania riesenia: ",
        "preskakovat zle pozicie: ",
        "minimalna velkost tabuListu: ",
        "maximalna velkost tabuListu: ",
        "krok zvacsenia: ",
        "vymena: ",
        "vyber horsieho: "
    ]
    for i in range(len(parametre)):
        print(strings[i], parametre[i])

    while True:
        zmena = input("chcete zmenit parametre? (y/n): ")
        if zmena.lower() == "y":
            break;
        elif zmena.lower() == "n":
            return;

    for i in range(len(parametre)):
        cislo = input(strings[i])
        if cislo.isdigit():
            parametre[i] = int(cislo)
            if i == 4 or i == 9:
                parametre[i] = True if parametre[i] > 0 else False

def parametreMapy(parametreStones, parametreLeaf):
    stringsStones =[
        "pocet kamenov: ",
    ]
    stringLeaf = [
        "pocet zltych: ",
        "pocet oranzovych: ",
        "pocet cervenych: "
    ]
    for i in range(1):
        print(stringsStones[i], parametreStones[i])
    print("------------")
    for i in range(3):
        print(stringLeaf[i], parametreLeaf[i])

    while True:
        zmena = input("chcete zmenit parametre? (y/n): ")
        if zmena.lower() == "y":
            break;
        elif zmena.lower() == "n":
            return;

    for i in range(1):
        cislo = input(stringsStones[i])
        if cislo.isdigit():
            parametreStones[i] = int(cislo)
    for i in range(3):
        cislo = input(stringLeaf[i])
        if cislo.isdigit():
            parametreLeaf[i] = int(cislo)

def getDefaultMap(mapa : Mapa):
    print("moznosti:")
    print("1 - zadanie - bez listov")
    print("2 - zadanie - s listami")

    while True:
        moznost = input("Zadajte moznost: ")
        if moznost == "1":
            mapa.x = 12
            mapa.y = 10
            mapa.leaves = []
            mapa.stones = [(1,2),(2,4),(4,3),(6,1),(8,6),(9,6)]
            mapa.createEmptyMap()
            return;
        elif moznost == "2":
            mapa.x = 12
            mapa.y = 10
            mapa.stones = [(5,0),(6,0),(5,9),(6,9)]
            mapa.leaves = [(1,0,'c'),(0,1,'c'),(10,0,'c'),
            (11,1,'c'),(2,3,'p'),(3,2,'p'),
            (8,2,'p'),(9,3,'p'),(3,5,'p'),
            (4,5,'z'),(5,4,'z'),(6,5,'z'),
            (7,4,'z'),(0,6,'c'),(1,7,'c'),
            (9,6,'p'),(8,7,'p'),(11,8,'c'),(10,9,'c')]
            mapa.createEmptyMap()
            return;

def readInput(st):
    hodnota = ""
    while True:
        hodnota = input(st)
        if hodnota.isdigit():
            hodnota = int(hodnota)
            break;
    return hodnota

def umiestniNaMapu(mapa : Mapa,miesto : tuple, co):
    if miesto[0] > -1 and miesto[0] < mapa.x:
        if miesto[1] > -1 and miesto[1] < mapa.y:
            if len(co) == 2:
                if co not in mapa.stones:
                    mapa.stones.append(co)
            else:
                listy = []
                for x,y,c in mapa.leaves:
                    listy.append((x,y))
                
                if miesto not in mapa.stones and miesto not in listy:
                    mapa.leaves.append(co)

def generateManualMap(mapa : Mapa):
    dlzka =readInput("Zadajte dlzku: ")    
    vyska =readInput("Zadajte vysku: ")
    mapa.x = dlzka
    mapa.y = vyska
    pocetKamenov = int(readInput("Zadajte pocet kamenov: "))
    mapa.stones = []
    mapa.leaves = []
    for i in range(pocetKamenov):
        miesto = input("zadaj poziciu v tvare x,x: ")
        miesto = tuple(int(x) for x in miesto.split(","))
        umiestniNaMapu(mapa,miesto,miesto)

    pocetZltych = int(readInput("Zadajte zltych listov: "))
    for i in range(pocetZltych):
        miesto = input("zadaj poziciu v tvare x,x: ")
        miesto = tuple(int(x) for x in miesto.split(","))
        co = (miesto[0],miesto[1],'z')
        umiestniNaMapu(mapa,miesto,co)
    pocetOranzovych = int(readInput("Zadajte oranzovych listov: "))
    for i in range(pocetOranzovych):
        miesto = input("zadaj poziciu v tvare x,x: ")
        miesto = tuple(int(x) for x in miesto.split(","))
        co = (miesto[0],miesto[1],'p')
        umiestniNaMapu(mapa,miesto,co)
    pocetCer = int(readInput("Zadajte pocet cervenych: "))
    for i in range(pocetCer):
        miesto = input("zadaj poziciu v tvare x,x: ")
        miesto = tuple(int(x) for x in miesto.split(","))
        co = (miesto[0],miesto[1],'c')
        umiestniNaMapu(mapa,miesto,co)
    
    mapa.createEmptyMap()


def generateMap(parametreStones,parametreLeaf, mapa : Mapa):
    dlzka = readInput("Zadajte dlzku: ")
    vyska = readInput("Zadajte vysku: ")
    spaces = []
    for i in range(dlzka):
        for j in range(vyska):
            spaces.append((i,j))
    Stones = []
    for i in range(parametreStones[0]):
        if(len(spaces) == 0): break
        Stones.append(spaces.pop(random.randint(0,len(spaces)-1)))

    Leaves = []
    if len(spaces) != 0:
        for i in range(parametreLeaf[0]):
            if(len(spaces) == 0): break
            rand = spaces.pop(random.randint(0,len(spaces)-1))
            Leaves.append((rand[0],rand[1],'z'))

    if len(spaces) != 0:
        for i in range(parametreLeaf[1]):
            if(len(spaces) == 0): break
            rand = spaces.pop(random.randint(0,len(spaces)-1))
            Leaves.append((rand[0],rand[1],'p'))

    if len(spaces) != 0:
        for i in range(parametreLeaf[2]):
            if(len(spaces) == 0): break
            rand = spaces.pop(random.randint(0,len(spaces)-1))
            Leaves.append((rand[0],rand[1],'c'))

    mapa.x = dlzka
    mapa.y = vyska
    mapa.stones = Stones
    mapa.leaves = Leaves
    mapa.createEmptyMap()


def nacitajMapu(parametreStones, parametreLeaf,mapa : Mapa):
    while True:
        print("------------------")
        print("moznosti: ")
        print("0 - vrat sa spat")
        print("1 - vyber default mapu")
        print("2 - vygeneruj")
        print("3 - parametre generovania")
        print("4 - manualne zadat mapu")
        print("5 - vypis nacitanu mapu")

        moznost = input("Zadajte moznost: ")

        if moznost == "3":
            parametreMapy(parametreStones,parametreLeaf)
        elif moznost == "2":
            generateMap(parametreStones,parametreLeaf,mapa)
        elif moznost == "1":
            getDefaultMap(mapa)
        elif moznost == "5":
            mapa.printMap([])
        elif moznost == "4":
            generateManualMap(mapa)
        elif moznost == "0":
            print("------------------")
            return;
