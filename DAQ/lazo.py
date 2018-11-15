import pytest
import numpy as np
import pylab as plt 
import nidaqmx
import random
from nidaqmx import system, constants

import collections
import re
import queue
import threading


import pytest
import time
from nidaqmx.constants import (
    Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)
#---------------------------------------------------------------------
#---------------------   Lazo de control   ---------------------------
#---------------------------------------------------------------------
from nidaqmx import system, constants
s = system.System()
#print(list(s.devices)) 


sample_rate=12000  #dividimos a la mitad la frecuencia de toma de datos. 24K para cada canal
samples_per_channel=1000 #maximo = 1000
numero_de_dispositivo = 5
frecuencia = '-'
señal = 'Funte-Voltaje'
que_medimos = 'test-analog-input'
line = 'Dev5/port0/line0' #salida del line0=pin1


#---------------------   Emision de pulso---------------------------

#Esta funcion configura el canal de emision
def conf_emitir(task, line):
    task.do_channels.add_do_chan(line, line_grouping=LineGrouping.CHAN_PER_LINE)

#Esta funcion emite
def emitir(task, duty=.5, num_de_ciclos=1000, delta_time_sleep=1):

    for _ in range(num_de_ciclos):

        task.write(True)
        #time.sleep(delta_time_sleep * duty)
        time.sleep(0.1)
        task.write(False)
        time.sleep(1)
        #time.sleep(delta_time_sleep * (1-duty))

    task.write(False)   

#Esta funcion emite  (ver despues)
def emitir_continuo(task): 
    delta_time_sleep = 1
    
    for _ in range(num_de_ciclos):

        task.write(True)
        time.sleep(delta_time_sleep * duty)
        task.write(False)
        time.sleep(delta_time_sleep * (1-duty))

    task.write(False)   


#Esta funcion se usa solo para emitir
def emision(num_de_ciclos=1000,delta_time_sleep=0.01):
        
    with nidaqmx.Task() as task:
        #definimos al pin "do_line" como un digital output
        conf_emitir(task, line)
        #task.write([True, False]*100)
        emitir(task, .5, num_de_ciclos, delta_time_sleep)

#--------------------- Medicion  -------------------------------------

#Esta funcion configura el canal de medicion
def conf_medir(task, sample_rate):
    task.ai_channels.add_ai_voltage_chan("Dev{}/ai0".format(numero_de_dispositivo), 
                                         terminal_config=constants.TerminalConfiguration.RSE, 
                                         units=constants.VoltageUnits.VOLTS)  #pusimos esta linea para setear el modo de medición
    task.timing.cfg_samp_clk_timing(sample_rate) #agregamos frecuencia de sample rate

#Esta funcion mide 
def medir(task, sample_per_channel):
    data = task.read(number_of_samples_per_channel=samples_per_channel)
    return data
    
#Esta funcion se usa solo para medir y graficar salida
def medicion():
    with nidaqmx.Task() as task:
        conf_medir(task, sample_rate)
        medir(task, sample_per_channel)
      
        plt.plot(np.arange(samples_per_channel)/sample_rate, data0,'s-', label = 'Canal 0')
        plt.xlabel('seg')
        plt.ylabel('V')
        plt.legend(loc='upper right')
        plt.show()
    
# Funcion que calcula el periodo de la senial medida    
def periodo(data, sample_rate):  
    i=1
    timeUP=[]
    periodo=[]
    while i<len(data):
        
        if data[i]>4.0 and data[i-1] < 2:
            timeUP.append(i/sample_rate)
        i+=1
    
    
    i=1
    periodo=0
    while i<len(timeUP):
        periodo=(timeUP[i]-timeUP[i-1])+periodo
        
        i+=1
    periodo=periodo/len(timeUP)
    
    return periodo
    
#--------- Emision y Medicion en simultaneo  ------------------

with nidaqmx.Task() as task:
    conf_emitir(task, line)

    q = queue.Queue()
    delta_time_sleep = 0.001
    def worker():
        while True:
            duty = q.get()
            while q.empty():
#                print("new duty cycle %s" % duty)
                task.write(True)
                time.sleep(delta_time_sleep * duty)
                task.write(False)
                time.sleep(delta_time_sleep * (1-duty))

    t = threading.Thread(target=worker)
    t.start()


    with nidaqmx.Task() as task2:
        conf_medir(task2, sample_rate)
        while True:
#            data = medir(task, samples_per_channel)
#            act = periodo(data, sample_rate)
#            print(act)
            q.put(0.5)
#            time.sleep(0)

emision()
####------->    Guardamos 
#
#NAMES  = np.array(['tiempo','canal0'])
#FLOATS = np.array([np.arange(samples_per_channel)/sample_rate, data0])
#DAT =  np.column_stack((NAMES, FLOATS)).T
#
##Nombre del archivo txt  
#np.savetxt('{}-Frec={}-Sample_rate={}-señal={}'.format(que_medimos,frecuencia,sample_rate,señal), DAT, delimiter="\t", fmt='%s')


