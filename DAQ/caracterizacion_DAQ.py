#se crea digital, se emite analogico, se mide analogico y el DAQ lo digitaliza

import pylab as plt 
import nidaqmx
#probamos un diagnostico para ver si reconoce la placa DAQ y que nombre le está dando
#------------         Diagnostico      ------------
#correr esto primero  y ver que nombre le pone al device!! ej:DevX 
from nidaqmx import system
s = system.System()
print(list(s.devices)) 

#ai0 y ai1 son los dos inputs analógicos del DAQ
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev7/ai1")
    print(task.read())

#lee voltaje del canal analógico que se especifica 
#ver cómo podemos hacer que el number_of_samples_per_channel sea ALL
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev7/ai0")
    data0 = task.read(number_of_samples_per_channel=1000)
    #print(data)
    plt.plot(data0, label = 'Canal 0')
    plt.legend(loc='upper right')
    #plt.show()


with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev7/ai1")
    data1 = task.read(number_of_samples_per_channel=1000)
    #print(data)
    plt.plot(data1, label = 'Canal 1')
    plt.legend(loc='upper right')
    #plt.show()


#al final no usamos esto por ahora, estamos emitiendo la señal con un generador de funciones
#--------------   Código para generar la señal   --------------
import sounddevice as sd 
import numpy as np 
import pylab as plt 
import time 

  

def generador_de_senhal(frecuencia, duracion, amplitud, funcion, fs=192000): 
    """ 
    Genera una seÃ±al de forma seniodal o de rampa, con una dada frecuencia y duracion. 
    """ 
    cantidad_de_periodos = duracion*frecuencia 
    puntos_por_periodo = int(fs/frecuencia) 
    puntos_totales = puntos_por_periodo*cantidad_de_periodos 
              
    tiempo = np.linspace(0, duracion, puntos_totales) 
    if funcion=='sin': 
          data = amplitud*np.sin(2*np.pi*frecuencia*tiempo) 
    elif funcion=='rampa':
        data = amplitud*signal.sawtooth(2*np.pi*frecuencia*tiempo) 
    else:
        print("Input no vÃ¡lido. Introducir sin o rampa")
        data = 0 
    return tiempo, data 


def play_tone(frecuencia, duracion, amplitud=1, fs=192000, wait=True): 
    """ 
    Esta funciÃ³n tiene como output un tono de una cierta duraciÃ³n y frecuencia. 
    """ 
    sd.default.samplerate = fs #frecuencia de muestreo 
       
    tiempo, data = generador_de_senhal(frecuencia, duracion, amplitud, 'sin')    
    sd.play(data) 
       
    if wait: 
        time.sleep(duracion) 
    
    return tiempo , data 



def playrec_tone(frecuencia, duracion, amplitud=0.1, fs=192000): 
      """ 
      Emite un tono y lo graba. 
      """ 
      sd.default.samplerate = fs #frecuencia de muestreo 
      sd.default.channels = 2,2 #por las dos salidas de audio 
       
      tiempo, data = generador_de_senhal(frecuencia, duracion, amplitud, 'sin')       
      
      with nidaqmx.Task() as task:
          task.ai_channels.add_ai_voltage_chan("Dev7/ai1")
          daq = (task.read())
      
      grabacion = sd.playrec(daq, blocking=True) 
       
      return tiempo, data, grabacion 



    
    
    
