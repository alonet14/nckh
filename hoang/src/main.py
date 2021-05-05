import PIL
import pandas
import os
from config import config_path as cfp
import numpy as np
from utils import filter
# path_name_file = cfp.path_to_project + cfp.path_to_data + '/1samp-2-60s.xlsx'
path_name_file = '/home/nvh/python_project/nckh/hoang/data/backup_3.xlsx'
data = pandas.read_excel(path_name_file, index_col=0, usecols='B')

print(type(data))

filter_data = filter.bandpass_filter_butterworth_hr(data.index)
print(filter_data.size)

peak = filter.find_hr(data.index)

import matplotlib
# from matplotlib import pyplot as plt
#
# fig = plt.figure()
# ax1 = fig.add_subplot(211)
# ax1.set_ylabel = 'volts'
# ax1.set_title('heart_signal')
# xdata = np.arange(0, data.index.size, 1)
# ydata = filter_data
#
# ax1.plot(xdata, ydata, color='blue', lw=1)
#
# plt.show()

