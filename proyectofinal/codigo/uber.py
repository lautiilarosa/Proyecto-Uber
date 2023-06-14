import  pickle
import sys
import re
import os
from mapa import createMap
from ubicaciones import cargar_fija,cargar_movil

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



def emptyfile(archivo):
    dato = deserializacion(archivo)
    if dato == "":
        return True
    return False


def emptyfile2(archivo):
    if os.path.getsize(archivo) == 0:
        return True
    return False

#----------Comandos-----------
if sys.argv[1] != "-create_map" and sys.argv[1] != "-load_fix_element" and sys.argv[1] != "-load_movil_element" and sys.argv[1] != "-create_trip":
    
    print("Error")
    print("ASD")

if sys.argv[1] == "-create_map":
    try:
        map_resultado = serializacion_Esquinas_Ycalles(sys.argv[2])
        print("map created successfully")
        with open(mi_Mapa_Grafo, "wb") as pickle_f:
            pickle.dump(map_resultado, pickle_f)
            
    except IndexError:
        print("Parámetro no permitido")


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
            #print("###")

            #with open(ubicaciones_pickle, "wb") as archivo:
                #archivo.flush()
                #valueBytes = (os.path.getsize(ubicaciones_pickle))
                
                #print(valueBytes)
                #ubicaciones = pickle.load(pickle_f)
                #print(ubicaciones)
        
            if emptyfile2(ubicaciones_pickle) == False:
                print("entramos aca")
                ubicaciones = deserializacion(ubicaciones_pickle)
            #else:
                #if valueBytes != 0:
                    #print("En realidad aca")

                    #with open(ubicaciones_pickle, "rb") as pickle_file:
                      #ubicaciones = pickle.load(pickle_file)
                      #print("XD")

            oldsize = len(ubicaciones)
            print(oldsize)

            cargar_fija(sys.argv[2],direction,map,ubicaciones)
            print(ubicaciones)
            print(len(ubicaciones))

            if oldsize != len(ubicaciones):
                with open(ubicaciones_pickle, "wb") as archivopkl:
                    pickle.dump(ubicaciones, archivopkl)
                print("Ubicación insertada con exito")
    except:
        print("Parámetro no permitido")


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
                with open(ubicaciones_pickle,"wb") as archivo:
                    print("")


            if emptyfile2(ubicaciones_pickle) == False:
                ubicaciones = deserializacion(ubicaciones_pickle)

            
            dicAutos = {}

            if os.path.exists(distancias_pickle) == False:
                with open(distancias_pickle, "wb") as archive:
                    print("")
            
            if emptyfile2(distancias_pickle) == False:
                dicAutos = deserializacion(distancias_pickle)

            distancias = cargar_movil(sys.argv[2],direction,sys.argv[4],map,ubicaciones, dicAutos)
            print(ubicaciones)

            if distancias != None:
                serializacion_ubicaciones_distancias(ubicaciones_pickle,ubicaciones)
                serializacion_ubicaciones_distancias(distancias_pickle,distancias)
            
            with open(distancias_pickle,"rb") as archivopkl:
                dicDistance = pickle.load(archivopkl)
                
                print(dicDistance)
    except:
        print("Parámetro no permitido")

