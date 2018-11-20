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
print(list(s.devices)) 


sample_rate=12000  #dividimos a la mitad la frecuencia de toma de datos. 24K para cada canal
samples_per_channel=1000 #maximo = 1000
numero_de_dispositivo = 7
frecuencia = '-'
señal = 'Funte-Voltaje'
que_medimos = 'test-analog-input'
line = 'Dev7/port0/line0' #salida del line0=pin1

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
#    print(periodo)
    return periodo
    
#--------- Emision y Medicion en simultaneo  ------------------

with nidaqmx.Task() as rtask: 
    conf_medir(rtask, sample_rate)
    act = .5
    periodo_ref = 0.01
    while True:
        with nidaqmx.Task() as wtask:
            wtask.co_channels.add_co_pulse_chan_freq('Dev7/ctr0', freq=366, duty_cycle=act) #366 es el maximo valor de frecuencia
            wtask.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS) 
            #no emite nada por default
            #si no le ponemos CONTINUOUS no emite nada.
            wtask.start()
            time.sleep(5)
            data = medir(rtask, samples_per_channel)
            T = periodo(data, sample_rate)

            
            if T > periodo_ref:
                act = act + .1
            else:
                act = act - .1
            
            print(act)



####------->    Guardamos 
#
#NAMES  = np.array(['tiempo','canal0'])
#FLOATS = np.array([np.arange(samples_per_channel)/sample_rate, data0])
#DAT =  np.column_stack((NAMES, FLOATS)).T
#
##Nombre del archivo txt  
#np.savetxt('{}-Frec={}-Sample_rate={}-señal={}'.format(que_medimos,frecuencia,sample_rate,señal), DAT, delimiter="\t", fmt='%s')


