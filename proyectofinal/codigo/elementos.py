import math
import sys
import pickle

class nodeDictionary:
    esquina = None
    d = None
    parent = None
    
nodo1 = nodeDictionary()
nodo2 = nodeDictionary()
nodo3 = nodeDictionary()
nodo4 = nodeDictionary()
nodo5 = nodeDictionary()
nodo6 = nodeDictionary()
nodo7 = nodeDictionary()
nodo8 = nodeDictionary()
nodo9 = nodeDictionary()
nodo10= nodeDictionary()
nodo11= nodeDictionary()



mapitaPrueba = {
  "e1": {
    "Node": nodo1,
    "e2": 5
  },
  
  "e2": {
    "Node": nodo2,
    "e4": 6
  },
  
  "e3": {
    "Node": nodo3,
    "e2": 6
    },

  "e4": {
    "Node": nodo4
  },
  
  "e5":{
    "Node": nodo5,
    "e3": 4,
    "e7": 8
    },

  "e6": {
    "Node": nodo6,
    "e5": 12,
    "e7": 11,
    "e8": 10
    },

  "e7": {
    "Node": nodo7,
    "e6": 11
    },

  "e8": {
    "Node": nodo8,
    "e6": 10,
    "e10": 9
    },

  "e9": {
    "Node": nodo9,
    "e8": 7
    },

  "e10": {
    "Node": nodo10,
    "e1": 30
    },

  "e11": {
    "Node": nodo11,
    "e6": 7
  }
  }
#quiero creer que las cosas las va a cargar como: 
# fix_element : [H1, [e1,]]
# listadoCP seria como un diccionario, que contenga;
diccionarioE = {
    "C1": [[("e2",4),("e4",2)], 1000],
    "P1": [[("e1",20),("e10",10)],1000],
    "P2": [[("e9",2),("e8",5)],1000],
    "H1": [("e4",3),("e2",3)],
    "C2": [[("e6",4),("e11",3)],1000],
    "P3": [[("e7",7),("e6",4)],1000],
    "E1": [("e1",16),("e10",14)],
    "P4": [[("e3",3),("e2",3)],1000],
    "H2": [("e1",4),("e2",1)],
    "H3": [("e9",5),("e8",2)],
    "P5": [[("e1",1),("e2",4)],1000],
    "C3": [[("e5",6),("e6",6)],1000],
    "C4": [[("e8",5),("e10",4)],1000],
    "E2": [("e6",4),("e8",6)],
    "C5": [[("e5",7),("e7",1)],1000],
    "P6": [[("e6",1),("e11",6)],1000],
}

#Y si pudieramos crear como resultado de esta funcion un diccionario que tenga de keys los autos, como values otro diccionarios 
# que estos a su vez tengan como keys las personas y sus respectivas distancias
# que el load_fix_element cargue 
#Suponiendo que es diccionario que guarda el nombre de los elementos como keys y su direccion [("e1",4),("e2",10)] como value

#deberia de recibir como parametro dicAutos porque si no cargara muchos distintos.
def calculoDistanciaAutosPersonas(listadoElementos, mapa):
    dicAutos = {}
    print("FIUMBA")
    #un doble for lamentablemente :( ¿se podra mejorar?
    for key in listadoElementos:
        if key[0] == "C":
            dicAutos[key] = {}
            for keyP in listadoElementos:
              if keyP[0] == "P":
                print("FIUMBA")
                distanceValue = calculoDistanciaCA(listadoElementos, key, keyP, mapa)
                dicAutos[key][keyP] = distanceValue 
    return dicAutos
    #Algoritmo de Djikstra luego:
    


def verificacionDobleMano(Mapa, primeraEsquina, segundaEsquina):
    if segundaEsquina in Mapa[primeraEsquina]:
        if primeraEsquina in Mapa[segundaEsquina]:
            #Aca estamos diciendo que es el caso de que es doble mano
          return [primeraEsquina,segundaEsquina]
        else:
            #Aca vemos que va de direccion de la primera esquina a la segunda, entonces por eso nuestra unica salida es por la segunda.
            return[segundaEsquina]
    else:
        if primeraEsquina in Mapa[segundaEsquina]:
            #Aca ocurre que de la primera esquina no vamos a la segunda, pero puede ocurrir que de la segunda esquina si vamos a la primera. Nuestra unica salida es la primera entonces
            return [primeraEsquina]
        else:
            #Caso donde en realidad no hay salida. Es posible.
            return []

