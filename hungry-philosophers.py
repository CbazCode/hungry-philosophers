""" #Integrantes
    #   Asis Romero, Sebastian
    #   Leon Ortiz, Diego
    #   Okamoto Rojas, Kioshi
"""
import time
import random
import threading

N = int(input('Ingrese cantidad de filosofos: '))
TIEMPO_TOTAL = int(input('Ingrese la cantidad de veces que comen: '))

class filosofo(threading.Thread):
    semaforo = threading.Lock() #SEMAFORO BINARIO ASEGURA LA EXCLUSION MUTUA
    estado = [] #ESTADO DE CADA FILOSOFO
    tenedores = [] #ARRAY DE SEMAFOROS PARA SINCRONIZAR ENTRE FILOSOFOS, MUESTRA QUIEN ESTA EN COLA DEL TENEDOR
    count=0

    def __init__(self):
        super().__init__()      #HERENCIA DE THREADING
        
        self.id=filosofo.count #ASIGNA ID AL FILOSOFO

        filosofo.count+=1 #INCREMENTA CANTIDAD DE FILOSOFOS
        filosofo.estado.append('PENSANDO') #INICIALIZA ESTADO DE FILOSOFO
        filosofo.tenedores.append(threading.Semaphore(0)) #AGREGA EL SEMAFORO DE SU TENEDOR (TENEDOR A LA IZQUIERDA)
        print("FILOSOFO {0} - PENSANDO".format(int(self.id+1)))

    def __del__(self):
        print("FILOSOFO {0} - Se para de la mesa".format(int(self.id+1)))  # CUANDO TERMINA EL THREAD

    def pensar(self):
        time.sleep(random.randint(0,5)) # CADA FILOSOFO SE TOMA DISTINTO TIEMPO PARA PENSAR, ALEATORIO

    def derecha(self,i):
        return (i-1)%N #BUSCAMOS EL INDICE DE LA DERECHA

    def izquierda(self,i):
        return(i+1)%N #BUSCAMOS EL INDICE DE LA IZQUIERDA

    def verificar(self,i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i]='COMIENDO'
            filosofo.tenedores[i].release()  #SI SUS VECINOS NO ESTAN COMIENDO AUMENTA EL SEMAFORO DEL TENEDOR Y CAMBIA SU ESTADO A COMIENDO

    def tomar(self):
        filosofo.semaforo.acquire() #SEÑALA QUE TOMARA LOS TENEDORES (EXCLUSION MUTUA)
        filosofo.estado[self.id] = 'HAMBRIENTO'
        self.verificar(self.id) #VERIFICA SUS VECINOS, SI NO PUEDE COMER NO SE BLOQUEARA EN EL SIGUIENTE ACQUIRE
        filosofo.semaforo.release() #SEÑALA QUE YA DEJO DE INTENTAR TOMAR LOS TENEDORES (CAMBIAR EL ARRAY ESTADO)
        filosofo.tenedores[self.id].acquire() #DISMINUYE EL ARREGLO TENEDORES A 0, LO CUAL INDICA QUE TENEDOR ESTA DESOCUPADO

    def cambiar(self):
        filosofo.semaforo.acquire() #SEÑALA QUE CAMBIARA DE ESTADO
        filosofo.estado[self.id] = 'PENSANDO'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release() #YA TERMINO DE COMER

    def comer(self):
        print("FILOSOFO {} COMIENDO".format(int(self.id+1)))
        
        time.sleep(2) #TIEMPO ARBITRARIO PARA COMER
        print("FILOSOFO {} TERMINO DE COMER".format(int(self.id+1)))

    def run(self):
        for i in range(TIEMPO_TOTAL):
            self.pensar() #EL FILOSOFO PIENSA
            self.tomar() #AGARRA LOS TENEDORES CORRESPONDIENTES
            self.comer() #COME
            self.cambiar() #CAMBIA DE ESTADO 

def main():
    lista=[]
    for i in range(N):
        lista.append(filosofo()) #AGREGA UN FILOSOFO A LA LISTA

    for f in lista:
        f.start() #METODO DE LIBRERIA THREADING LLAMA A RUN POR DEFECTO
                  #METODO RUN SE SOBREESCRIBE -- OVERWRITE

    for f in lista:
        f.join()  #ASEGURA QUE HILOS SE TERMINEN CORRECTAMENTE


main()
