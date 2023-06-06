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
    
class GraphNode:
  vertex = None
  conectList = None
  EdgesListofGraph = None

  #PARA DJIKSTRA:
  parent = None
  #d; estimacion del camino mas corto
  d = None
  

class NodoAsociado:
  vertex1 = None
  peso = None
  asociadoA = None
  
def createGraph(LV,LA):
  listAdyacencia = []
  for i in range(len(LV)):
    Node = GraphNode()
    Node.vertex = LV[i]
    Node.conectList = []
    listAdyacencia.append(Node)
    
  for i in range(len(LV)):
    listAdyacencia[i].conectList = []
    for j in range(len(LA)):
      if LV[i] == LA[j][0]:
        NodoconectList = NodoAsociado()
        NodoconectList.vertex1 = LA[j][1]
        NodoconectList.peso = LA[j][2]
        NodoconectList.asociadoA = LA[j][0]
        listAdyacencia[i].conectList.append(NodoconectList)
  listAdyacencia[0].EdgesListofGraph = LA
  print("map created successfully")
  return listAdyacencia
