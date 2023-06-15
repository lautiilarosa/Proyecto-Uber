import math
import sys
import pickle

class nodeDictionary:
    esquina = None
    d = None
    parent = None
    


def calculoDistanciaAutosPersonas(listadoElementos, mapa, dicAutos):
    #un doble for lamentablemente :( ¿se podra mejorar?
    for key in listadoElementos:
        if key[0] == "c":
            dicAutos[key] = {}
            for keyP in listadoElementos:
              if keyP[0] == "p":
                distanceValue = calculoDistanciaCA(listadoElementos, key, keyP, mapa)
                dicAutos[key][keyP] = distanceValue 
    return dicAutos

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


#Djikstra:
#El mapa es el diccionario, la esquinaInicio seria donde partimos pero como key, es decir "e1" por ejemplo.

def initRelax(mapa, esquinaInicio):
  for esquinas in mapa:
    mapa[esquinas]["Node"].esquina = esquinas
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
      if busquedaElemento(listaVerticesUsados, esquinaAdyacente) == None and esquinaAdyacente != "Node":
        relax(verticeAUsar.esquina, esquinaAdyacente, mapa)


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
  #ESTE SERA EL CASO DONDE ESTAN EN LA MISMA CALLE:
  if (primeraEsquina == primeraEsquinaPersona or primeraEsquina == segundaEsquinaPersona) and (segundaEsquina == primeraEsquinaPersona or segundaEsquina == segundaEsquinaPersona):
    if (segundaEsquina in Mapa[primeraEsquina]) and (primeraEsquina in Mapa[segundaEsquina]):
      #doble Mano, hay que respetar APUNTANDO A UNO DE LOS NODOS NADA MAS:
      if primeraEsquina == primeraEsquinaPersona:
        distancia = abs(diccionarioElementos[keyAuto][0][0][1] - diccionarioElementos[keyPersona][0][0][1])
        return distancia
      if primeraEsquina == segundaEsquinaPersona:
        distancia = abs(diccionarioElementos[keyAuto][0][0][1] - diccionarioElementos[keyPersona][0][1][1])
        return distancia
      
    if segundaEsquina in Mapa[primeraEsquina]:
      #tengo que saber bien cual de las dos esquinas de la persona coincide con la segunda esquina del auto(?):
      if segundaEsquina == primeraEsquinaPersona:
        distanciaPersonaSegundaEsquina = diccionarioElementos[keyPersona][0][0][1]
      else:
        distanciaPersonaSegundaEsquina = diccionarioElementos[keyPersona][0][1][1]
      
      distancia = diccionarioElementos[keyAuto][0][1][1] - distanciaPersonaSegundaEsquina
      if distancia >= 0:
        return distancia
    
    if primeraEsquina in Mapa[segundaEsquina]:
      if primeraEsquina == primeraEsquinaPersona:
        distanciaPersonaPrimeraEsquina = diccionarioElementos[keyPersona][0][0][1]
      else:
        distanciaPersonaPrimeraEsquina = diccionarioElementos[keyPersona][0][1][1]
      
      distancia = diccionarioElementos[keyAuto][0][0][1] - distanciaPersonaPrimeraEsquina
      if distancia >= 0:
        return distancia
        
  
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
  