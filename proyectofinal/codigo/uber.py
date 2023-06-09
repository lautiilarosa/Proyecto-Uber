import  pickle
import sys
import re
import os
from mapa import createMap
from ubicaciones import cargar_fija,cargar_movil

mi_Mapa = "miMapa.pkl" 
ubicaciones_pickle = "ubicaciones.pkl"

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
def serializacion_ubicaciones(archivo,diccionario):
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
    tuplas = re.findall(r'\((.*?),(.*?)\)',string)
    structure = [(elem1, int(elem2)) for elem1, elem2 in tuplas]
    return structure

def emptyfile(archivo):
    if os.path.getsize(archivo) == 0:
        return True
    return False


#----------Comandos-----------
if sys.argv[1] == "-create_map":
    try:
        map_resultado = serializacion_Esquinas_Ycalles(sys.argv[2])
        print("MAPA CREADO CORRECTAMENTE")
    except IndexError:
        print("Parámetro no permitido")


if sys.argv[1] == "-load_fix_element":
    try:
        if emptyfile(mi_Mapa) == False:
            with open(mi_Mapa,"rb") as file:
                map = pickle.load(file)

            direction = string_to_structure(sys.argv[3])
            if emptyfile(ubicaciones_pickle) == False:
                ubicaciones = deserializacion(ubicaciones_pickle)

            oldsize = len(ubicaciones)
            cargar_fija(sys.argv[2],direction,map,ubicaciones)
            if oldsize != len(ubicaciones):
                serializacion_ubicaciones(ubicaciones_pickle,ubicaciones)
                print("Ubicación Insertada con éxito")
        print("ERROR!!!")
    except IndexError:
        print("Parámetro no permitido")


if sys.argv[1] == "-load_movil_element":
    try:
        if emptyfile(mi_Mapa) == False:
            with open(mi_Mapa,"rb") as file:
                map = pickle.load(file)

            direction = string_to_structure(sys.argv[3])
            if emptyfile(ubicaciones_pickle) == False:
                ubicaciones = deserializacion(ubicaciones_pickle)

            oldsize = len(ubicaciones)
            cargar_movil(sys.argv[2],direction,sys.argv[4],map,ubicaciones)
            if oldsize != len(ubicaciones):
                serializacion_ubicaciones(ubicaciones_pickle,ubicaciones)
                print("Ubicación Insertada con éxito")
        print("ERROR!!!")
    except IndexError:
        print("Parámetro no permitido")


