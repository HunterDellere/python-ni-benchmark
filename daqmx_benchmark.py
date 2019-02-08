from daqmx_session import DAQmxSession
import time
import sys
import pandas as pd
import xlsxwriter
import os.path
import datetime


def benchmark(session, method, device, channel, samples, trials):
    results = []

    for trial in range(trials):
        t_start = time.perf_counter()
        method(device, channel, samples, trial)
        t_end = time.perf_counter()
        t_elapsed = t_end - t_start
        sys.stdout.write("Trial Progress: %d of %d   \r" % (trial, trials))
        sys.stdout.flush()
        time.sleep(.100)
        results.append([trial, t_elapsed])

    session.close()
    print(results)


'''
The following section of code configures and executes benchmarking
'''

print("Starting...")
# Configure Testing Parameters Here
samples = 1000
trials = 100
device = 'Dev1'
channel = 'ai1'

# Begin Benchmark Section
session = DAQmxSession()
benchmark(session, session.analog_input, device, channel, samples, trials)
