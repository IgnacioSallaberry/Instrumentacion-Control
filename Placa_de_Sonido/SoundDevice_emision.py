import sounddevice as sd
import numpy as np
import pylab as plt
import time
from scipy.signal import find_peaks
from scipy import signal

def seno(frecuencia, duracion, amplitud=1, fs=192000):
    """
    Esta función tiene como output una funcion seno de una cierta duración y frecuencia.
    """
    tiempo=np.arange(fs*duracion)/fs
    seno=amplitud*np.sin(2*np.pi*frecuencia*tiempo).astype(np.float32)
    
    plt.plot(tiempo,seno)
    plt.title('señal original')
    plt.xlabel('Tiempo(s)')
    plt.ylabel('Amplitud')
    
    plt.show()
    
    return seno



def max_sin(frecuencia, duracion, amplitud=1, fs=192000):
    """
    Esta función tiene como output los primeros 10 máximos de la función de entrada
    """
    #array de la función de entrada
    sin=[]       
    sin=seno(frecuencia, duracion, fs=192000)
    #array del tiempo
    tiempo=np.arange(fs*duracion)/fs
    
    
    maximos=[]   #array de los maximos de la señal
    ubic_max=[]  #array de la ubicación de los maximos
    
    j=0    # j es un contador de maximos
    i=1    # i recorre todo el array del seno

    #busco los primeros 10 maximos----> j<10
    while i<len(sin)-1 and j<10:
        
        if sin[i-1] < sin[i] and sin[i] > sin[i+1]:
            maximos.append(sin[i])        #guardo los maximos de la señal 
            ubic_max.append(tiempo[i])    #guardo la ubicación de los maximos de la señal
            j+=1
        
        i+=1
        
    axes=plt.gca()
    #axes.set_xlim([0.0249,0.0252])
    #axes.set_ylim([0.9999,1.0002])
    #grafico señal y maximos       
    plt.plot(tiempo[:i+1],sin[:i+1],'*')
    plt.title('primeros 10 picos')
    plt.xlabel('Tiempo(s)')
    plt.ylabel('Amplitud')
    plt.plot(ubic_max[:],maximos[:], 'rs')
    plt.show()    
    
    return j,maximos  # pido ver cuantos maximos tengo y sus valores

#%%

def grabacion(duracion, fs=192000):
    """
    Graba la entrada de microfono por el tiempo especificado
    """
    sd.default.samplerate = fs #frecuencia de muestreo
    sd.default.channels = 1#1 porque la entrada es una sola
    
    grab = sd.rec(frames = fs*duracion, blocking = True)
    tiempo=np.arange(fs*duracion)/fs
    
    
    #sd.default.channels = 1 #por las dos salidas de audio
    #grab = sd.playrec(seno, blocking=True)
    
    #grafico señal y maximos       
    plt.plot(tiempo,grab,'*')
    plt.title('Grabacion')
    plt.xlabel('Tiempo(s)')
    plt.ylabel('Amplitud')
    plt.show()    
    
    return grab
    

def max_grabacion(duracion, amplitud=1, fs=192000):
    '''
    Calcula los maximos de la grabacion del microfono
    '''
    
    grab=grabacion(duracion, fs=192000)
    
    #array del tiempo
    tiempo=np.arange(fs*duracion)/fs
    
    maximos=[]   #array de los maximos de la señal
    ubic_max=[]  #array de la ubicación de los maximos
    
    i=1    # i recorre todo el array del seno

    #busco los primeros 10 maximos----> j<10
    while i<len(grab)-1:
        
        if grab[i-1] < grab[i] and grab[i] > grab[i+1]:
            maximos.append(grab[i])        #guardo los maximos de la señal 
            ubic_max.append(tiempo[i])    #guardo la ubicación de los maximos de la señal
            
        
        i+=1
    
    #axes=plt.gca()
    #axes.set_xlim([0.249,0.52])
    #axes.set_ylim([0.999,1.02])
    
    
    #grafico señal y maximos       
    plt.plot(tiempo,grab,'*')
    plt.title('Grabacion y maximos')
    plt.xlabel('Tiempo(s)')
    plt.ylabel('Amplitud')
    plt.plot(ubic_max[:],maximos[:], 'rs')
    plt.show()    
    
    

#%%  
def frecuencias(frec=0,fmax=30000):
    
    fmin=frec
    frecuencia=[1]
    
    while frecuencia[-1] < fmax:
        frec+=0.2
        frecuencia.append(np.exp(frec))
        
    
    print(plt.plot(frecuencia))


    