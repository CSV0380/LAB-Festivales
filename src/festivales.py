from typing import NamedTuple
from datetime import datetime, time, date
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



#EJERCICIO 1


def parsea_bool(cadena):
    if cadena == 'sí':
        return True
    else:
        return False
    
def parsea_date(cadena):
    return datetime.strptime(cadena, "%Y-%m-%d").date()


def parsea_artista(cadena):
    res = []
    resf = []
    lista = cadena.split("-")
    for i in lista:
        res.append(i.split("_"))
    for j in res:
        nombre = str(j[0])
        hora_comienzo = datetime.strptime(j[1], "%H:%M").time()
        cache = int(j[2])
        resf.append(Artista(nombre, hora_comienzo, cache))
    return resf



def lee_festivales (archivo:str)->list[Festival]:
    res = []
    with open(archivo, encoding = 'utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for nombre, fecha_ini, fecha_fin, estado, precio, entradas_vendidas, artistas, top in lector:
            nombre = str(nombre)
            fecha_ini = parsea_date(fecha_ini)
            fecha_fin = parsea_date(fecha_fin)
            estado = str(estado)
            precio = float(precio)
            entradas_vendidas = int(entradas_vendidas)
            artistas = parsea_artista(artistas)
            top = parsea_bool(top)
            res.append(Festival(nombre, fecha_ini, fecha_fin, estado, precio, entradas_vendidas, artistas, top))
    return res


festivales = lee_festivales("data\\festivales.csv")
# print(lee_festivales("data\\festivales.csv")[0])



#EJERCICIO 2

def total_facturado(festivales:list[Festival], fecha_ini:date|None=None, fecha_fin:date|None=None)->float:
    res = 0.0
    for f in festivales:
        if ((fecha_ini is None or f.fecha_comienzo >= fecha_ini) or (fecha_fin is None or f.fecha_fin <= fecha_fin)):
            if f.estado == "CELEBRADO":
                ingresos_festival = f.precio * f.entradas_vendidas
                res += ingresos_festival
    return res

# print(total_facturado(festivales, None, None))



#EJERCICIO 3

def artista_top(festivales: list[Festival]) -> tuple[int, str]:
    res = dict()
    for f in festivales:
        if f.estado == "CELEBRADO":
            for artista in f.artistas:
                nombre = artista.nombre 
                if nombre not in res:
                    res[nombre] = 0
                res[nombre] += 1

    top = sorted(res.items(), key=lambda x: x[1], reverse=True)[0]
    return (top[1], top[0])

# print(artista_top(festivales))



#EJERCICIO 4

def mes_mayor_beneficio_medio(festivales: list[Festival]) -> str:
    datos_por_mes = {}

    for f in festivales:
        mes = f.fecha_comienzo.month
        ingresos = f.entradas_vendidas * f.precio
        for a in f.artistas:
            gastos = sum(a.cache)
        beneficio = ingresos - gastos

        if mes not in datos_por_mes:
            datos_por_mes[mes] = [0.0, 0]
        
        datos_por_mes[mes][0] += beneficio
        datos_por_mes[mes][1] += 1
    
    mejor_mes = -1
    mejor_media = float('-inf')

    for mes, datos in datos_por_mes.items():
        media = datos[0] / datos[1]
        if media > mejor_media:
            mejor_media = media
            mejor_mes = mes
    
    meses = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", 
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    return meses[mejor_mes]

print(mes_mayor_beneficio_medio(festivales))