#Por el momento lo que pienso es que vamos a necesitar esta funcion para saber el peso que hay entre u y v. Pero tengo mis dudas.
#Por lo que veo, no estoy tomando solamente el vertice. SI no el NODO que contiene el vertice para poder dar los otros atributos.
#Djikstra:
#El mapa es el diccionario, la esquinaInicio seria donde partimos pero como key, es decir "e1" por ejemplo.

def initRelax(mapa, esquinaInicio):
  for esquinas in mapa:
    mapa[esquinas]["Node"].d = math.inf
    mapa[esquinas]["Node"].parent = None
  mapa[esquinaInicio]["Node"].d = 0
  
def calculoPeso(esquinaInicio, esquinaDestino, mapa):
  if esquinaDestino in mapa[esquinaInicio]:
      return mapa[esquinaInicio][esquinaDestino]
  else:
      return 0
    
def relax(esquinaInicio, esquinaDestino, mapa):
  if mapa[esquinaDestino]["Node"].d > (mapa[esquinaInicio]["Node"].d + calculoPeso(esquinaInicio, esquinaDestino, mapa)):
    mapa[esquinaDestino]["Node"].d = mapa[esquinaInicio]["Node"].d + calculoPeso(esquinaInicio, esquinaDestino, mapa)
    mapa[esquinaDestino]["Node"].parent = esquinaInicio

#minQueue, una funcion donde voy a tener que ordenar los vertices de mi grafo por su atributo d.
#Por lo que estoy viendo, lo que yo habia hecho es: 
#1- a Minqueue le pasamos la lista de vertices usados porque asi vamos a CORROBORAR cuales son los vertices que aun se pueden usar, la lista que se retorna es eso.
#2- Lo que vaya a sacar seria la llave, para luego poder ingresar al valor de esta en mapa
#3- Parece que necesito hacer una lista de nodos :(
#4- el parametro esquina es un string, "c1" "h2"


def minQueue(mapa,listaVerticesUsados):
  lista = []
  for esquina in mapa:
    if busquedaElemento(listaVerticesUsados, esquina) == None:
      lista.append(mapa[esquina]["Node"])
  lista.sort(key=lambda x: x.d)
  return lista

#PARA VERIFICAR SI ESTA EN LA LISTA DE VERTICES USADOS O NO:

def busquedaElemento(lista, elemento):
  try:
    indice = lista.index(elemento)
    return indice
  except ValueError:
    return None

#Estoy viendo que en el tp pidieron representando el grafo con matriz de adyacencia. Este sera como lista de adyacencia
#Que pasa, por que tenemos verticeAdyacente y luego verticeAdyacenteVERDADERO.
#Sucede que con verticeAdyacente nos estamos refiriendo al nodo que se encuentra en el conectlist de uno de los elementos del GRAFO. Si lo llevaramos a las funciones como relax, No funcionaria porque debe leer los atributos, que no son de los Nodos de Conectlist si no de los nodos del Grafo!!.
#Este Djikstra esta pasando valores strings en esquina inicio e-e
#listaVerticesusados deberia de ser nada mas una lista de strings de las esquinas ya usadas
def Djikstra(mapa, esquinaInicio):
  initRelax(mapa, esquinaInicio)
  listaVerticesUsados = []
  verticesOrdenados = minQueue(mapa,listaVerticesUsados)
  while len(verticesOrdenados) > 0:
    verticesOrdenados = minQueue(mapa,listaVerticesUsados)
    #ESTAMOS SACANDO UN NODO EN EL POP, VAMOS A VER COMO LOGRAMOS IMPLEMENTAR.
    verticeAUsar = verticesOrdenados.pop(0)
    listaVerticesUsados.append(verticeAUsar.esquina)
    #este for sera para buscar los adyacentes a la esquina a usar
    #Recordemos, estamos recorriendo en esquinaAdyacente las llaves de los Subdiccionarios del MAPA
    for esquinaAdyacente in mapa[verticeAUsar.esquina]:
      if busquedaElemento(listaVerticesUsados, esquinaAdyacente) == None:
        relax(verticeAUsar, esquinaAdyacente)

