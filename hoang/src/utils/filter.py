def bandpass_filter_butterworth_hr(data, fl=0.83, fh=2.33, fs=100):
    from scipy.signal import butter, lfilter
    filter_data = []
    min_bandwidth = fl * 2 / fs
    max_bandwidth = fh * 2 / fs

    if len(data) != 0:
        b, a = butter(N=3, Wn=[min_bandwidth, max_bandwidth], btype='bandpass', output='ba')
        filter_data = lfilter(b, a, data)
    return filter_data


def low_filter_butterworth_rr(data, fr=0.5, fs=100):
    from scipy.signal import butter, lfilter
    filter_data = []
    low_bandwidth = fr * 2 / fs
    if len(data) != 0:
        b, a = butter(N=3, Wn=low_bandwidth, btype='low', output='ba')
        filter_data = lfilter(b, a, data)
    return filter_data


def find_hr(data):
    filter_data = bandpass_filter_butterworth_hr(data)
    import pandas as pd
    from scipy.signal import find_peaks
    series_hr_data = pd.Series(filter_data)
    max_hr = series_hr_data.max()
    min_hr = series_hr_data.min()
    thress_hold = (max_hr - min_hr)/100
    print(max_hr, min_hr)
    return max_hr