import  pickle
import sys

from mapa import createMap




mi_Mapa = "miMapa.pkl" 
def serializacion_Esquinas_Ycalles(parametroRecibido):
    with open(parametroRecibido) as file:
        datoEsquinas = file.readline()
        datoAristasyPeso = file.readline()
        
    
    with open(mi_Mapa, "wb") as pickle_file:
        pickle.dump(datoEsquinas, pickle_file)

        pickle.dump(datoAristasyPeso, pickle_file)
    

    mapa_creado = createMap(mi_Mapa)
    return mapa_creado
        

if sys.argv[1] == "-create_map":
    try:
        map_resultado = serializacion_Esquinas_Ycalles(sys.argv[2])
        print("MAPA CREADO CORRECTAMENTE")
    except IndexError:
        print("Parametro no permitido")
       