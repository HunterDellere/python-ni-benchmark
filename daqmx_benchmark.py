import time
import sys
from pandas import DataFrame as df

from daqmx_session import DAQmxSession

# Configure Testing Parameters Here
samples = 1000
trials = 100
device = 'Dev1'
channel = 'ai1'
clk_src = 'OnboardClock'
benchmark_method = 'analog_input'


# Main benchmark function
def benchmark(session, method, device, channel, samples, trials, clk_src):
    results = []

    for trial in range(trials):
        sys.stdout.write("Trial Progress: %d of %d   \r" % (trial+1, trials))
        sys.stdout.flush()  # Progress indicator
        t_start = time.perf_counter()
        method(device, channel, samples, trial, clk_src)  # Calls target method
        t_end = time.perf_counter()
        t_elapsed = t_end - t_start
        results.append(t_elapsed)

    session.close()

    # Follow code is for console display until print statement
    sys.stdout.write("\n\n")  # Formatting
    data = df(results, columns=['Time'])  # Full results
    stats = data.Time.describe().reindex()  # Statistics of runs
    print(stats.to_csv(header=False, sep='\t'))


'''

MAIN FUNCTION

The following section of code configures and executes benchmarking function
with the configured parameters

'''

print("Starting...")

# Begin Benchmark Section
session = DAQmxSession()
benchmark(session, eval('session.' + benchmark_method),
          device, channel, samples, trials, clk_src)
