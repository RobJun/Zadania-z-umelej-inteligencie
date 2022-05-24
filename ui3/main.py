
import random
from src.FileParse import getConf
import src.UserInterface
from src.gens import FrequencyTable, disableTest3, enableTest3,resetCurrentSeed
from src.plotter import DataCollector
from src.gens import generujCestu
from src.mapa import Mapa
from src.find import find
import time

def test3(mapa : Mapa,random, maxIter,minTabuSize,maxTabuSize,TabuSizeStep,swapAll,choose):
    collector = DataCollector()
    cID = collector.createCollection(2,"")
    cID2 = collector.createCollection(2,"")
    pohyby = [generujCestu(mapa) for i in range(10)]
    print("max iteracie: ",maxIter)
    print("minTabuSize: ",minTabuSize, "\tmaxTabusize: ",maxTabuSize,"\tkrokZvacsenia: ",TabuSizeStep)
    print("swaps: ", swapAll, "\trandom: ",random,"\tchoose: ",choose)
    enableTest3()
    for i in range(minTabuSize,maxTabuSize+1,TabuSizeStep):
        print("Velkost " + str(i)+ ": ")
        avrTime = 0
        avrFitness = 0
        #TEST 3 uprava
        for j in range(10):
            resetCurrentSeed()
            t,newF = find(i,maxIter,mapa,pohyby[j],collector,rand=random,swaps = swapAll,choose=choose)
            avrTime += t
            avrFitness += newF[1]
        avrTime /=10
        avrFitness /= 10 
        collector.addToCollection(cID,(i,avrTime));
        collector.addToCollection(cID2,(i,avrFitness))
        print("cas[s]: ", t)
        print()
    collector.create2dGraphFromIds("Zavislosť času [s] od veľkosti tabu listu",("Velkost", "čas"),cID)
    input()
    collector.create2dGraphFromIds("Zavislosť fitness od veľkosti tabu listu",("Velkost", "fitnes"),cID2)
    input()
    disableTest3()



def test1(mapa : Mapa, rand1,tabuSize,maxIter, repeats,swapAll,choose):
    collector = DataCollector()
    colIDs = []
    frequency = FrequencyTable(mapa)
    maxF = mapa.maxFitness()
    bestFitness = (0,0)
    print("------------------------------------")
    print("max iteracii bez vylepseni: ",maxIter, "\topakovani: ",repeats)
    print("tabuSize: ",tabuSize)
    print("skipping: ",mapa.skip)
    print("swaps: ", swapAll, "\trandom neighbors: ",rand1)
    print("------------------------------------")
    pohyby = []
    i = 1
    while True:
        print()
        print("iteracia c."+ str(i))
        cId = collector.createCollection(2,"iteracia c."+ str(i))
        colIDs.append(cId)
        pohyb = generujCestu(mapa,frequency)

        maxSim = 0
        for poh in pohyby:
            sim = 0
            for j in range(mapa.x+mapa.y):
                if poh[j] == pohyb[j]:
                    sim+=1
            maxSim = sim if maxSim < sim else maxSim
        print("podobnost pociatocneho stavu s predchadzajucimi: {:.3f}%".format(maxSim/(mapa.x+mapa.y)*100))
        print("pociatocny stav: ", pohyb)
        pohyby.append(pohyb)

        t,newF = find(tabuSize,maxIter,mapa,pohyb,collector,frequency, collectFitnessId=cId, rand=rand1, swaps=swapAll,choose=choose)
        print("cas : ",t,"s")
        i+=1
        if newF[1] > bestFitness[1]:
            bestFitness = newF
        if maxF == bestFitness[1]:
            break;
        if repeats != 0 and i == repeats+1:
            break;


    print("najlepsia fitness: {}/{}".format(bestFitness,maxF))

    bestIterId = collector.createCollection(2,"najlepšie riešenie 1") 
    collector(bestIterId,bestFitness)      
    collector.create2dGraphFromIds("graf",("iteracia","fitness"),colIDs,bestIterId)

    input()
        

def test2(mapa : Mapa, rand1,tabuSize,maxIter,swapAll,choose):
    mapa1 = Mapa(mapa.x,mapa.y,mapa.stones,mapa.leaves,True)
    mapa2 = Mapa(mapa.x,mapa.y,mapa.stones,mapa.leaves,False)
    collector = DataCollector()

    collectionSkipId = collector.createCollection(2,"vyskúšanie všetkých začiatkov")
    colletionStopId = collector.createCollection(2,"vyskúšanie pokial sa mohol pohnút")
    bestIterId = collector.createCollection(2,"najlepšie riešenie - všetky")
    bestIter2Id = collector.createCollection(2,"najlepšie riešenie - pokial sa mohol pohnuť")

    pohyby = generujCestu(mapa1)
    print("------------------------------------")
    print("pociatocny vektor: \n",pohyby)
    print("max iteracii bez vylepsenia: ",maxIter)
    print("tabuSize: ",tabuSize)
    print("skipping: ",mapa.skip)
    print("swaps: ", swapAll, "\trandom neighbors: ",rand1)
    print("choose: ",choose)
    print("------------------------------------")
    print("preskakovanie povolene:")
    t,res =find(tabuSize,maxIter,mapa1,pohyby,collector,collectFitnessId=collectionSkipId,rand=rand1,choose=choose,swaps=swapAll)
    collector(bestIterId,res)
    print("čas: ", t, "s")
    print("preskakovanie zakazane: ")
    t,res =find(tabuSize,maxIter,mapa2,pohyby,collector,collectFitnessId=colletionStopId,rand=rand1,choose=choose, swaps=swapAll)
    print("čas: ", t, "s")
    collector(bestIter2Id,res)

    collector.create2dGraphFromIds("graf",("iteracia","fitness"),collectionSkipId,colletionStopId,bestIter2Id,bestIterId)
    input()



if __name__ == '__main__':
    confParametre = getConf("conf.ini")
    mapa = Mapa(12,10,[(1,2),(2,4),(4,3),(6,1),(8,6),(9,6)],[])
    while True:
        moznost = src.UserInterface.menu()
        if moznost == "p":
            src.UserInterface.parametreTabuSearch(confParametre[0])
        elif moznost == "n":
            src.UserInterface.nacitajMapu(confParametre[1],confParametre[2],mapa)
        elif moznost == "1":
            mapa.skip = confParametre[0][4]
            test1(mapa,confParametre[0][1],confParametre[0][0],confParametre[0][2],confParametre[0][3],confParametre[0][8],confParametre[0][9])
        elif moznost == "2":
            mapa.skip = confParametre[0][4]
            test2(mapa,confParametre[0][1],confParametre[0][0],confParametre[0][2],confParametre[0][8],confParametre[0][9])
        elif moznost == "3":
            mapa.skip = confParametre[0][4]
            test3(mapa,confParametre[0][1],confParametre[0][2],confParametre[0][5],confParametre[0][6],confParametre[0][7],confParametre[0][8],confParametre[0][9])
        elif moznost == "0":
            break
    


