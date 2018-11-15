import pytest
import numpy as np
import pylab as plt 
import nidaqmx
import random


import collections
import re

import numpy
import pytest
import random
import time
import nidaqmx.stream_writers as sw
import nidaqmx
from nidaqmx.constants import (
    Edge, TriggerType, AcquisitionType, LineGrouping, Level, TaskMode)
from nidaqmx.utils import flatten_channel_string
from nidaqmx.tests.fixtures import x_series_device
from nidaqmx.tests.helpers import generate_random_seed

#---------------------------------------------------------------------

do_line = 'Dev5/port0/line0'

with nidaqmx.Task() as task:
    task.do_channels.add_do_chan(
            do_line, line_grouping=LineGrouping.CHAN_PER_LINE)    #definimos al pin "do_line" como un digital output
    data = [False,True,False,True]*1000
    i=0
    read_data=[]
    while i<len(data):
        if data[i] == True:
            task.write(True)
            read_data.append(task.read())
            time.sleep(0.0025)
            
        else:
            task.write(False)            
            read_data.append(task.read())
            time.sleep(0.0075)
        i+=1
    task.write(False)   
'''
# Generate random values to test.
    values_to_test = [bool(random.getrandbits(1)) for _ in range(100)]

    values_read = []
    for value_to_test in values_to_test:
        task.write(value_to_test)
        time.sleep(1)
        values_read.append(task.read())

    assert values_read == values_to_test
    value_read = task.read(number_of_samples_per_channel=1)
    # Verify setting number_of_samples_per_channel (even to 1)
    # returns a list
    for i in value_read:
        print(value_read)
    assert isinstance(value_read, list)
    assert len(value_read) == 1
'''