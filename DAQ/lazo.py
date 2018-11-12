import pytest
import numpy as np
import pylab as plt 
import nidaqmx
import random
from nidaqmx import system, constants

import collections
import re

import pytest
import time
from nidaqmx.constants import (
    Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)
#---------------------------------------------------------------------
#---------------------   Lazo de control   ---------------------------
#---------------------------------------------------------------------


sample_rate=12000  #dividimos a la mitad la frecuencia de toma de datos. 24K para cada canal
samples_per_channel=1000 #maximo = 1000
numero_de_dispositivo = 5
frecuencia = '-'
señal = 'Funte-Voltaje'
que_medimos = 'test-analog-input'


#---------------------------------------------------------------------
#---------------------   Emision de pulso - vemos la salida por el line0 = pin1 ---------------------------
do_line = 'Dev5/port0/line0'


def emision(num_de_ciclos=3,delta_time_sleep=1):
        
    with nidaqmx.Task() as task:
        #definimos al pin "do_line" como un digital output
        conf_emitir(task, do_line)
        emitir(task, num_de_ciclos, delta_time_sleep)


def conf_emitir(task, line):
    task.do_channels.add_do_chan(line, line_grouping=LineGrouping.CHAN_PER_LINE)


def emitir(task, duty=.5, num_de_ciclos=3, delta_time_sleep=1):

    for _ in range(num_de_ciclos):

        task.write(True)
        time.sleep(delta_time_sleep * duty)
        task.write(False)
        time.sleep(delta_time_sleep * (1-duty))

    task.write(False)   

#
####------->    Lectura    Canal 0

def medicion():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev{}/ai0".format(numero_de_dispositivo), 
                          terminal_config=constants.TerminalConfiguration.RSE, 
                          units=constants.VoltageUnits.VOLTS)  #pusimos esta linea para setear el modo de medición
        task.timing.cfg_samp_clk_timing(sample_rate) #agregamos frecuencia de sample rate
        time.sleep(0.5)
        data0 = task.read(number_of_samples_per_channel=samples_per_channel)
     
        
        plt.plot(np.arange(samples_per_channel)/sample_rate, data0,'s-', label = 'Canal 0')
        plt.xlabel('seg')
        plt.ylabel('V')
        plt.legend(loc='upper right')
        plt.show()
        per=periodo(data0)
        return per
    
def periodo(data0):  
    i=1
    timeUP=[]
    periodo=[]
    while i<len(data0):
        
        if data0[i]>4.0 and data0[i-1] < 2:
            timeUP.append(i/sample_rate)
        i+=1
    
    
    i=1
    periodo=0
    while i<len(timeUP):
        periodo=(timeUP[i]-timeUP[i-1])+periodo
        
        i+=1
    periodo=periodo/len(timeUP)
    
    return periodo
    
    

with nidaqmx.Task() as task:
    conf_medicion(task, )
    conf_emision(task)
    while True:
        emitir(3)
        
        per=medir()  
        print (per)

    


####------->    Guardamos 
#
#NAMES  = np.array(['tiempo','canal0'])
#FLOATS = np.array([np.arange(samples_per_channel)/sample_rate, data0])
#DAT =  np.column_stack((NAMES, FLOATS)).T
#
##Nombre del archivo txt  
#np.savetxt('{}-Frec={}-Sample_rate={}-señal={}'.format(que_medimos,frecuencia,sample_rate,señal), DAT, delimiter="\t", fmt='%s')


