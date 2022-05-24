from random import randint
from src.pohyby import Gardener,moveUntilCant
from colorama import Fore, Back
import copy

#farby vo vypise
colors = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Back.RED + Fore.BLACK,
    Back.GREEN + Fore.BLACK,
    Back.YELLOW + Fore.BLACK,
    Back.BLUE+ Fore.BLACK,
    Back.MAGENTA + Fore.BLACK,
    Back.CYAN + Fore.BLACK,
]



class Mapa:
    def __init__(self,cols,rows,stones,leaves,skip = False) -> None:
        self.x = cols #pocet stlpcov
        self.y = rows #pocet riadkov
        self.stones = stones #zoznam kamenov
        self.leaves = leaves #zoznmam listov
        self.skip = skip
        self.leafMax = [0,0,0] #maximalne pocty listov
        self.prazdna = self.createEmptyMap() #vytvor prazdnu mapu

    def createEmptyMap(self):
        plocha = [[0]*(self.x+2) for i in range(self.y+2)]

        for x in range(self.x+2):
            plocha[0][x] = '*'
            plocha[-1][x] = '*'

        for y in range(self.y+2):
            plocha[y][0] = '*'
            plocha[y][-1] = '*'

        
        leafs= ['z','p','c']
        self.leafMax = [0,0,0]
        #umiestni kamene na plochu
        for x,y in self.stones:
            plocha[y+1][x+1] = 'K';
        #umiestni listy na plochu
        for x,y,c in self.leaves:
            plocha[y+1][x+1] = c
            self.leafMax[leafs.index(c)]+=1

        self.prazdna = plocha
        return plocha


    def fillMap(self,moves):
        #vytvor kopiu prazdnej mapy
        mapa = copy.deepcopy(self.prazdna)

        smerPohybu = -1
        poradieCesty = 1 
        gardener = Gardener(0,0)
        leaves = ['z','p','c']
        while gardener.cColor != 'c' and gardener.pocetPozbieranych[leaves.index(gardener.cColor)] == self.leafMax[leaves.index(gardener.cColor)]:
            gardener.cColor = leaves[leaves.index(gardener.cColor)+1]
        for start in moves[:(self.x+self.y)]:
            if start < self.x:
                smerPohybu = 0 #pohyb dole
                gardener(start+1,0)
            elif start < self.x+self.y:
                smerPohybu = 1 #pohyb vlavo
                gardener(self.x+1,start-self.x+1)
            elif start < 2*self.x + self.y:
                smerPohybu = 2 #pohyb vpravo
                gardener(start - (self.x + self.y)+1,self.y+1)
            else:
                smerPohybu = 3 #pohyb hore
                gardener(0,start - (2*self.x + self.y)+1)

            turnIndex = 0 #pozicia  vo vektore pohybov
            startOfTurns = self.x+self.y
            mapaStones = len(self.stones)
            #opakuj pohyby pokial nevyjdes z mapy
            while not moveUntilCant(mapa,smerPohybu,poradieCesty,gardener,self.leafMax):
                if self.skip or mapa[gardener.row][gardener.col] != '*':
                #ak sa pohyboval hore alebo dole
                    if smerPohybu % 2 == 0:
                        left,right = mapa[gardener.row][gardener.col-1],mapa[gardener.row][gardener.col+1]
                        #ak sa moze rozhodnut ci pojde vlavo alebo vpravo
                        
                        if (left == 0 or left == gardener.cColor or left == '*') and (right == 0 or right == gardener.cColor or right == '*'):
                            #ak su nejake casti urcujuce otocenie
                            if startOfTurns < len(moves):
                                smerPohybu = moves[startOfTurns+(turnIndex+start)%mapaStones]*2 + 1
                            else:
                                #ak nie rozhodni sa podla hodnoty turnIndex
                                smerPohybu = ((turnIndex+5*smerPohybu+7*poradieCesty)%2)*2+1
                            turnIndex+=1  
                        #moze sa pohnut len vpravo
                        elif right == 0 or right == gardener.cColor or right == '*':
                            smerPohybu = 3
                        #moze sa pohnut len vlavo
                        elif  left == 0 or left == gardener.cColor or left == '*':
                            smerPohybu = 1  
                        #nema sa kam otocit
                        else:
                            #ak nie je natstavene preskakovanie tak 
                            if not self.skip:
                                if gardener.cColor == 'c' and (left == 'c' or right == 'c'):
                                    print("what")
                                return mapa,gardener
                            else: #ak je nastavene
                                #ak sa zahradnik nepohol zo zaciatku chod na dalsi zaciatok
                                if mapa[gardener.row][gardener.col] == '*':
                                    break
                                else:
                                    #ak sa zastavil v ploche tak ukonci vyplnovanie cesty
                                    return mapa,gardener
                    else:
                        up,down = mapa[gardener.row-1][gardener.col],mapa[gardener.row+1][gardener.col]
                        if (up == 0 or up == gardener.cColor or up == '*') and (down == 0 or down == gardener.cColor or down == '*'):
                            if turnIndex < len(moves):
                                smerPohybu = moves[startOfTurns+(turnIndex+start)%mapaStones]*2
                            else:
                                smerPohybu = ((turnIndex+5*smerPohybu+7*poradieCesty)%2)*2
                            turnIndex+=1 
                        elif down == 0 or down == gardener.cColor or down == '*':
                            smerPohybu = 0
                        elif  up == 0 or up == gardener.cColor or up == '*':
                            smerPohybu = 2
                        else:
                            if not self.skip:
                                if gardener.cColor == 'c' and (up == 'c' or down == 'c'):
                                    print("what")
                                return mapa,gardener
                            else:
                                if mapa[gardener.row][gardener.col] == '*':
                                    break
                                else:
                                    return mapa,gardener
                else:
                    return mapa,gardener
                if turnIndex == len(moves):
                    turnIndex = randint(0,len(moves)-1)
            #if not skip:
            poradieCesty+=1

        return mapa,gardener

    #funkcia na vypocet fitness
    def fitness(self,moves):
        mapa,gardener = self.fillMap(moves)
        #pripocitaj ku vysledku fitness pozbieranych listov
        return gardener.fitness + self.leafFitness(gardener.pocetPozbieranych),gardener.pocetCiest

    #vrati maximalnu dosiahnutelnu fitness
    def maxFitness(self):
        result = 0;
        result = self.x*self.y-len(self.stones)
        return result + self.leafFitness(self.leafMax)

    #vrati fitness pozbieranych listov
    def leafFitness(self,leafCount):
        result = 0
        #kazdy zlty list ma hodnotu dvojnasobku maximalnej fitness policok
        #kazdy oranzovy ma dvojnasobok zlteho
        #kazdy cerveny ma dvojnasobok cerveneho
        mult = 2*(self.x*self.y-len(self.stones))
        for i in leafCount:
            result+= mult*i
            mult*=2

        return result

    #funkcia na vypisanie zahrady
    def printMap(self,moves):
        mapa,gardener = self.fillMap(moves)
        if len(mapa) != self.y+2:
            print("what")
        for row in mapa:
            line = f""
            for col in row:
                if isinstance(col,int) and col > 0:
                    line += colors[(col-1) % len(colors)]+"{:<2}".format(col) + " " + Fore.RESET + Back.RESET
                elif col in ['z','c','p']:
                    if col == 'z':
                        line += Fore.YELLOW+Back.YELLOW+ "{:<2}".format(col)+ " " + Fore.RESET + Back.RESET
                    elif col == 'p':
                        line += "\033[48;5;208m\033[38;5;208m"+ "{:<2}".format(col)+ " " + Fore.RESET + Back.RESET
                    else:
                        line += Fore.RED+Back.RED+ "{:<2}".format(col)+ " " + Fore.RESET + Back.RESET
                else:
                    line += "{:<2}".format(col) + " "
            print(line)
