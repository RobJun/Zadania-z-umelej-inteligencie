from src.gens import najdiNajlepsi, resetCurrentSeed, vygenerujNasledovnikov
from src.mapa import Mapa
from src.gens import FrequencyTable
import time

def find(tabuMaxSize,maxIterWoBtr, mapa : Mapa, start,collector,frequency : FrequencyTable = None, 
            collectFitnessId=0, rand :int = 0, swaps : int = 0, choose : bool = False):
        tabuList = []
        best = current = start
        fitness,pocet= bestFitness,pocet= mapa.fitness(best)
        tabuList.append(start)
        bestIter = 0
        allIter = 0
        it = 0
        maxFitness = mapa.maxFitness()
        start = time.time()
        while it < maxIterWoBtr+1 and bestFitness != maxFitness:
            allIter+=1
            #zber pre statistiku
            if collectFitnessId != 0:
                collector(collectFitnessId,(allIter,fitness))
            kandidati = vygenerujNasledovnikov(current,mapa,pocet,rand=rand,swaps=swaps)
            naj,fitness,pocet = najdiNajlepsi(kandidati,tabuList,mapa,fitness,choose)


            #mapa.printMap(current)
            #nastavnie pre frekvencnu pamat
            if frequency != None:
                for i in range(mapa.x+mapa.y):
                    frequency.addOccurance(naj[i],i)

            current = naj
            if(fitness > bestFitness):
                bestFitness = fitness
                best = current
                bestIter = allIter+1
                if collectFitnessId != 0:
                    collector(collectFitnessId,(bestIter,fitness))
                it = 0

            #pridanie stavu do tabulistu
            tabuList.append(current)
            if(len(tabuList) > tabuMaxSize):
                tabuList.pop(0)

            it+=1
        end = time.time();
        print("počet všetkých iteracií: ",allIter)
        print("najlepšie riešenie v iteracií: ", bestIter)
        print("najlepsi vektor: ",best)
        print("fitness: {}/{}".format(bestFitness,maxFitness))
        mapa.printMap(best)

        return end-start,(bestIter,bestFitness)

