from scipy.signal import butter
from scipy.signal import lfilter, find_peaks, find_peaks_cwt
import numpy as np
import scipy.signal as ss
from matplotlib import pyplot as plt
import pandas as pd


def butter_bandpass_filter(data, lowcut=0.83, highcut=2.33, fs=100, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='bandpass', output='ba')
    y = lfilter(b, a, data)
    return y


def butter_lowpass_filter(data, fs=100, fr=0.5, order=5):
    nyq = 0.5 * fs
    f = fr / nyq
    c, d = butter(order, f, btype='lowpass')
    RR = lfilter(c, d, data)
    return RR

# Loc tin hieu nhip tim
def find_hr(data, lowcut=0.83, highcut=2.33, fs=100, order=3, distance=2.5, width=2.5):
    hr = butter_bandpass_filter(data, lowcut=lowcut, highcut=highcut, fs=fs, order=order)
    threshold_hr = (max(hr) - min(hr)) * 0.01  # muc nguong
    peaks, _ = ss.find_peaks(hr, distance=distance, height=threshold_hr, width=width)

    return peaks



# Loc tin hieu nhip tho
def find_rr(data, fs=100, fr=0.5, distance=2.5, width=2.5):
    rr = butter_lowpass_filter(data, fs=fs, fr=fr, order=5)
    threshold_rr = (max(rr) - min(rr)) * 0.01  # muc nguong
    peaks, _ = ss.find_peaks(rr, distance=distance, height=threshold_rr, width=width)
    return peaks

# # get data
# data = pd.read_excel('E:\\python_project\\hoang\\data\\backup_3.xlsx')
# data = np.asarray(data)
# t = data[:, 0:1]
# # thời gian đo
# ts = 60
# # ts = 10
# # Chuyen thoi gian sang truc x
# for index in range(0, np.size(t)):
#     t[index] = ts * (index + 1) / np.size(t)
# # get voltage
# voltage = data[:, -1]
#
# ################################### draw data #################################
# plt.figure(1)
# plt.title('Original Signal')
# plt.xlabel('Times')
# plt.ylabel('Voltage')
# plt.plot(t, voltage)

#
# fs = 100
# fL = 0.83
# fH = 2.33
# fr = 0.5





########### ve đồ thi #############

# # tín hiệu nhịp tim
# plt.figure(2)
# plt.title('HR signal')
# plt.xlabel('Times')
# plt.ylabel('Voltage')
# plt.plot(t, HR)
# plt.plot(t[peaks], HR[peaks], 'x')
#
# # tín hiệu nhịp thở
# plt.figure(3)
# plt.title('RR signal')
# plt.xlabel('Times')
# plt.ylabel('Voltage')
# plt.plot(t, RR)
# plt.plot(t[peaks2], RR[peaks2], 'x')
#
# plt.show()
