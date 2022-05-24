leaves = ['z','p','c']


#trieda na urcenie polohy zahradakara v zahrade
class Gardener:
    def __init__(self,col,row) -> None:
        self.row = row
        self.col = col
        self.cColor = leaves[0]
        self.pocetPozbieranych = [0,0,0]
        self.fitness = 0
        self.pocetCiest = 0

    def __call__(self,col,row):
        self.row = row
        self.col = col
        self.pocetCiest+=1

def hore(stav,number, gardener : Gardener):
    nextMove = stav[gardener.row-1][gardener.col]
    #miesto na ktore sa chce pohnut je koniec plochy, ina cesta alebo farba listu ktoru este nemozeme zbierat
    if nextMove == '*' or (nextMove != 0 and nextMove != gardener.cColor):
        return False 
    #ak sme zobrali list
    if nextMove == gardener.cColor:
        gardener.pocetPozbieranych[leaves.index(gardener.cColor)]+=1
    #pohnutie zahradkara o miesto vyssie a nastavenie na cislo cesty
    gardener.row-=1
    stav[gardener.row][gardener.col] = number
    gardener.fitness+=1
    return True

def dole(stav,number, gardener: Gardener):
    nextMove =  stav[gardener.row+1][gardener.col]
    if nextMove == '*' or (nextMove != 0 and nextMove != gardener.cColor):
        return False 
    if nextMove == gardener.cColor:
        gardener.pocetPozbieranych[leaves.index(gardener.cColor)]+=1
    gardener.row+=1
    stav[gardener.row][gardener.col] = number
    gardener.fitness+=1
    return True


def vlavo(stav,number, gardener: Gardener):
    nextMove =  stav[gardener.row][gardener.col-1]
    if nextMove == '*' or (nextMove != 0 and nextMove != gardener.cColor):
        return False 
    if nextMove == gardener.cColor:
        gardener.pocetPozbieranych[leaves.index(gardener.cColor)]+=1
    gardener.col-=1
    stav[gardener.row][gardener.col] = number
    gardener.fitness+=1
    return True

def vpravo(stav,number, gardener: Gardener):
    nextMove =  stav[gardener.row][gardener.col+1]
    if nextMove == '*' or (nextMove != 0 and nextMove != gardener.cColor):
        return False 
    if nextMove == gardener.cColor:
        gardener.pocetPozbieranych[leaves.index(gardener.cColor)]+=1
    gardener.col+=1 
    stav[gardener.row][gardener.col] = number
    gardener.fitness+=1
    return True

#kontrola ci po zastaveni zastavil mimo plochy alebo v nej
def isOutOfBounds(position : Gardener,matrix, opIndex):
    row,col = position.row,position.col
    if opIndex == 0:
        row +=1
    elif opIndex == 2:
        row-=1
    elif opIndex == 1:
        col -=1
    elif opIndex == 3:
        col +=1 
    if matrix[row][col] == '*':
        return True
    return False

def moveUntilCant(matrix,opIndex,number, gardener : Gardener, leafMax):
    operation=[dole,vlavo,hore,vpravo]
    #nastavenie hrabaca na farbu ktora je v mape
    #vykonavaj pohyb dokym nevrati false
    while(operation[opIndex](matrix,number,gardener)):
        #ak pozbieral listy farby tak sa nastivi dalsia uroven listov
        if gardener.cColor != 'c' and gardener.pocetPozbieranych[leaves.index(gardener.cColor)] == leafMax[leaves.index(gardener.cColor)]:
            gardener.cColor = leaves[leaves.index(gardener.cColor)+1]
    #kontrola ci po zastaveni zastavil mimo plochy alebo v nej
    return isOutOfBounds(gardener,matrix,opIndex)