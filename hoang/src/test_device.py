import nidaqmx.task as task
from nidaqmx._task_modules.in_stream import InStream
from nidaqmx.constants import Edge, AcquisitionType
from nidaqmx.stream_readers import AnalogSingleChannelReader
import src.utils.butterworth_filter as btwf
import numpy as np
import src.utils.file_utils as file_utils
data_raw = np.zeros(shape=(6000,))

if __name__ == "__main__":

    configed_task = task.Task('Task read I signal')
    configed_task.ai_channels.add_ai_voltage_chan('Dev1/ai0')
    configed_task.timing.cfg_samp_clk_timing(rate=100,
                                             source=u'',
                                             active_edge=Edge.RISING,
                                             sample_mode=AcquisitionType.FINITE,
                                             samps_per_chan=6000)

    instream_analog_task = AnalogSingleChannelReader(InStream(configed_task))
    instream_analog_task.read_many_sample(data=data_raw, number_of_samples_per_channel=6000, timeout=100)
    file_path = 'E:\\python_project\\hoang\data\\data_test.csv'
    file_utils.write_to_csv_file(data_raw, file_path)

    import matplotlib.pyplot as plt
    import numpy as np
    peaks = btwf.find_hr(data_raw)
    peaks2 = btwf.find_rr(data_raw)
    HR = btwf.butter_bandpass_filter(data_raw)
    RR = btwf.butter_lowpass_filter(data_raw)
    t = np.arange(0, 60, 0.01)
    plt.figure(2)
    plt.title('HR signal')
    plt.xlabel('Times')
    plt.ylabel('Voltage')
    plt.plot(t, HR)
    plt.plot(t[peaks], HR[peaks], 'x')
    # tín hiệu nhịp thở
    plt.figure(3)
    plt.title('RR signal')
    plt.xlabel('Times')
    plt.ylabel('Voltage')
    plt.plot(t, RR)
    plt.plot(t[peaks2], RR[peaks2], 'x')
    plt.show()
