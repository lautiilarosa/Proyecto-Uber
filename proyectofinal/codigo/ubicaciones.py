
from elementos import calculoDistanciaAutosPersonas

#Función que cheque si la dirección ingresada es válida
def chequear_direccion(mapa,direccion):
    direccion[0][0] = direccion[0][0].lower()
    direccion[1][0] = direccion[1][0].lower()
    if direccion[0][0] in mapa:
        x = mapa[direccion[0][0]]
        if direccion[1][0] in x:
            peso1 = x[direccion[1][0]]
            peso2 = direccion[0][1] + direccion[1][1]
            if peso1 == peso2: return True

        if direccion[1][0] in mapa:
            y = mapa[direccion[1][0]]
            if direccion[0][0] in y:
                peso1 = y[direccion[0][0]]
                peso2 = direccion[0][1] + direccion[1][1]
                if peso1 == peso2: return True
    return False                


#función que carga ubicaciones fijas
def cargar_fija(elemento,direccion,mapa,diccionario):
    elemento = elemento.lower()
    if elemento in diccionario:
        print("Ubicación ya existente")
        return
    
    if chequear_direccion(mapa,direccion) == True:
        diccionario[elemento] = direccion
        return diccionario
    print("Dirección no válida")
    return

#función que carga ubicaciones móviles
def cargar_movil(elemento,direccion,monto,mapa,diccionario):
    elemento = elemento.lower()
    if elemento in diccionario:
        print("Ubicación ya existente")
        return
    
    if chequear_direccion(mapa,direccion) == True:
        list = []
        list.append(direccion)
        list.append(monto)
        diccionario[elemento] = list
        
        distancias = calculoDistanciaAutosPersonas(diccionario,mapa)
        return distancias 
    else:
        print("Dirección no válida")
        return





