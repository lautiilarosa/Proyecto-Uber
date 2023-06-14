import math
import pickle
import sys 
import ast
import re
 
class graphnode:
  distance = None
  parent = None
  color = None

#Deserializar el archivo pickle
def createMap(archivo):
    with open(archivo, "rb") as pickle_f:
     datosArchivo = pickle.load(pickle_f)
     datosArchivo2 = pickle.load(pickle_f)
     if datosArchivo != "" and isinstance(datosArchivo, str): 
       datosArchivo = str(datosArchivo)

       datosArchivo = datosArchivo[3:]
       datosArchivo = datosArchivo.replace("{","")
       datosArchivo = datosArchivo.replace("}","")
       datosArchivo = datosArchivo.strip()
       
       listaEsquinas = datosArchivo.split(",")

       datosArchivo2 = str(datosArchivo2)
 
       # Obtener los valores entre < y >
  
       valores = re.findall(r'<([^>]*)>', datosArchivo2)

       # Dividir cada valor por comas y crear una lista de tuplas
       listaAristas = [tuple(int(valor) if valor.isdigit() else valor for valor in valor.split(',')) for valor in valores]
     else:
       print("mapa vacio")
       return 
     
     map = createGraph(listaEsquinas, listaAristas)
    return map
    
#crear el grafo 
def createGraph(LV,LA):
  graph = {}
  for i in range(len(LV)):
    nodo = graphnode()
    LV[i] = LV[i].lower()
    connectvertex = {}
    graph[LV[i]] = connectvertex
    connectvertex["Node"] = nodo
    for j in range(len(LA)):
      #LA[j][0] = LA[j][0].lower()
      if LV[i] == LA[j][0]:
        #LA[j][1] = LA[j][1].lower()
        connectvertex[LA[j][1]] = LA[j][2]
  return graph      
