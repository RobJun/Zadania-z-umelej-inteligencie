from matplotlib import pyplot as plt


#zberac udajov ktory vytvori graf z id ktore zbiera
class DataCollector:
    def __init__(self) -> None:
        self.collections = []
        pass


    def __call__(self,colId,data : tuple):
        self.addToCollection(colId,data)

    #returns collection id do ktoreho mozeme vkladat data
    def createCollection(self,numOfAxis, Name):
        if numOfAxis != 2:
            print("ERROR --- num of axis can be 2 or 3")
            return 0;
        self.collections.append([[] for i in range(numOfAxis+1)])
        self.collections[-1][0] = Name
        return len(self.collections)

    def addToCollection(self,colId,data : tuple):
        if len(self.collections) < colId-1:
            print("ERROR --- collection id not right")
            return;
        if len(self.collections[colId-1]) != len(data)+1:
            print("ERROR --- incorrect number of axis")
            return;

        for i in range(len(data)):
            self.collections[colId-1][i+1].append(data[i])

    #ukazanie grafu
    def create2dGraphFromIds(self,title,axisNames,*colIds):
        plt.cla()
        plt.title(title)
        plt.xlabel(axisNames[0])
        plt.ylabel(axisNames[1])
        for i in colIds:
            if isinstance(i,list):
                for j in i:
                    if len(self.collections[j-1][1]) == 1:
                        plt.plot(self.collections[j-1][1],self.collections[j-1][2],'o',label=self.collections[j-1][0])
                    else:
                        plt.plot(self.collections[j-1][1],self.collections[j-1][2],label=self.collections[j-1][0])
            else:
                if len(self.collections[i-1][1]) == 1:
                    plt.plot(self.collections[i-1][1],self.collections[i-1][2],'o',label=self.collections[i-1][0])
                else:
                    plt.plot(self.collections[i-1][1],self.collections[i-1][2],label=self.collections[i-1][0])
        plt.legend()
        plt.show()
        

        
