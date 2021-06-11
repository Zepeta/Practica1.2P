from os import pardir
import numpy as np
import time
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

def busqueda_anchura(x_inicial, y_inicial,x_final, y_final,mapa):
    x = x_inicial
    y = y_inicial
    posicion_final = (x_final,y_final)
    nodos_recorridos = []
    opciones = dict.fromkeys(["A","B","D","I"],False) 
    nodos_recorridos.append((x,y))
    nivel = []
    aux = []
    nivel.append((x,y))
    nodos_opcion = []
    while posicion_final not in nivel and posicion_final not in nodos_recorridos:
        if (x,y) not in nodos_opcion:
            nodos_opcion.append((x,y))
        while nivel:
            nodo_padre = nivel.pop()
            x,y = nodo_padre[0],nodo_padre[1] 
            contador_opciones, opciones =  verificar_opciones(mapa,opciones,x,y,nodos_recorridos)
            if contador_opciones == 1:
                x,y = avanzar_derecho(mapa, x,y,opciones,nodos_recorridos,posicion_final)
                nivel.append((x,y))
                if (x,y) not in nodos_opcion:
                    nodos_opcion.append((x,y))
                break
            elif contador_opciones > 1:
                keys_opc = list(opciones.keys())
                values_opc = list(opciones.values())
                while keys_opc and values_opc:
                    opciones = dict.fromkeys(["A","B","D","I"],False) 
                    camino,valor = keys_opc.pop(), values_opc.pop()
                    if valor:
                        if camino == "A":
                            y-=1
                        elif camino == "B":
                            y+=1
                        elif camino == "D":
                            x+=1   
                        elif camino == "I":
                            x-=1 
                        nodos_recorridos.append((x,y))
                        x,y = avanzar_derecho(mapa,x,y,opciones,nodos_recorridos, posicion_final)
                        aux.append((x,y))                    
                        x,y = nodo_padre[0],nodo_padre[1] 
        for elemento in aux:
            nivel.append(elemento)
            if elemento not in nodos_opcion:
                nodos_opcion.append(elemento)
        aux.clear()
        #print(nivel)
        if posicion_final in nivel or posicion_final in nodos_recorridos:
            print("Se llegó")         
        #time.sleep(0.5)
    nodos_opcion.reverse()
    return nodos_recorridos, nodos_opcion
    
def avanzar_derecho(mapa, x,y,opciones,nodos_recorridos, posicion_final):
    cont = 1
    while cont==1:
        if True in list(opciones.values()):
            camino = list(opciones.keys())[list(opciones.values()).index(True)]
            if camino == "A":
                y-=1                
            elif camino == "B":
                y+=1                     
            elif camino == "D":
                x+=1                     
            elif camino == "I":
                x-=1   
        if (x,y) not in nodos_recorridos:
            nodos_recorridos.append((x,y))
        opciones = dict.fromkeys(["A","B","D","I"],False) 
        cont,camino = verificar_opciones(mapa, opciones, x,y, nodos_recorridos)
        
    return x,y

def verificar_opciones(mapa,opciones, x,y,nodos_recorridos):
    contador_opciones = 0
    arriba = mapa[y-1,x] if y > 0 else 0
    derecha = mapa[y,x+1] if x < 14 else 0
    izquierda = mapa[y,x-1] if x > 0 else 0
    abajo = mapa[y+1,x] if y < 14 else 0
    if arriba == 1 and not (x,y-1) in nodos_recorridos:
        opciones["A"] = True
        contador_opciones+=1
    if abajo == 1 and not (x,y+1) in nodos_recorridos:
        opciones["B"] = True
        contador_opciones+=1
    if derecha == 1 and not (x+1,y) in nodos_recorridos:
        opciones["D"] = True
        contador_opciones+=1  
    if izquierda == 1 and not (x-1,y) in nodos_recorridos:
        opciones["I"] = True
        contador_opciones+=1
    return contador_opciones, opciones     

#busqueda_anchura(0,9,14,1,mapa)

#(5,3)->(3,5)
#(0,9)->(5,3)