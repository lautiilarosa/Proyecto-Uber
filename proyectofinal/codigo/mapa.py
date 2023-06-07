import math
import pickle
import sys 
import ast
 
def createMap(archivo):
    print("A")
    with open(archivo, "rb") as pickle_f:
     listaEsquinas = eval(pickle.load(pickle_f))
     listaAristas = ast.literal_eval(pickle.load(pickle_f))
     
     map = createGraph(listaEsquinas, listaAristas)
     print("MAPA CREADO CORRECTAMENTE")
    return map
    

def createGraph(LV,LA):
  graph = {}
  for i in range(len(LV)):
    LV[i] = LV[i].lower()
    connectvertex = {}
    graph[LV[i]] = connectvertex
    for j in range(len(LA)):
      LA[j][0] = LA[j][0].lower()
      if LV[i] == LA[j][0]:
        LA[j][1] = LA[j][1].lower()
        connectvertex[LA[j][1]] = LA[j][2]
  return graph      
