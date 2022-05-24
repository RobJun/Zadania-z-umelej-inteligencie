import random
import time
import math
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as n

POCET_BODOV = 5000
ROZMER_MRIEZKY = 200
ROZMER_PLOCHY = 50                  

#funkcia vrati vzdialenost bodov vypocitanu vzorcom na eulerovu vzdialenost
def eulerova_vzdialenost(x1, y1, x2, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

#funkcia vrati zoznam vzdialenosti bodov, dlhy k
def zoznam_vzdialenosti(zoznam_bodov, x, y, vzdialenosti, k):
    vzdialenosti2 = vzdialenosti[:]
    for bod in zoznam_bodov:                                                                #pre kazdy bod v danom stvorci
        bol_vlozeny = False
        euler_vzdialenost = eulerova_vzdialenost(x, y,bod[0], bod[1])                       #vypocitame vzdialenost od bodu, ktory ideme klasifikovat
        for i in range(len(vzdialenosti2)):                                                    
            if(euler_vzdialenost < vzdialenosti2[i][0]):                                    #tuto vzdialenost porovname so vzdialenostami, ktore uz v zozname su
                vzdialenosti2.insert(i, (euler_vzdialenost, bod[2], bod[0], bod[1], k))     #a vlozime ju na jej spravne miesto - vytvarame usporiadany zoznam
                bol_vlozeny = True
                if(len(vzdialenosti2) == k+1):                                              #ak uz zoznam vzdialenosti bol velky k, tak posledny prvok vymazeme
                    vzdialenosti2.pop()
                break                                                                   
        if not bol_vlozeny and len(vzdialenosti2) < k:                                      #ak sme ho nikam nevlozili, ale zoznam este nie je velky k
            vzdialenosti2.append((euler_vzdialenost, bod[2], bod[0], bod[1], k))            #tak ho vlozime nakoniec
    return vzdialenosti2

#funkcia vrati ci sa suradnice stvorca nachadzaju uz mimo plochy
def mimo_plochy(x, y):
    return (x >= 50 or x < 0 or y < 0 or y >= 50)

#rekurzivna funkcia vrati zoznam k najblizsich bodov od bodu
def najdi_obvod(obvod, vyskusane, x, y, k, zoznam_vzdialenosti_k_najblizsich, plocha):
    while (len(obvod) == 0):                            #ked uz nemame ake stvorce prejst
        return zoznam_vzdialenosti_k_najblizsich        

    novy_obvod = []                                                                                 #novy obvod ktory prehladame - zvacsi sa o 1 stvorce dookola
    zoznam_vzdialenosti_k_najblizsich2 = zoznam_vzdialenosti_k_najblizsich[:]   
    for stvorec in obvod:                                                                           #pre kazdy stvorec v obvode
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not mimo_plochy(stvorec[0] + i, stvorec[1] + j) and not (stvorec[0] + i, stvorec[1] + j) in vyskusane:         #ak suradnice noveho stvorca nie su mimo plochy a este sme ich neprehladali
                    novy_obvod.append((stvorec[0] + i, stvorec[1] + j))                                                           #bude tvorit novy obvod
                    vyskusane.append((stvorec[0] + i, stvorec[1] + j))                                                            #prida sa do vyskusanych, aby sme ich uz nezaratavali v buducnosti
        zoznam_vzdialenosti_k_najblizsich2 = zoznam_vzdialenosti(plocha[stvorec[0]][stvorec[1]], x, y, zoznam_vzdialenosti_k_najblizsich2, k)   #vypocita sa zoznam vzdialenosti na danocm stvorci

    if(len(zoznam_vzdialenosti_k_najblizsich2) == k and zoznam_vzdialenosti_k_najblizsich == zoznam_vzdialenosti_k_najblizsich2):   #ak uz je zoznam dlhy k a zoznam vzdialenosti sa po iteracii nezmenil
        return zoznam_vzdialenosti_k_najblizsich2                                                                                   #tak sa hladanie k najblizcisch bodov ukoncuje
    return najdi_obvod(novy_obvod,vyskusane, x, y, k, zoznam_vzdialenosti_k_najblizsich2, plocha)                                   #inak sa zvacsi obvod a hlada sa dalej

#funkcia klasifikuje dany bod -> vrati farbu, akou by mal byt zafarbeny
def classify(x, y, k, plocha, realna_pozicia_y, realna_pozicia_x):
    obvod = [(realna_pozicia_x, realna_pozicia_y)]                                  #zoznam stvorcov ktore tvoria obvod, ktore ale len budeme prehladavat
    vyskusane = [(realna_pozicia_x, realna_pozicia_y)]                              #zoznam stvorcov ktore budem prehladavat ale ktore sme uz aj prehladali
    zoznam_vzdialenosti = najdi_obvod(obvod, vyskusane, x, y, k, [], plocha)        #zoznam k bodov, ktore su najblizsie pri bode
   
    pocty = { "R" : 0, "G" : 0, "B" : 0, "P" : 0}
    for i in zoznam_vzdialenosti:                                                               #spravenie statistiky farby, ktora sa najvaiac vyskytuje v zozname vzdialenosti
        pocty[i[1]] += 1 
    return [n for n, v in sorted(pocty.items(), key=lambda item: item[1], reverse=True)][0]     #touto farbou klasifikujeme bod

#funkcia na vizualizaciu riesenia
def vykresli(zoznam_bodov, k, subplot):
    x = []                                                                                          
    y = []
    f = []
    z = []
    cmap = ListedColormap(['#ff4444', '#8fce00', '#6ebaff', '#ac7fe2'])
    cmapBACK = ListedColormap(['#f48383', '#cbff56', '#b2daff', '#ddc3fc'])

    #vytvaranie x, y, farba zoznamov na vizualizaciu klasifikovanych bodov
    for i in zoznam_bodov:
        for m in i:  
            for j in m:
                x.append(j[0])
                y.append(j[1])
                if(j[2] == "R"): f.append(0)
                elif(j[2] == "G"): f.append(1)
                if(j[2] == "B"): f.append(2)
                if(j[2] == "P"): f.append(3)

    #klasifikacia volnych ploch 
    for j in range(-5000,5100,100):
        for i in range(-5000,5100,100):
            realna_pozicia_x, realna_pozicia_y = do_ktoreho_strvorca_patria(i, j)
            farba = classify(i, j, k, zoznam_bodov, realna_pozicia_x, realna_pozicia_y)
            if(farba == "R"): z.append(0)
            elif(farba == "G"): z.append(1)
            if(farba == "B"): z.append(2)
            if(farba == "P"): z.append(3)

    npx, npy = n.meshgrid(n.arange(-5000,5100,100),n.arange(-5000,5100,100))
    z = n.array(z).reshape(npx.shape)

    subplot.set_title("k = " + str(k))
    subplot.pcolormesh(npx,npy,z,cmap=cmapBACK,shading='auto',norm=plt.Normalize(vmin=0,vmax=4))
    subplot.scatter(x,y, c = f, cmap = cmap, s = 2, norm=plt.Normalize(vmin=0,vmax=4))
    subplot.set_xlim(-5000, 5000)
    subplot.set_ylim(-5000, 5000)    

#funkcia vrati pozicie stvorca na ploche, v ktorom sa bod ma nachadzat 
def do_ktoreho_strvorca_patria(x, y):
    realna_pozicia_x = ((x + POCET_BODOV) // ROZMER_MRIEZKY)
    realna_pozicia_y = ((y + POCET_BODOV) // ROZMER_MRIEZKY)
    if(realna_pozicia_x != 0): realna_pozicia_x -= 1
    if(realna_pozicia_y != 0): realna_pozicia_y -= 1
    return (realna_pozicia_x, realna_pozicia_y)

#funkcia vrati vygenerovanych 20 000 bodov s priradenou farbou
def generovanie_bodov(plocha):
    vygenerovane_body = [[[] for j in range(ROZMER_PLOCHY)] for i in range(ROZMER_PLOCHY)]      #zoznam bodov ulozenych v ploche
    body = []                                                                                   #zoznam vsetkych bodov v poradi ako boli generovane
    for i in range(POCET_BODOV):     
        for farba in "RGBP":                        #aby sa negenerovali 2 po sebe rovnake farby
            if(random.randint(0,99) == 0):          #bod v celom priestore
                while True:                                                                 #bod sa bude generovat dokym nebude unikatny
                    neunikatny = False
                    x = random.randint(-POCET_BODOV, POCET_BODOV)                           
                    y = random.randint(-POCET_BODOV, POCET_BODOV)
                    realna_pozicia_x, realna_pozicia_y = do_ktoreho_strvorca_patria(x, y)
                    for bod in vygenerovane_body[realna_pozicia_y][realna_pozicia_x]:       #porovnanie ci uz taky bod vygenerovany nebol
                        if(bod[0] == x and bod[1] == y):
                            neunikatny = True
                            break
                    for bod in plocha[realna_pozicia_y][realna_pozicia_x]:                  #porovnanie s zadanymi bodmi
                        if(bod[0] == x and bod[1] == y):
                            neunikatny = True
                            break
                    if(not neunikatny): break                                               
            else:
                while True:
                    neunikatny = False
                    if(farba == "R"):
                        x = random.randint(-POCET_BODOV, 499)
                        y = random.randint(-POCET_BODOV, 499)
                    elif(farba == "G"):
                        x = random.randint(-499, POCET_BODOV)
                        y = random.randint(-POCET_BODOV, 499)
                    elif(farba == "B"):
                        x = random.randint(-POCET_BODOV, 499)
                        y = random.randint(-499, POCET_BODOV)
                    else:
                        x = random.randint(-499, POCET_BODOV)
                        y = random.randint(-499, POCET_BODOV)
                    realna_pozicia_x, realna_pozicia_y = do_ktoreho_strvorca_patria(x, y)  
                    for bod in vygenerovane_body[realna_pozicia_y][realna_pozicia_x]:
                        if(bod[0] == x and bod[1] == y):
                            neunikatny = True
                            break
                    for bod in plocha[realna_pozicia_y][realna_pozicia_x]:
                        if(bod[0] == x and bod[1] == y):
                            neunikatny = True
                            break
                    if(not neunikatny): break
                    
            vygenerovane_body[realna_pozicia_y][realna_pozicia_x].append((x, y, farba))            
            body.append((x,y,farba))
    return body

#funkcia vrati 50x50 plochu so zadanymi bodmi v nej 
def inicializacia_plochy(zaciatocne_body):
    plocha = [[[] for j in range(ROZMER_PLOCHY)] for i in range(ROZMER_PLOCHY)]
    for bod in zaciatocne_body:                 
        realna_pozicia_x, realna_pozicia_y = do_ktoreho_strvorca_patria(bod[0], bod[1])
        plocha[realna_pozicia_y][realna_pozicia_x].append(bod)
    return plocha 

def main():
    zaciatocne_body = [(-4500, -4400, "R"), (-4100, -3000, "R"), (-1800, -2400,"R"), (-2500, -3400, "R"), (-2000, -1400, "R"),
                       (4500, -4400, "G"), (4100, -3000, "G"), (1800, -2400,"G"), (2500, -3400, "G"), (2000, -1400, "G"),
                       (-4500, 4400, "B"), (-4100, 3000, "B"), (-1800, 2400, "B"), (-2500, 3400, "B"), (-2000, 1400, "B"),
                       (4500, 4400, "P"), (4100, 3000, "P"), (1800, 2400,"P"), (2500, 3400, "P"), (2000, 1400, "P")
                      ]
    
    plocha = inicializacia_plochy(zaciatocne_body)

    start = time.time()
    body = generovanie_bodov(plocha)
    end = time.time()
    print("Vygenerovalo sa {} bodov za {} sekúnd.".format(len(body), round(end - start, 2)))

    fig, ax = plt.subplots(2, 2)
    for k, subplot in [(1, ax[0][0]), (3, ax[0][1]), (7, ax[1][0]), (15, ax[1][1])]:
        plocha = inicializacia_plochy(zaciatocne_body)
        statistika = 0
        start = time.time()
        for bod in body:
            x = bod[0]
            y = bod[1]
            realna_pozicia_x, realna_pozicia_y = do_ktoreho_strvorca_patria(x, y)
            farba = classify(x, y, k, plocha, realna_pozicia_x, realna_pozicia_y)               
            if(farba == bod[2]): statistika += 1                                               
            plocha[realna_pozicia_y][realna_pozicia_x].append((x, y, farba))
        end = time.time()
        print("----------------------------------------------------------------")
        print("Štatistika pre k =", k, ":", statistika, " ", round((statistika/20000) * 100, 2), "%")
        print("Klasifikácia všetkých bodov trvala: ", round(end - start, 2), "s")
        start = time.time()
        vykresli(plocha, k, subplot)
        end = time.time()
        print("Vykresľovanie bodov trvalo:", round(end - start, 2), "s")
    fig.show()
    input("stlačte enter na vypnutie programu")
    plt.close()

main()