import os

archivo = "ubicaciones.pkl"

with open(archivo,"r+") as file:
    file.truncate(0)

print("Se eliminó el archivo")