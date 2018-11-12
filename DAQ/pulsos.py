#se crea digital, se emite analogico, se mide analogico y el DAQ lo digitaliza

import pytest
import numpy as np
import pylab as plt 
import nidaqmx
import random


from nidaqmx.types import CtrTime
from nidaqmx.constants import (
    Edge, TriggerType, AcquisitionType, Level, TaskMode)
from nidaqmx.stream_readers import CounterReader
from nidaqmx.stream_writers import CounterWriter
from nidaqmx.tests.fixtures import x_series_device
from nidaqmx.tests.helpers import generate_random_seed


#probamos un diagnostico para ver si reconoce la placa DAQ y que nombre le está dando
#------------         Diagnostico      ------------
#correr esto primero  y ver que nombre le pone al device!!
from nidaqmx import system, constants
s = system.System()
nombre = list(s.devices)
print(nombre)

dev = nombre[0]
print(dev.name[3])
print(x_series_device)

##poner esto en la consola para ver que le puedo pedir a dev
#dir(dev)


@pytest.mark.parametrize('seed', [generate_random_seed()])
# Reset the pseudorandom number generator with seed.
def test_one_sample_uint32(self, x_series_device, seed):
        # Reset the pseudorandom number generator with seed.
        random.seed(seed)

        number_of_pulses = 100#random.randint(100)
        frequency = random.uniform(1000, 10000)

        # Select random counters from the device.
        counters = random.sample(self._get_device_counters(x_series_device), 2)


        with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task:
            write_task.co_channels.add_co_pulse_chan_freq(
                counters[0], freq=frequency)
            write_task.timing.cfg_implicit_timing(
                samps_per_chan=number_of_pulses)

            read_task.ci_channels.add_ci_count_edges_chan(counters[1])
            read_task.ci_channels.all.ci_count_edges_term = (
                '/{0}InternalOutput'.format(counters[0]))

            reader = CounterReader(read_task.in_stream)

            data0 =read_task.start()
            data1 =write_task.start()

            write_task.wait_until_done(timeout=2)
            
            

            value_read = reader.read_one_sample_uint32()
            assert value_read == number_of_pulses
            print(value_read)
        plt.plot(data0)
        plt.show()
