import random
from threading import Thread, Lock 
import time 

particulas = 3
pasos = 4
numHilos = 4  
archivo = "Elementos.txt"

lock = Lock()

x = []
y = []
vx = []
vy = []

for i in range(particulas):
    x.append(random.uniform(0, 1000))  # Posición en X
    y.append(random.uniform(0, 1000))  # Posición en Y
    vx.append(random.uniform(0, 10))   # Velocidad en X
    vy.append(random.uniform(0, 10))   # Velocidad en Y


archivo_inicial = "datos_iniciales.txt"

with open(archivo_inicial, "w") as f_inicial:
    f_inicial.write("X Y VX VY\n") 
    for i in range(particulas):
        f_inicial.write(f"{x[i]} {y[i]} {vx[i]} {vy[i]}\n")


def mover_particulas(inicio, fin):

    linea_bloque = ""
    for i in range(inicio, fin):
        x[i] += vx[i]
        y[i] += vy[i]
        linea_bloque += f"{x[i]:.2f} {y[i]:.2f} | "

    with lock:
        with open(archivo, "a") as f:
            f.write(linea_bloque)
            
def simular():

    with open(archivo, "w") as f:  
        pass
 
    for paso in range(pasos):
        print(f"Iniciando paso {paso + 1}/{pasos}")

        hilos = []
        bloque_size = particulas // numHilos

        for i in range(numHilos):

            inicio = i * bloque_size  

            if i < numHilos - 1:
                fin = (i + 1) * bloque_size  
            else:
                fin = particulas 
            
            hilo = Thread(target=mover_particulas, args=(inicio, fin))
            hilos.append(hilo)
            hilo.start()

        for hilo in hilos:
            hilo.join()

        with open(archivo, "a") as f:
            f.write("\n")

if __name__ == "__main__":
    inicio_tiempo = time.time()
    simular()  
    fin_tiempo = time.time()
    duracion = fin_tiempo - inicio_tiempo
    print(f"Terminado en {duracion:.2f} segundos.")