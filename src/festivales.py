from typing import NamedTuple
from datetime import date, datetime, time
import csv
 
Artista = NamedTuple("Artista",     
                        [("nombre", str), 
                        ("hora_comienzo", time), 
                        ("cache", int)])

Festival = NamedTuple("Festival", 
                        [("nombre", str),
                        ("fecha_comienzo", date),
                        ("fecha_fin", date),
                        ("estado", str),                      
                        ("precio", float),
                        ("entradas_vendidas", int),
                        ("artistas", list[Artista]),
                        ("top", bool)
                    ])


def parsea_artistas(cadena):
    res = []
    lista = cadena.split("-")
    for i in lista:
        datos = i.split("_")
        if len(datos) == 3:
            nombre = str(datos[0])
            hora_comienzo = datetime.strptime(datos[1], "%H:%M").time()
            cache = int(datos[2])
            res.append(Artista(nombre, hora_comienzo, cache))
    return res

def parsea_bool(cadena):
    if cadena == 'sí':
        res = True
    elif cadena == 'no':
        res = False
    return res

def parsea_date(cadena):
    return datetime.strptime(cadena, '%Y-%m-%d').date()


def lee_festivales (archivo:str)->list[Festival]:
    res = []
    with open(archivo, encoding = 'utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for nombre, fecha_comienzo, fecha_fin, estado, precio, entradas_vendidas, artistas, top in lector:
            nombre = str(nombre)
            fecha_comienzo = parsea_date(fecha_comienzo)
            fecha_fin = parsea_date(fecha_fin)
            estado = str(estado)
            precio = float(precio)
            entradas_vendidas = int(entradas_vendidas)
            artistas = parsea_artistas(artistas)
            top = parsea_bool(top)
            res.append(Festival(nombre, fecha_comienzo, fecha_fin, estado, precio, entradas_vendidas, artistas, top))
    return res

festivales = lee_festivales("data\\festivales.csv")
print(festivales[0])