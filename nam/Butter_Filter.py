from scipy.signal import butter
from scipy.signal import lfilter, find_peaks, find_peaks_cwt
import numpy as np
import scipy.signal as ss
from matplotlib import pyplot as plt
import pandas as pd

fs = 100
fL = 0.83
fH = 2.33
fr = 0.5


def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='bandpass', output='ba')
    y = lfilter(b, a, data)
    return y

def butter_lowpass_filter(data,fs, fr, order=5):
    nyq = 0.5 * fs
    f=fr/nyq
    c, d =butter(order,f,btype='lowpass')
    RR = lfilter(c, d, data)
    return RR

# get data
data = pd.read_excel('rate-100-NofS-100-60s.xlsx')
#data = pd.read_csv('data.csv')
print(data)
data = np.asarray(data)
t = data[:,0:1]
print(t)
# thời gian đo
ts = 60
#ts = 10
# Chuyen thoi gian sang truc x
for index in range(0, np.size(t)):
    t[index] = ts * (index + 1) / np.size(t)
print(t)
print(t)
# get voltage
voltage = data[:,-1]
print(voltage)
print(type(voltage))
print(np.shape(voltage))
################################### draw data #################################
plt.figure(1)
plt.title('Original Signal')
plt.xlabel('Times')
plt.ylabel('Voltage')
plt.plot(t, voltage)


# Loc tin hieu nhip tim
HR = butter_bandpass_filter(voltage, fL, fH, fs, order=3)
threshold_HR = (max(HR) - min(HR)) * 0.01  # muc nguong
peaks, _ = ss.find_peaks(HR, distance=2.5, height=threshold_HR, width=2.5)
print(threshold_HR)
HR = np.asarray(HR)
print(np.size(peaks))
# Loc tin hieu nhip tho
RR = butter_lowpass_filter(voltage,fs, fr, order=5)
threshold_RR = (max(RR) - min(RR)) * 0.01  # muc nguong
peaks2, _ = ss.find_peaks(RR, distance=2.5, height=threshold_RR, width=2.5)
########### ve đồ thi #############
# tín hiệu nhịp tim
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
