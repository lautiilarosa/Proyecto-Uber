from elementos import Djikstra
import math
#Verificar que existe la persona, y que exista tambien el lugar al que quiere ir
#Datos a necesitar: Mapa y diccionario de elementos
#si solamente nos entrega elementos, GENIAL; entramos nada mas al diccionario de elementos
#fijarme si se trata de UBICACION o si es ya direccion
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
    "e1": 5,
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



def chequear_direccion(mapa,direccion):
    direccion[0][0] = direccion[0][0].lower()
    direccion[1][0] = direccion[1][0].lower()
    if direccion[0][0] in mapa:
        x = mapa[direccion[0][0]]
        if direccion[1][0] in x:
            peso1 = x[direccion[1][0]]
            peso2 = direccion[0][1] + direccion[1][1]
            if peso1 == peso2: 
                return True

        if direccion[1][0] in mapa:
            y = mapa[direccion[1][0]]
            if direccion[0][0] in y:
                peso1 = y[direccion[0][0]]
                peso2 = direccion[0][1] + direccion[1][1]
                if peso1 == peso2: 
                    return True
    return False     

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
    #La direccion del auto porque acordemonos que no es que exactamente este en una esquina, hay que sumarle unos km mas. 
    #La esquinaAuto seria la esquina a la que tiene que ir si o si para empezar el recorrido.
    #Acordemonos; la direccion del auto esta escrita como: [("e1",4),("e2",10)]
    distancia = 0
    if EsquinaPersona == direccionPersona[0][0]:
        distancia = direccionPersona[0][1]
    else:
        if EsquinaPersona == direccionPersona[1][0]:
            distancia = direccionPersona[1][1]
    #ahora SI POR FINNN LO QUE EL MUNDO ESPERABA, USAR DJIKSTRAAAAA
    Djikstra(Mapa, EsquinaPersona)
    #claramente deben de estar las esquinas de la persona, y si sus d son infinitos, ¿no existe forma de llegar?
    
    distance1 = Mapa[esquinaLugar]["Node"].d
    currentNode1 = Mapa[esquinaLugar]["Node"]
    lista1 = []
    while currentNode1 != None:
        lista1.insert(0, currentNode1.esquina)
        llaveParent = Mapa[currentNode1.esquina]["Node"].parent
        print(llaveParent)
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
    
    #Y si sumo antes la distancia de la persona a sus esquinas?:
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
    #nada mas para ver si en caso de que es infinito, las listas deberian estar vacias.
    return [math.inf, lista1, lista2]

def estoEsunaPrueba(persona, destinoDireccion1):
    print(persona)
    print(destinoDireccion1)
    
    stringDestino = str(destinoDireccion1)
    print(len(stringDestino))
    print(stringDestino)

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
      
      # [(e3, 10), (e2, 40)]
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
            return "¡Estan en la misma calle!, no hay recorrido por esquinas"
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
                return "¡Estan en la misma calle!, no hay recorrido por esquinas"
    
    #Ahora si se viene lo chido:
    if len(sentidoCalleP) == 2:
        #voy a usar el codigo que tengo en elementos.py y hacer un cambio en calculoDjikstra
        distanciaPersonaLugar1 = calculoDjikstraPE(direccionPersona, sentidoCalleP[0], mapa, direccionLugar[0][0], direccionLugar[1][0], direccionLugar)
        distanciaPersonaLugar2 = calculoDjikstraPE(direccionPersona, sentidoCalleP[1], mapa, direccionLugar[0][0], direccionLugar[1][0], direccionLugar)
        if distanciaPersonaLugar1[0] >= distanciaPersonaLugar2[0]:
            return distanciaPersonaLugar2[1]
        else:
            return distanciaPersonaLugar1[1]
    
    if len(sentidoCalleP) == 1:
        distanciaPersonaLugar = calculoDjikstraPE(direccionPersona, sentidoCalleP[0], mapa, direccionLugar[0][0], direccionLugar[1][0], direccionLugar)
        return distanciaPersonaLugar[1]
    
    if len(sentidoCalleP) == 0:
        return "No se puede realizar"
        
print(verificarElementos("P6", "H1", mapitaPrueba, diccionarioE))       
    