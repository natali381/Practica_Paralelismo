import time
from multiprocessing import Process, Manager

def buscar(lineas, x_buscado, y_buscado, modo="secuencial", resultados=None):
    paso = 0
    for linea in lineas:
        columnas = linea.strip().split("|")

        for particula_num, datos in enumerate(columnas):
            datos = datos.strip()

            if datos == "":
                continue

            partes = datos.split()

            if len(partes) != 2:
                continue

            x = float(partes[0])
            y = float(partes[1])

            if x == x_buscado and y == y_buscado:
                if modo == "paralelo":
                    resultados.append((paso, particula_num))
                else:
                    print(f"Posición encontrada en paso {paso}, partícula #{particula_num}")
                return
            
        paso += 1
    if modo != "paralelo":
        print("Posición no encontrada.")

def principal_busqueda(archivo, x_buscado, y_buscado, num_procesos):
  

    # ===== SECUENCIAL =====
    print("============== BUSQUEDA: SECUENCIAL ==============\n")
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    inicio_tiempo = time.time()
    buscar(lineas, x_buscado, y_buscado, modo="secuencial")

    fin_tiempo = time.time()
    duracion= round(fin_tiempo - inicio_tiempo,4)
    print(f"Tiempo secuencial: {duracion} segundos\n")

    # ===== PARALELO =====
    print("============== BUSQUEDA: PARALELO ===============\n")
    inicio_tiempo = time.time()
    total_lineas = len(lineas)
    tamano_bloque = total_lineas // num_procesos

    with Manager() as manager:
        resultados = manager.list()
        procesos = []

        for i in range(num_procesos):
            inicio = i * tamano_bloque
            if i < num_procesos - 1:
                fin = (i + 1) * tamano_bloque
            else:
                fin = total_lineas
 
            bloque = lineas[inicio:fin]

            p = Process(target=buscar, args=(bloque, x_buscado, y_buscado, "paralelo", resultados))
            procesos.append(p)
            p.start()

        for p in procesos:
            p.join()

        if resultados:
            paso, particula = resultados[0]
            print(f"Posición encontrada en paso {paso}, partícula #{particula}")
        else:
            print("Posición no encontrada.")

        fin_tiempo = time.time()
        duracion= round(fin_tiempo - inicio_tiempo,4)   
        print(f"Tiempo paralelo: {duracion} segundos\n")

from collections import Counter

def contar(lineas, modo="secuencial", resultados=None, indice=None):
    coordenadas = []

    for linea in lineas:
        columnas = linea.strip().split("|")

        for particula_num, datos in enumerate(columnas):
            datos = datos.strip()

            if datos == "":
                continue

            partes = datos.split()

            if len(partes) != 2:
                continue

            x = float(partes[0])
            y = float(partes[1])
            coordenadas.append((x, y))

    conteo = Counter(coordenadas)

    if modo == "paralelo":
        if resultados is not None:
            if indice is not None:
                resultados[indice] = conteo
    else:
        print("Las 10 coordenadas mas frecuentes:")
        for coord, veces in conteo.most_common(10):
            print(f"Coordenada {coord} → {veces} veces")

def principal_conteo(archivo, num_procesos):
  

    # ===== CONTEO SECUENCIAL =====
    print("=============== CONTEO : SECUENCIAL ===============\n")
    with open(archivo, 'r') as f:
        lineas = f.readlines()

    inicio_tiempo = time.time()
    contar(lineas, modo="secuencial")
    fin_tiempo = time.time()
    duracion= round(fin_tiempo - inicio_tiempo,4)
    print(f"Tiempo (secuencial): {duracion} segundos\n")

    # ===== CONTEO PARALELO =====
    print("=============== CONTEO : PARALELO ===============\n")
    total_lineas = len(lineas)
    bloque_tamano = total_lineas // num_procesos
    inicio_tiempo = time.time()

    with Manager() as manager:
        resultados = manager.dict()
        procesos = []

        for i in range(num_procesos):

            inicio = i * bloque_tamano
            if i < num_procesos - 1:
                fin = (i + 1) * bloque_tamano
            else:
                fin = total_lineas

            bloque = lineas[inicio:fin]
            p = Process(target=contar, args=(bloque, "paralelo", resultados, i))
            procesos.append(p)
            p.start()

        for p in procesos:
            p.join()

        conteo_total = Counter()
        for parcial in resultados.values():
            conteo_total += parcial

        print("Las 10 coordenadas mas frecuentes:")
        for coord, veces in conteo_total.most_common(10):
            print(f"Coordenada {coord} → {veces} veces")

        fin_tiempo = time.time()
        duracion= round(fin_tiempo - inicio_tiempo,4)
        print(f"Tiempo (paralelo): {duracion} segundos\n")


if __name__ == "__main__":

    archivo = "Elementos.txt"
    x_buscado = 632.27 
    y_buscado = 877.96
    num_procesos = 2
 
    principal_busqueda(archivo, x_buscado,y_buscado,num_procesos)
    principal_conteo(archivo,num_procesos)
