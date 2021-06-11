from BusquedaProfundidad import busqueda_profundidad
from BusquedaAnchura import busqueda_anchura
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
import matplotlib.animation as animation
import sys

fig = plt.figure(figsize=(5.5,5.5))
ax1 = fig.add_subplot()
root = tk.Tk()
root.title("Práctica 2")

columna = 0
fila = 0
mapeo = []
bandera_ep = False
nodos_recorridos = []
nodos_opcion = []
arreglo = []
bandera_ba = False
bandera_bp = False

doc = open("doc.txt","r").read()
filas = doc.split("\n")
row = len(filas)
col = len(filas[0].split(","))
lista = []
for fila in filas:
    aux = fila.split(",")
    for car in aux:
        lista.append(int(car))
mapa = np.array(lista).reshape(row,col)


#print(mapa)
ax1.xaxis.set_ticks_position('top')
ax1.set_xticks(np.arange(1,col+1))
ax1.set_yticks(np.arange(1,row+1))
ax1.grid(color='k')

def definirMapa():
    global mapeo
    global bandera_ep
    global ax1
    if not bandera_ep:
        mapeo = np.full((row,col),2)
        im = ax1.imshow(mapeo,cmap = ListedColormap(['k']), extent = [1,col+1,row+1,1])
    else:
        im = ax1.imshow(mapeo,cmap = ListedColormap(['gray',"w","k"]), extent = [1,col+1,row+1,1])
    im = None
    
    return mapa

def animate(i):
    global bandera_ba, bandera_bp
    if bandera_bp: 
        recorrer_mapa()
    if bandera_ba:
        recorrer_mapabp()
    definirMapa()


def muestraMapa():
    
    root_panel = tk.Frame()
    root_panel.pack()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=5, pady=10, side=tk.LEFT)

    btn_mc = tk.Button(root, #root_panel
                     text = "Mostrar valor de Casilla",
                     command= lambda: mostrarCasilla(definirMapa()))    
    btn_mc.pack(padx=5, pady=10, )#side=tk.LEFT)

    btn_cc = tk.Button(root, #root_panel
                     text = "Cambiar valor de Casilla",
                     command= lambda: cambiarCasilla())       
    btn_cc.pack(padx=5, pady=10, )#side=tk.LEFT)

    btn_bp = tk.Button(root, #root_panel
                     text = "Busqueda por profundidad",
                     command= lambda: definir_criterio())       
    btn_bp.pack(padx=5, pady=10, )

    btn_bp = tk.Button(root, #root_panel
                     text = "Busqueda por anchura",
                     command= lambda: definir_ba())       
    btn_bp.pack(padx=5, pady=10, )

    root.bind("<Key>",eventoClick)
    
    intervalo = 1000
    ani = animation.FuncAnimation(fig, animate, interval=intervalo,cache_frame_data=False,save_count=0) 
    
    global columna, fila
    arreglo = establecerPosiciones()
    columna, fila = arreglo[0],arreglo[1]

    root.mainloop()

def definir_ba():
    global arreglo, bandera_ba
    x_inicial, y_inicial, x_final, y_final = arreglo[0],arreglo[1],arreglo[2],arreglo[3]
    global nodos_recorridos,nodos_opcion
    nodos_recorridos,nodos_opcion = busqueda_anchura(x_inicial,y_inicial,x_final,y_final,mapa)
    bandera_ba = True

def recorrer_mapabp():
    global nodos_recorridos,nodos_opcion
    if nodos_opcion:
        nodo_opcion = nodos_opcion.pop()
        indice = nodos_recorridos.index(nodo_opcion)
        lista = []
        for i in range(0,indice+1):
            lista.append(nodos_recorridos[0])
            nodos_recorridos.remove(nodos_recorridos[0])   
        for tupla in lista:
            plt.text(float(tupla[0]+1)+.3,float(tupla[1]+1)+.7,"V")
            mapear(tupla[1]+1, tupla[0]+1)

