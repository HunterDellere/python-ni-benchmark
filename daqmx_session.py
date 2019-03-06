import nidaqmx
import numpy as np

random_data = np.random.uniform(-1, 1, 10000).tolist()


class DAQmxSession:

    def __init__(self):
        print("DAQmx Session Initialized")

    def configure(self, device, channel):
        self.physical_channel = str(device) + "/" + str(channel)
        print("DAQmx Session Configured for " + self.physical_channel)

    def open(self, method):
        # Random data used for generation tasks


        self.task = nidaqmx.task.Task()
        # Method lookup dictionary used to make the call dynamic
        self.methods = {
            "ai": "self.task.ai_channels.add_ai_voltage_chan(self.physical_channel)",
            "ao": "self.task.ao_channels.add_ao_voltage_chan(self.physical_channel)"
        }
        eval(self.methods[method])
        # Add DAQmx Start Task here so that first
        # iteration does not have to auto-start, skewing the results.

    def close(self):
        self.task.close()

    # Available methods for testing are below
    def analog_input(self, device, channel,
                     samples, trial=0, clk_src='', rate=10000):
        # On the first trial we do configure and open
        if trial == 0:
            self.configure(device, channel)
            self.open("ai")
            self.task.timing.cfg_samp_clk_timing(rate, clk_src)
            self.data = self.task.read(samples)
        else:
            self.data = self.task.read(samples)

    def analog_output(self, device, channel,
                      samples, trial=0, clk_src='', rate=10000):

        # On the first trial we do configure and open
        if trial == 0:
            self.configure(device, channel)
            self.open("ao")
            # self.task = nidaqmx.task.Task()
            # self.task.ao_channels.add_ao_voltage_chan(self.physical_channel)
            self.task.timing.cfg_samp_clk_timing(rate, clk_src)
            self.task.write(random_data, auto_start=True)
            self.task.stop()
        else:
            self.task.write(random_data, auto_start=True)
            self.task.stop()