#Me parece que un cambio que voy a tener que hacer aca es el agregar la direccion de la persona(?)
def calculoDjikstra(direccionAuto, EsquinaAuto, Mapa, esquina1Persona, esquina2Persona, direccionPersona):
    #La direccion del auto porque acordemonos que no es que exactamente este en una esquina, hay que sumarle unos km mas. 
    #La esquinaAuto seria la esquina a la que tiene que ir si o si para empezar el recorrido.
    #Acordemonos; la direccion del auto esta escrita como: [("e1",4),("e2",10)]
    distancia = 0
    if EsquinaAuto == direccionAuto[0][0]:
        distancia = direccionAuto[0][1]
    else:
        if EsquinaAuto == direccionAuto[1][0]:
            distancia = direccionAuto[1][1]
    #ahora SI POR FINNN LO QUE EL MUNDO ESPERABA, USAR DJIKSTRAAAAA
    Djikstra(Mapa, EsquinaAuto)
    #claramente deben de estar las esquinas de la persona, y si sus d son infinitos, ¿no existe forma de llegar?
    distance1 = Mapa[esquina1Persona]["Node"].d
    distance2 = Mapa[esquina2Persona]["Node"].d
    #Y si sumo antes la distancia de la persona a sus esquinas?:
    distance1 = distance1 + direccionPersona[0][1]
    distance2 = distance2 + direccionPersona[1][1]
    
    #Revisar el sentido de la calle y darle la distancia que le corresponda entonces
    #Primer caso; es una calle de doble sentido y tranquilamente comparamos entre las dos distancias cual es la menor
    #segundo caso; es una calle de un sentido y revisamos como va, y dependiendo de eso tomaremos tal distancia
    #tercer caso; no hay forma de llegar
    if esquina2Persona in Mapa[esquina1Persona] and esquina1Persona in Mapa[esquina2Persona]:
      if distance1 >= distance2:
        distancia = distancia + distance2
      else:
        distancia = distancia + distance1
      return distancia
    
    if esquina2Persona in Mapa[esquina1Persona]:
      distancia = distancia + distance1
      return distancia
    
    if esquina1Persona in Mapa[esquina2Persona]:
      distancia = distancia + distance2
      return distancia
    return math.inf
      

def calculoDistanciaCA(diccionarioElementos, keyAuto, keyPersona, Mapa):
  #verificar si es una calle de doble mano
  primeraEsquina = diccionarioElementos[keyAuto][0][0][0]
  segundaEsquina = diccionarioElementos[keyAuto][0][1][0]
  #Y antes que nada, tambien deberia revisar las esquinas de la persona
  primeraEsquinaPersona = diccionarioElementos[keyPersona][0][0][0]
  segundaEsquinaPersona = diccionarioElementos[keyPersona][0][1][0]
  listaEsquinaC = verificacionDobleMano(Mapa, primeraEsquina, segundaEsquina)
  #Aca bueno, entra la cosa; si mi len de la lista es 2, estan las dos esquinas, si solamente hay una tendremos que ver bien cual es y si no hay ninguna bueno, murio.
  #calculo Djikstra
  if len(listaEsquinaC) == 2:
    distanciaAutoPersona1 = calculoDjikstra(diccionarioElementos[keyAuto][0], listaEsquinaC[0], Mapa, primeraEsquinaPersona, segundaEsquinaPersona, diccionarioElementos[keyPersona][0])
    distanciaAutoPersona2 = calculoDjikstra(diccionarioElementos[keyAuto][0], listaEsquinaC[1], Mapa, primeraEsquinaPersona, segundaEsquinaPersona, diccionarioElementos[keyPersona][0])
    
    if distanciaAutoPersona1 >= distanciaAutoPersona2:
      return distanciaAutoPersona2
    else:
      return distanciaAutoPersona1
    
  if len(listaEsquinaC) == 1:
    distanciaAutoPersona = calculoDjikstra(diccionarioElementos[keyAuto][0], listaEsquinaC[0], Mapa, primeraEsquinaPersona, segundaEsquinaPersona, diccionarioElementos[keyPersona][0])
    return distanciaAutoPersona

  if len(listaEsquinaC) == 0:
    return "No es posible realizar viaje"
  
print("HOLA")    
listadoDistancias = calculoDistanciaAutosPersonas(diccionarioE, mapitaPrueba)
print(listadoDistancias)