def definir_criterio():
    global arreglo
    global nodos_recorridos
    global bandera_bp
    bandera_bp = True
    mapa = definirMapa()
    x_inicial, y_inicial, x_final, y_final = arreglo[0],arreglo[1],arreglo[2],arreglo[3]
    cadena = simpledialog.askstring("Criterio","Ingrese el orden separado por comas, A:Arriba, D:Derecha, I:Izquierda, B:Abajo", parent=root) 
    if cadena != None:
        criterio = cadena.split(",")
        nodos_recorridos = busqueda_profundidad(x_inicial,y_inicial,x_final, y_final,mapa,criterio)

def recorrer_mapa():
    global nodos_recorridos
    if nodos_recorridos != []:        
        pos = nodos_recorridos.pop()
        print(pos[0]+1,pos[1]+1)
        plt.text(float(pos[0]+1)+.3,float(pos[1]+1)+.7,"V")
        mapear(pos[1]+1, pos[0]+1)
        
def eventoClick(event):
    if event.keysym == "Escape":
        root.destroy()
        sys.exit()

def mapear(fila, columna):
    mapa = definirMapa()
    fila = fila-1
    columna = columna-1
    posicion = mapa[fila,columna] 
    if posicion == 1:
        mapeo[fila,columna] = mapa[fila,columna] #actual
        if fila+1<mapa.shape[0]:
            mapeo[fila+1,columna] = mapa[fila+1,columna] #abajo
        if fila-1 >=0:
            mapeo[fila-1,columna] = mapa[fila-1,columna] #arriba
        if columna+1 < mapa.shape[1]:
            mapeo[fila,columna+1] = mapa[fila,columna+1] #derecha
        if columna-1 >= 0: 
            mapeo[fila,columna-1] = mapa[fila,columna-1] #izquierda
       

def establecerPosiciones():
    mapa = definirMapa()
    global mapeo
    global bandera_ep
    global arreglo
    valorColInic = simpledialog.askinteger("Columna","Ingrese el valor de la columna inicial", parent=root) 
    valorFilaInic = simpledialog.askinteger("Fila","Ingrese el valor de la fila inicial",parent=root) 
    if mapa[valorFilaInic-1,valorColInic-1] ==  1:
        valorColFin = simpledialog.askinteger("Columna","Ingrese el valor de la columna final", parent=root) 
        valorFilaFin = simpledialog.askinteger("Fila","Ingrese el valor de la fila final",parent=root)  
        if mapa[valorFilaFin-1,valorColFin-1] == 1:
            plt.text(float(valorColInic)+.2,float(valorFilaInic)+.7,"I")
            plt.text(float(valorColInic)+.3,float(valorFilaInic)+.7,"V")
    else:
        messagebox.showerror("Error","Ingrese datos validos")

    plt.text(float(valorColFin)+.5,float(valorFilaFin)+.7,"F")
    mapear(valorFilaInic,valorColInic)
    bandera_ep = True
    arreglo = [valorColInic-1, valorFilaInic-1,valorColFin-1, valorFilaFin-1]
    return arreglo

def mostrarCasilla(mapa):
    valorCol = simpledialog.askinteger("Columna","Ingrese el valor de la columna deseada", parent=root) 
    valorFila = simpledialog.askinteger("Fila","Ingrese el valor de la fila deseada",parent=root) 
    if (valorCol and valorFila) is not None:
        if mapa[valorFila-1,valorCol-1] == 0:
            valor = "Valor de casilla: Muro"
        elif mapa[valorFila-1,valorCol-1] == 1:
            valor = "Valor de casilla: Pasillo"
        else: 
            valor = "Valor de casilla: No definido"
        messagebox.showinfo("Valor",valor)    
    else:
        messagebox.showerror("Error","Ingrese datos validos")

def cambiarCasilla():
    global mapa, mapeo
    valorCol = simpledialog.askinteger("Columna","Ingrese el valor de la columna deseada", parent=root) 
    valorFila = simpledialog.askinteger("Fila","Ingrese el valor de la fila deseada",parent=root) 
    nuevoValor = simpledialog.askinteger("Nuevo valor","Ingrese el nuevo valor",parent=root) 
    if (valorCol and valorFila) is not None:
        mapa[valorFila-1,valorCol-1] = nuevoValor
        mapeo[valorFila-1,valorCol-1] = nuevoValor
    else:
        messagebox.showerror("Error","Ingrese datos validos")


muestraMapa()
