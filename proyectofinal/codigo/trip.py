from elementos import Djikstra
from ubicaciones import chequear_direccion
import math
     
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

def calculoDjikstraPE(direccionPersona, EsquinaPersona, Mapa, esquinaLugar, esquina2Lugar, direccionLugar):
    
    distancia = 0
    if EsquinaPersona == direccionPersona[0][0]:
        distancia = direccionPersona[0][1]
    else:
        if EsquinaPersona == direccionPersona[1][0]:
            distancia = direccionPersona[1][1]
    
    Djikstra(Mapa, EsquinaPersona)
   
    
    distance1 = Mapa[esquinaLugar]["Node"].d
    currentNode1 = Mapa[esquinaLugar]["Node"]
    lista1 = []
    while currentNode1 != None:
        lista1.insert(0, currentNode1.esquina)
        llaveParent = Mapa[currentNode1.esquina]["Node"].parent
    
        if llaveParent == None:
            currentNode1 = None
        else:
            currentNode1 = Mapa[llaveParent]["Node"]
        
    
    distance2 = Mapa[esquina2Lugar]["Node"].d
    currentNode2 = Mapa[esquina2Lugar]["Node"]
    lista2 = []
    while currentNode2 != None:
        lista2.insert(0, currentNode2.esquina)
        llaveParent2 = Mapa[currentNode2.esquina]["Node"].parent
        if llaveParent2 == None:
            currentNode2 = None
        else:
            currentNode2 = Mapa[llaveParent2]["Node"]
    
    distance1 = distance1 + direccionLugar[0][1]
    distance2 = distance2 + direccionLugar[1][1]
    
    #Revisar el sentido de la calle y darle la distancia que le corresponda entonces
    #Primer caso; es una calle de doble sentido y tranquilamente comparamos entre las dos distancias cual es la menor
    #segundo caso; es una calle de un sentido y revisamos como va, y dependiendo de eso tomaremos tal distancia
    #tercer caso; no hay forma de llegar
    
    #EN ESTE DJIKSTRA LA MODIFICACION QUE HAREMOS ES EL QUE RETORNE UNA LISTA, PRIMERO LA DISTANCIA Y SEGUNDO UNA SUBLISTA DE LOS NODOS POR LOS QUE PASA.
    if esquina2Lugar in Mapa[esquinaLugar] and esquinaLugar in Mapa[esquina2Lugar]:
      if distance1 >= distance2:
        distancia = distancia + distance2
        listafinal = lista2
      else:
        distancia = distancia + distance1
        listafinal = lista1
      return [distancia, listafinal]
    
    if esquina2Lugar in Mapa[esquinaLugar]:
      distancia = distancia + distance1
      return [distancia, lista1]
    
    if esquinaLugar in Mapa[esquina2Lugar]:
      distancia = distancia + distance2
      return [distancia, lista2]
    
    return [math.inf, lista1, lista2]


def verificarElementos(persona, destino, mapa, diccionarioElementos):
  verPersona = str(persona)
  verDestino = str(destino)
  
  if verDestino[0] == "<":
      elementos = verDestino.split()

      # Convertir los elementos en tuplas
      direccionDestinoCorregida = [(elem.split(',')[0][1:], int(elem.split(',')[1][:-1])) for elem in elementos]
      if chequear_direccion(mapa, direccionDestinoCorregida) == True:
          shortPath = calculoCaminoMasCorto(direccionLugar, mapa, verPersona)
          return shortPath
      else:
          return "No existe tal direccion!"
      
  else:
      if verPersona in diccionarioElementos and verDestino in diccionarioElementos:
          #Ahora que sabemos que existen, tendran camino alguno?. Si calculamos con Djikstra, entonces si, lo hay.
          direccionLugar = diccionarioElementos[verDestino]
          direccionPersona = diccionarioElementos[verPersona]
          shortPath = calculoCaminoMasCorto(direccionLugar, mapa, direccionPersona[0])
          return shortPath
      else:
          return "No existe tal lugar!"
    

def calculoCaminoMasCorto(direccionLugar, mapa, direccionPersona):
    #CASO DONDE ESTEN EN LA MISMA CALLE DEBO VERIFICAR SENTIDO DE LA CALLE
    sentidoCalleP = verificacionDobleMano(mapa,direccionPersona[0][0],direccionPersona[1][0])
    if (direccionPersona[0][0] == direccionLugar[0][0] or direccionPersona[0][0] == direccionLugar[1][0]) and (direccionPersona[1][0] == direccionLugar[0][0] or direccionPersona[1][0] == direccionLugar[1][0]):
        if len(sentidoCalleP) == 2: 
            return []
        if len(sentidoCalleP) == 1:
            if sentidoCalleP[0] == direccionLugar[0][0]:
                distanciaEsquinaLugar = direccionLugar[0][1]
            else:
                distanciaEsquinaLugar = direccionLugar[1][1]
            
            if sentidoCalleP[0] == direccionPersona[0][0]:
                distanciaEsquinaPersona = direccionPersona[0][1]
            else:
                distanciaEsquinaPersona = direccionPersona[1][1]
            
            if distanciaEsquinaLugar <= distanciaEsquinaPersona:
                return []
    

    if len(sentidoCalleP) == 2:
  
        distanciaPersonaLugar1 = calculoDjikstraPE(direccionPersona, sentidoCalleP[0], mapa, direccionLugar[0][0], direccionLugar[1][0], direccionLugar)
        distanciaPersonaLugar2 = calculoDjikstraPE(direccionPersona, sentidoCalleP[1], mapa, direccionLugar[0][0], direccionLugar[1][0], direccionLugar)
        if distanciaPersonaLugar1[0] == math.inf and distanciaPersonaLugar2[0] == math.inf:
            return None 
        if distanciaPersonaLugar1[0] >= distanciaPersonaLugar2[0]:
            return distanciaPersonaLugar2[1]
        else:
            return distanciaPersonaLugar1[1]
    
    if len(sentidoCalleP) == 1:
        distanciaPersonaLugar = calculoDjikstraPE(direccionPersona, sentidoCalleP[0], mapa, direccionLugar[0][0], direccionLugar[1][0], direccionLugar)
        if distanciaPersonaLugar[0] == math.inf:
            return None
        return distanciaPersonaLugar[1]
    
    if len(sentidoCalleP) == 0:
        return None
        
  
    