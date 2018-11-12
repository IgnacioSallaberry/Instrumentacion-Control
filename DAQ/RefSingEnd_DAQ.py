#se crea digital, se emite analogico, se mide analogico y el DAQ lo digitaliza

import numpy as np
import pylab as plt 
import nidaqmx

#probamos un diagnostico para ver si reconoce la placa DAQ y que nombre le está dando
#------------         Diagnostico      ------------
#correr esto primero  y ver que nombre le pone al device!!
from nidaqmx import system, constants
s = system.System()
a = system.Device.ai_simultaneous_sampling_supported
nombre = list(s.devices)
print(nombre)


#print(type('{}'.format(nombre)))
#--------------------------------------------------

sample_rate=24000  #dividimos a la mitad la frecuencia de toma de datos. 24K para cada canal
samples_per_channel=1000 #maximo = 1000
numero_de_dispositivo = 4
frecuencia = '-'
señal = 'Funte-Voltaje'
que_medimos = 'test-analog-imput'

#####------->    Canal 0 y Canal 1
#with nidaqmx.Task() as task:
#    ai0 = task.ai_channels.add_ai_voltage_chan("Dev{}/ai0".format(numero_de_dispositivo), 
#                      terminal_config=constants.TerminalConfiguration.RSE, 
#                      units=constants.VoltageUnits.VOLTS)  #pusimos esta linea para setear el modo de medición
#
#    ai1 = task.ai_channels.add_ai_voltage_chan("Dev{}/ai1".format(numero_de_dispositivo), 
#                      terminal_config=constants.TerminalConfiguration.RSE,
#                      units=constants.VoltageUnits.VOLTS)  #pusimos esta linea para setear el modo de medición
#    task.timing.cfg_samp_clk_timing(sample_rate) #agregamos frecuencia de sample rate 
#    data = task.read(number_of_samples_per_channel=samples_per_channel)
#
#    plt.plot(np.arange(samples_per_channel)/sample_rate,data[0],'s-', label = 'Canal 0')
#    plt.plot(np.arange(samples_per_channel)/sample_rate,data[1],'s-', label = 'Canal 1')
#   
#    plt.xlabel('seg')
#    plt.ylabel('V')
#    plt.show()
#    plt.legend(loc='upper right')
#    plt.show()


####------->    Canal 0
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev{}/ai0".format(numero_de_dispositivo), 
                      terminal_config=constants.TerminalConfiguration.RSE, 
                      units=constants.VoltageUnits.VOLTS)  #pusimos esta linea para setear el modo de medición
    task.timing.cfg_samp_clk_timing(sample_rate) #agregamos frecuencia de sample rate
    data0 = task.read(number_of_samples_per_channel=samples_per_channel)
    
    plt.plot(np.arange(samples_per_channel)/sample_rate, data0,'s-', label = 'Canal 0')
    plt.xlabel('seg')
    plt.ylabel('V')
    plt.legend(loc='upper right')
    plt.show()


####------->    Canal 1
#with nidaqmx.Task() as task:
#    task.ai_channels.add_ai_voltage_chan("Dev{}/ai1".format(numero_de_dispositivo), 
#                      terminal_config=constants.TerminalConfiguration.RSE,
#                      units=constants.VoltageUnits.VOLTS)  #pusimos esta linea para setear el modo de medición
#    task.timing.cfg_samp_clk_timing(sample_rate) #agregamos frecuencia de sample rate
#    data1 = task.read(number_of_samples_per_channel=samples_per_channel)
#
#    plt.plot(np.arange(samples_per_channel)/sample_rate, data1,'s-', label = 'Canal 1')
#    plt.xlabel('seg')
#    plt.ylabel('V')
#    plt.legend(loc='upper right')
#    plt.show()




####------>  GUARDA los datos de salida en un archivo de texto 
#paso_de_med=list(range(samples_per_channel))
#paso_temporal = []
#for i in range(samples_per_channel):
#    paso_temporal.append((1/sample_rate)*i)
    
#    
NAMES  = np.array(['tiempo','canal0'])
FLOATS = np.array([np.arange(samples_per_channel)/sample_rate, data0])
DAT =  np.column_stack((NAMES, FLOATS)).T

#Nombre del archivo txt  
#np.savetxt('{}-Frec={}-Sample_rate={}-señal={}'.format(que_medimos,frecuencia,sample_rate,señal), DAT, delimiter="\t", fmt='%s')




'''
#Nos muestra el voltaje que está midiendo el canal 1
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev{}/ai1".format(numero_de_dispositivo))
    print(task.read())



#medimos con los dos canales
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev{}/ai0".format(numero_de_dispositivo), 
                      terminal_config=constants.TerminalConfiguration.RSE)  #pusimos esta linea para setear el modo de medición
    task.timing.cfg_samp_clk_timing(48000) #agregamos frecuencia de sample rate, el maximo es 48000
    
    data0 = task.read(number_of_samples_per_channel=200)
    plt.plot(data0,'bs-', label = 'Canal 0')
    plt.legend(loc='upper right')
    plt.show()


with nidaqmx.Task() as task:
    
    task.ai_channels.add_ai_voltage_chan("Dev{}/ai1".format(numero_de_dispositivo), 
                      terminal_config=constants.TerminalConfiguration.RSE)  #pusimos esta linea para setear el modo de medición
    task.timing.cfg_samp_clk_timing(48000) #agregamos frecuencia de sample rate
    
    data1 = task.read(number_of_samples_per_channel=200)
    plt.plot(data1,'sr-', label = 'Canal 1')
    plt.legend(loc='upper right')
    plt.show()

'''


'''
#frecuencia
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_freq_voltage_chan("Dev{}/ai0".format(numero_de_dispositivo),
    units=constants.FrequencyUnits.HZ)

    freq= task.read(number_of_samples_per_channel=1000)
    plt.plot(freq,'sr-', label = 'freq')
    plt.legend(loc='upper right')
    plt.show()
'''
''' 
i=0
data=[]
while i<len(data0):
    data.append(data1[i]-data0[i])
    i+=1

plt.plot(data, label = 'data1-data0')
plt.legend(loc='upper right')
plt.show()

'''

