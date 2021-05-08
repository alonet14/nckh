from scipy.signal import butter
from scipy.signal import lfilter, find_peaks, find_peaks_cwt
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

fs = 100
fL = 0.83
fH = 2.33
fr = 0.5

def find_hr(data):
    filter_data = butter_bandpass_filter(data, fL, fH, fs)
    import pandas as pd
    from scipy.signal import find_peaks
    series_hr_data = pd.Series(filter_data)
    max_hr = series_hr_data.max()
    min_hr = series_hr_data.min()
    thress_hold = (max_hr - min_hr)/100
    print(max_hr, min_hr)
    return max_hr

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='bandpass', output='ba')
    y = lfilter(b, a, data)
    return y


# get data
data = pd.read_excel('rate-100-NofS-100-60s.xlsx')
# print(data)
data = np.asarray(data)
t = data[:, 0:1]
# thời gian đo
ts = 60
# Chuyen thoi gian sang truc x
for index in range(0, np.size(t)):
    t[index] = ts * (index + 1) / np.size(t)
# print(t)

# get voltage
voltage = data[:, -1]
print(voltage)
################################### draw data #################################
plt.figure(1)
plt.title('Original Signal')
plt.xlabel('Times')
plt.ylabel('Voltage')
plt.plot(t, voltage)

plt.figure(2)
HR = butter_bandpass_filter(voltage, fL, fH, fs)
threshold_HR = (max(HR) - min(HR)) * 0.01  # muc nguong
# print(HR)
peaks, _ = find_peaks(HR, threshold=threshold_HR, height=1.35, width=1.5)
print(peaks)
# pkh,_ = find_peaks(HR, height=1.35, width=1.5, threshold=threshold_HR);
plt.title('HR signal')
plt.xlabel('Times')
plt.ylabel('Voltage')
plt.plot(t, HR)
plt.plot(t[peaks], HR[peaks], 'x')
c = np.savetxt('a.txt', HR)

# [pkh, lch] = find_peaks(HR, t, threshold_HR)
# # peaks,tp = find_peaks(HR,t, threshold=threshold_HR)

plt.show()
