import  configparser

#funkcia na ziskanie configuracnych hodnot zo suboru
def getConf(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    if 'Search' in config: 
        tabuSize = int(config['Search']['tabuMaxSize']) if 'tabuMaxSize' in config['Search'] and config['Search']['tabuMaxSize'].isdigit() else 500
        maxIteracie =  int(config['Search']['maxIteracie'])  if 'maxIteracie' in config['Search'] and config['Search']['maxIteracie'].isdigit() else 200
        numOfRepeats =  int(config['Search']['numOfRepeats'])  if 'numOfRepeats' in config['Search'] and config['Search']['numOfRepeats'].isdigit() else 5
        skip =   (True if int(config['Search']['skipUnStartable']) > 0 else False) if 'skipUnStartable' in config['Search'] and config['Search']['skipUnStartable'].isdigit() else False
        minTabuSize= int(config['Search']['minTabuSize'])  if 'minTabuSize' in config['Search'] and config['Search']['minTabuSize'].isdigit() else 100
        maxTabuSize= int(config['Search']['maxTabuSize'])  if 'maxTabuSize' in config['Search'] and config['Search']['maxTabuSize'].isdigit() else 1000
        tabuStep= int(config['Search']['tabuStep'])  if 'tabuStep' in config['Search'] and config['Search']['tabuStep'].isdigit() else 100
        chooseWorse =  (True if int(config['Search']['chooseWorse']) > 0 else False) if 'chooseWorse' in config['Search'] and config['Search']['chooseWorse'].isdigit() else False
    else:
        tabuSize = 500
        maxIteracie = 200
        numOfRepeats =  5
        skip =   False
        minTabuSize= 100
        maxTabuSize= 1000
        tabuStep=1000
        chooseWorse = False

    if 'swaps' in config:
        enableSwaps = int(config['swaps']['enable'])  if 'enable' in config['swaps'] and config['swaps']['enable'].isdigit() else 0
    else:
        enableSwaps = 0

    if 'neighbors' in config:
        randomNeighbors =  int(config['neighbors']['random'])  if 'random' in config['neighbors'] and config['neighbors']['random'].isdigit() else 0
    else:
        randomNeighbors =  0

    if 'Stones' in config and 'count' in config['Stones'] and config['Stones']['count'].isdigit():
        count =  int(config['Stones']['count'])
    else:
        count = 5
    if 'Leaf' in config:
        yellow =  int(config['Leaf']['yellow']) if 'yellow' in config['Leaf'] and config['Leaf']['yellow'].isdigit() else 4
        orange =  int(config['Leaf']['orange']) if 'orange' in config['Leaf'] and config['Leaf']['orange'].isdigit() else 7
        red =  int(config['Leaf']['red']) if 'red' in config['Leaf'] and config['Leaf']['red'].isdigit() else 10
    else:
        yellow = 4
        orange =  7
        red =  10

    return [tabuSize,randomNeighbors,maxIteracie,numOfRepeats,skip,minTabuSize,maxTabuSize,tabuStep,enableSwaps,chooseWorse],[count],[yellow,orange,red]
