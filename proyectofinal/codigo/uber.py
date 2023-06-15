import  pickle
import sys
import re
import os
import math
from mapa import createMap
from ubicaciones import cargar_fija,cargar_movil,chequear_direccion
from trip import calculoCaminoMasCorto
from elementos import calculoDistanciaAutosPersonas

mi_Mapa = "miMapa.pkl" 
ubicaciones_pickle = "ubicaciones.pkl"
distancias_pickle = "distancias.pkl"
mi_Mapa_Grafo = "miMapaGrafo.pkl"

#-----------Serializaciones y Deserializar-----------
#Serializar Mapa
def serializacion_Esquinas_Ycalles(parametroRecibido):
    with open(parametroRecibido) as file:
        datoEsquinas = file.readline()
        datoAristasyPeso = file.readline()
        
    
    with open(mi_Mapa, "wb") as pickle_file:
        pickle.dump(datoEsquinas, pickle_file)

        pickle.dump(datoAristasyPeso, pickle_file)
    

    mapa_creado = createMap(mi_Mapa)
    return mapa_creado

#Serializar ubicaciones
def serializacion_ubicaciones_distancias(archivo,diccionario):
    with open(archivo,"wb") as file:
        pickle.dump(diccionario,file)


#Deserializar
def deserializacion(archivo):
    with open(archivo,"rb") as file:
        objeto = pickle.load(file)
    return objeto    

#----------Otras funciones-----------

#Función que pasa la dirección en string a estructura de datos
def string_to_structure(string):
    valores = re.findall(r'<(.*?)>', string)
    valores_divididos = [valor.split(",") for valor in valores]
    direccion = [tuple(int(valor) if valor.isdigit() else valor for valor in valor.split(',')) for valor in valores]
    return direccion

#El archivo esta vacío? v1
def emptyfile(archivo):
    dato = deserializacion(archivo)
    if dato == "":
        return True
    return False

#El archivo esta vacío v2?
def emptyfile2(archivo):
    if os.path.getsize(archivo) == 0:
        return True
    return False



#Función que verifica que los argumentos del createtrip sean validos
def verificar_argumentos(persona,direccion_elemento,map,diccionario):
    if direccion_elemento[0] == "<":
        direccion = string_to_structure(direccion_elemento)
        if (persona in diccionario) and chequear_direccion(map,direccion) == True:
            direccionpersona = diccionario[persona][0]
            #caso en que la persona este pidiendo viaje a la direccion donde esta (si, muy vago):
            if (direccionpersona[0] == direccion[0] or direccionpersona[0] == direccion[1]) and (direccionpersona[1] == direccion[0] or direccionpersona[1] == direccion[1]):
                return -1
            shortpath = calculoCaminoMasCorto(direccion,map,direccionpersona)
            if shortpath == None:
                return None
            return shortpath
        return 
    else:
        direccion_elemento = direccion_elemento.lower()
        if (persona in diccionario) and (direccion_elemento in diccionario):
            direccionpersona = diccionario[persona][0]
            direccionlugar = diccionario[direccion_elemento]
            
            if (direccionpersona[0] == direccionlugar[0] or direccionpersona[0] == direccionlugar[1]) and (direccionpersona[1] == direccionlugar[0] or direccionpersona[1] == direccionlugar[1]):
                return -1
            shortpath = calculoCaminoMasCorto(direccionlugar,map,direccionpersona)
            if shortpath == None:
                return None
            return shortpath
        return 


#Función que arma el ranking de los autos
def ranking(distancias,persona,ubicaciones):
    
    rankingdiccionariov1 = {}
    for auto in distancias:
        diccionario = distancias[auto]
        if persona in diccionario:
            if diccionario[persona] != math.inf:
                rankingdiccionariov1[auto] = diccionario[persona]
    #Ordenar el diccionario
    rankingdiccionariov1 = dict(sorted(rankingdiccionariov1.items(),key=lambda x:x[1]))
    if len(rankingdiccionariov1) == 0: return

    #calcular el coste final
    for auto in rankingdiccionariov1:
        costefinal = (rankingdiccionariov1[auto] + ubicaciones[auto][1])/4
        rankingdiccionariov1[auto] = costefinal

    i = 0
    ranking_final = {}
    for claves in rankingdiccionariov1:
        ranking_final[claves] = rankingdiccionariov1[claves]
        i += 1
        if i == 3:
            break
    return ranking_final 


