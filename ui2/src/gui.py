import tkinter as tk
from tkinter.constants import ALL


#funckie pre vizualizaciu riešení

#zoberie finalny uzol spatne zoberie vsetky uzly na ceste ku korenu - pociatocnemu uzlu
def createOutputForTkinter(nodes):
    stavy = []
    while nodes != 0:
        stavy.append(nodes)
        nodes = nodes.parent
    return stavy

#funckia na vytvorenie okna
def showSolution(nodes1, nodes2, nodes3):
    #ziskanie stavov na vykreslenie
    stavy1 = createOutputForTkinter(nodes1)
    stavy2 = createOutputForTkinter(nodes2)
    stavy3 = createOutputForTkinter(nodes3)

    #nastavenie poctu riadkov a stlpcov
    rows = nodes1.stav.rows
    cols = nodes1.stav.cols

    global window 
    window = tk.Tk()
    global canvas
    canvas = tk.Canvas(window,width=500,height=500)
    canvas.pack()

    initOffset = 30
    squareSize = 30
    initOffset2 = initOffset + rows*(squareSize+3) + 30
    initOffset3 = initOffset2 + rows*(squareSize+3) + 30
    window.deiconify()

    squareSize = 30

    canvas.delete(ALL)
    canvas.create_text(100,10, text="Heuristika zle ulozenych cisiel: ")
    canvas.create_text(150,initOffset2-20, text="Heuristika podla vzdialenosti k spravnemu miestu: ")
    canvas.create_text(100,initOffset3-20, text="Kombinacia oboch: ")
    firstHla = drawHlavolam(rows,cols,initOffset,initOffset,squareSize)
    secondHla = drawHlavolam(rows,cols,initOffset2,initOffset,squareSize)
    thirdHla = drawHlavolam(rows,cols,initOffset3,initOffset,squareSize)

    #nastavuje klavesu space na prepnutie na dalsi krok
    canvas.bind("<space>", lambda event, r = rows, c = cols: drawCallback(stavy1,stavy2,stavy3,r,c,firstHla,secondHla, thirdHla))
    initOffset = 30
    canvas.focus_set()
    window.mainloop()


#vykresli pociatocny hlavolam a vrati tuple tkinter id pre data
def drawHlavolam(rows, cols, offset,offset2,squareSize):
    squares = []
    texts = []
    heur = canvas.create_text(offset2+cols*(squareSize+3)+100,offset,text="Hodnota: xxx")
    for i in range(rows):
        for j in range(cols):
            squares.append(canvas.create_rectangle(offset2+j*(squareSize+3),offset+i*(squareSize+3),
                            offset2+j*(squareSize+3)+squareSize,offset+i*(squareSize+3)+squareSize, fill="red"))
            texts.append(canvas.create_text(offset2+j*(squareSize+3)+squareSize//2,offset+i*(squareSize+3)+squareSize//2,text="0"))
    return (heur,squares,texts)

#spusta vykreslovanie stavov
def drawCallback(stavy,stavy2,stavy3,r,c,fH,sH, tH):
    if len(stavy) == 0 and len(stavy2) == 0 and len(stavy3) == 0:
        #ak uz boli vybrate vsetky kroky riesenia
        window.destroy()
    else:
        if len(stavy) >0:
            draw(stavy.pop(),r,c,fH[1],fH[2],fH[0])
        if len(stavy2) > 0:
            draw(stavy2.pop(),r,c,sH[1],sH[2],sH[0])
        if len(stavy3) > 0:
            draw(stavy3.pop(),r,c,tH[1],tH[2],tH[0])

#vykresluje krok ku rieseniu
def draw(node,rows,cols,squares,texts,h):
    canvas.itemconfigure(h,text="hodnota:" + str(node.getHeuristika()))
    for i in range(rows):
        for j in range(cols):
            mat = node.stav.matrix[i*cols+j]
            if mat == 0:
                #skryva stvorceky s prazdnym miestom
                canvas.itemconfigure(squares[i*cols+j],fill="red", state='hidden')
                canvas.itemconfigure(texts[i*cols+j],state='hidden')
            else:
                canvas.itemconfigure(squares[i*cols+j],state='normal')
                canvas.itemconfigure(texts[i*cols+j],text=str(mat),state='normal')