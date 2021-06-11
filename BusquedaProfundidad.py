import numpy as np
import time
#busqueda_profundidad(5, 3, 12, 1,mapa,["D","A","B","I"])
def busqueda_profundidad(x_inicial, y_inicial, x_final, y_final,mapa,criterio):
    x = x_inicial
    y = y_inicial
    nodos_recorridos = []
    posicion_final = (x_final,y_final)
    posicion_actual = (x,y)
    camino = ""
    ruta = []
    ruta.append((x_inicial,y_inicial))
    while  posicion_actual != posicion_final:      
        opciones = dict.fromkeys(criterio,False)          
        nodos_recorridos.append(posicion_actual)
        contador_opciones, opciones = verificar_opciones(mapa, opciones,x,y,nodos_recorridos)
        # print(posicion_actual)
        # print(opciones)
        # print(nodos_recorridos)
        if contador_opciones==1:    
            camino = list(opciones.keys())[list(opciones.values()).index(True)]
            if camino == "A":
                y-=1                
            elif camino == "B":
                y+=1                     
            elif camino == "D":
                x+=1                     
            elif camino == "I":
                x-=1        
            posicion_actual = (x,y)
        elif contador_opciones>1:
            if not posicion_actual in ruta:
                ruta.append(posicion_actual)
            # print("ruta",ruta)
            keys_opc = list(opciones.keys())
            values_opc = list(opciones.values())
            keys_opc.reverse()
            values_opc.reverse()                   
            while keys_opc and values_opc:
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
                    break    
            posicion_actual = (x,y)                                    
        elif contador_opciones==0:
            posicion_actual = ruta.pop()    
            x = posicion_actual[0]
            y = posicion_actual[1]
            # print("regreso",posicion_actual)
            # print("ruta",ruta)
        if posicion_actual==posicion_final:
            print("Haz llegado!!!")        
            if (x_inicial,y_inicial) not in ruta:
                ruta.insert(0,(x_inicial,y_inicial))    
            ruta.append(posicion_actual)
            nodos_recorridos.append(posicion_actual)
        #time.sleep(0.5) 
    nodos_recorridos.reverse()    
    print(ruta)
    return nodos_recorridos

def verificar_opciones(mapa,opciones,x,y,nodos_recorridos):
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
                 
         
# doc = open("doc.txt","r").read()
# filas = doc.split("\n")
# row = len(filas)
# col = len(filas[0].split(","))
# lista = []
# for fila in filas:
#     aux = fila.split(",")
#     for car in aux:
#         lista.append(int(car))
# mapa = np.array(lista).reshape(row,col)
# busqueda_profundidad(5, 3, 7, 8,mapa,["D","B","A","I"])


# (5,3)->(12,1)
# (0,9)->(12,1)
# (3,1) -> (3,9)