def cuadrointeractivo(ubicaciones,distancias,persona,elemento_direccion,ranking,camino,mapa,ubicaciones_pickle,distancia_pickle):
    print("")
    print("----------Bienvenido ",persona,"----------")
    print("")
    #Imprimir los autos ordenados de menor a mayor en cuanto a la distancia
    print("Este es el ranking de los autos:")
    i = 1
    for clave in ranking:
        print(i,": ",clave,"y el coste del viaje: ",ranking[clave])
    
    #Imprimir el recorrido que hara cualquiera de los autos
    print("")
    print("Este es el camino que tomará el auto para dirigirse a la dirección:")
    print("(",end=" ")
    for i in range(0,len(camino)):
        if i == len(camino)-1:
            print(camino[i],end=" ")
        else:
            print(camino[i],end=" -> ")
    print(")")
    print("")

    entrada1 = input("Eliga el auto que desea que realize el viaje: ")
    while True:
        entrada1 = entrada1.lower()
        if entrada1 in ranking:
            auto = entrada1
            break
        else:
            entrada1 = input("Auto incorrecto, por favor intente de vuelta: ")
    print("")
    print("Se escogió el auto:",auto)
    #Verificar que el usuario acepte y realizar los cambios y serializarlos en los archivos pickle
    entrada2 = input("¿Acepta el viaje? Ingrese si/no: ")
    entrada2 = entrada2.lower()
    while entrada2 != "si" and entrada2 != "no":
        entrada2 = input("Respuesta incorrecta por favor intente de vuelta: ")
        entrada2 = entrada2.lower()
    
    if entrada2 == "no":
        print("Okey,continue viajando con nosotros !")
        return
    
    if elemento_direccion[0] == "<":
        direccion = string_to_structure(elemento_direccion)
    else:
        elemento_direccion = elemento_direccion.lower()
        direccion = ubicaciones[elemento_direccion]
    
    ubicaciones[persona][1] = ubicaciones[persona][1] - ranking[auto]
    ubicaciones[persona][0] = direccion
    ubicaciones[auto][0] = direccion
    distancias = calculoDistanciaAutosPersonas(ubicaciones,mapa,distancias)
    serializacion_ubicaciones_distancias(ubicaciones_pickle,ubicaciones)
    serializacion_ubicaciones_distancias(distancia_pickle,distancias)
    print("")
    print("Se encuentra en la dirección:",ubicaciones[persona][0])
    print("El auto se encuentra en la dirección:",ubicaciones[persona][0])
    print("Ha llegado a destino, gracias por viajar con nosotros")
    return



#----------Comandos-----------
if sys.argv[1] != "-create_map" and sys.argv[1] != "-load_fix_element" and sys.argv[1] != "-load_movil_element" and sys.argv[1] != "-create_trip":
    print("Error")


#Cargar mapa
if sys.argv[1] == "-create_map":
    try:
        if os.path.exists(sys.argv[2]) == False:
            #En caso de que el fichero (el .txt) no se encuentre.
            print("No fue posible cargar el mapa")
        else:
            map_resultado = serializacion_Esquinas_Ycalles(sys.argv[2])
            print("map created succesfully")
            print(" ")
            with open(mi_Mapa_Grafo, "wb") as pickle_f:
              pickle.dump(map_resultado, pickle_f)
    except IndexError:
        print("Parámetro no permitido")


#Cargar elemento fijo
if sys.argv[1] == "-load_fix_element":
    try:
        if emptyfile(mi_Mapa_Grafo) == True:
            print("No hay nada cargado en el mapa")
        else:
            with open(mi_Mapa_Grafo,"rb") as file:
                map = pickle.load(file)

            ubicaciones = {}
            direction = string_to_structure(sys.argv[3])
            if os.path.exists(ubicaciones_pickle) == False:
                with open(ubicaciones_pickle, "wb") as archivo:
                    print("")
            
            if emptyfile2(ubicaciones_pickle) == False:
                ubicaciones = deserializacion(ubicaciones_pickle)
            
            oldsize = len(ubicaciones)
            cargar_fija(sys.argv[2],direction,map,ubicaciones)
            if oldsize != len(ubicaciones):
                serializacion_ubicaciones_distancias(ubicaciones_pickle,ubicaciones)
                print("Ubicación insertada con exito")

    except IndexError:
        print("Parámetro no permitido")


#Cargar elemento movil
if sys.argv[1] == "-load_movil_element":
    try:
        if emptyfile(mi_Mapa_Grafo) == True:
            print("No hay nada cargado en el mapa")
        else:
            with open(mi_Mapa_Grafo,"rb") as file:
                map = pickle.load(file)

            ubicaciones = {}
            direction = string_to_structure(sys.argv[3])
            
            if os.path.exists(ubicaciones_pickle) == False:
                with open(ubicaciones_pickle, "wb") as archivo:
                    print("")
            
            if emptyfile2(ubicaciones_pickle) == False:
                ubicaciones = deserializacion(ubicaciones_pickle)
            
            dicAutos = {}
            if os.path.exists(distancias_pickle) == False:
                with open(distancias_pickle, "wb") as archivo:
                    print("")

            if emptyfile2(distancias_pickle) == False:
                dicAutos = deserializacion(distancias_pickle)

            monto = int(sys.argv[4])
            distancias = cargar_movil(sys.argv[2],direction,monto,map,ubicaciones,dicAutos)
            if distancias != None:
                serializacion_ubicaciones_distancias(ubicaciones_pickle,ubicaciones)
                serializacion_ubicaciones_distancias(distancias_pickle,distancias)
                print("Ubicación insertada con éxito")
    except IndexError:
        print("Parámetro no permitido")


#Crear viaje
if sys.argv[1] == "-create_trip":
    try:
        if emptyfile(mi_Mapa_Grafo) == True:
            print("No hay nada cargado en el mapa")
        else:
            map = deserializacion(mi_Mapa_Grafo)
            ubicaciones = deserializacion(ubicaciones_pickle)
            distancias = deserializacion(distancias_pickle)
            sys.argv[2] = sys.argv[2].lower()
            camino = verificar_argumentos(sys.argv[2],sys.argv[3],map,ubicaciones)
            #Si es igual a none no podemos ir de la persona a la dirección o los argumentos fueron mal ingresados
            if camino != None:
                if camino == -1:
                    print("¡ya estamos aqui!")
                else:
                    distanciasautos = deserializacion(distancias_pickle)
                    ranking = ranking(distanciasautos,sys.argv[2],ubicaciones)
                #Si es igual a none quiere decir que ningún auto se puede dirigir a la persona
                    if ranking != None:
                       cuadrointeractivo(ubicaciones,distancias,sys.argv[2],sys.argv[3],ranking,camino,map,ubicaciones_pickle,distancias_pickle)
                    else:
                       print("ERROR!")
            else:
                print("ERROR!")
    except IndexError:
        print("Parámetro no permitido")                 

