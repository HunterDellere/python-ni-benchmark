import nidaqmx


class DAQmxSession:

    def __init__(self):
        print("DAQmx Session Initialized")

    def configure(self, device, channel):
        self.physical_channel = str(device) + "/" + str(channel)
        print("DAQmx Session Configured for " + self.physical_channel)

    def open(self, method):
        self.task = nidaqmx.task.Task()
        # self.task.ai_channels.add_ai_voltage_chan(self.physical_channel)
        methods = {
            "ai": self.task.ai_channels.add_ai_voltage_chan(self.physical_channel)
        }
        methods[method]
        # Add DAQmx Start Task here so that first
        # iteration does not have to auto-start, skewing the results.

    def close(self):
        self.task.close()

    def analog_input(self, device, channel, samples, trial=0):
        if trial == 0:
            self.configure(device, channel)
            self.open("ai")
        else:
            self.data = self.task.read(samples)
