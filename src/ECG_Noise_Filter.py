"""!
@file ECG_Noise_Filter.py
@brief In this sub-program, we have combined multiple filters to create our final filter.
@author 
     - Mr. Mohamed Ali Haoufa
     - Mr. Mohamed Nacer Namane
@date Jun 7, 2022
@copyright Copyright (c) 2022.  All rights reserved.
"""

from scipy import signal
from scipy.signal import butter, iirnotch, lfilter
import numpy as np

def butter_highpass(cutoff, fs, order=5):
    """!
    @brief Apply a Butterworth high-pass filter to a signal.

    This function applies a high-pass filter to a signal to attenuate frequencies
    lower than the specified cutoff frequency. The order of the filter determines
    the roll-off rate of the attenuation. The resulting filter coefficients (b, a)
    can be used to filter the signal using the `scipy.signal.lfilter` function.

    @param cutoff: The frequency below which lower frequencies will be attenuated, in Hertz.
    @param fs: The sampling frequency of the signal in Hertz.
    @param order: The order of the Butterworth filter (default is 5).
    @return: The filter coefficients (b, a) for the high-pass filter.
    """
    nyq = 0.5*fs
    normal_cutoff = cutoff/nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False, output='ba')
    return b, a

def butter_lowpass(cutoff, fs, order=5):
    """!
    @brief Apply a Butterworth low-pass filter to a signal.

    This function applies a low-pass filter to a signal to attenuate frequencies
    higher than the specified cutoff frequency. The order of the filter determines
    the roll-off rate of the attenuation. The resulting filter coefficients (b, a)
    can be used to filter the signal using the `scipy.signal.lfilter` function.

    @param cutoff: The frequency above which higher frequencies will be attenuated, in Hertz.
    @param fs: The sampling frequency of the signal in Hertz.
    @param order: The order of the Butterworth filter (default is 5).
    @return: The filter coefficients (b, a) for the low-pass filter.
    """
    nyq = 0.5*fs
    normal_cutoff = cutoff/nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False, output='ba')
    return b, a

def notch_filter(cutoff, q,fs):
    """!
    @brief Apply a notch filter to an ECG signal.

    This function applies a notch filter to an ECG signal to attenuate frequencies
    around the specified cutoff frequency. The quality factor (q) determines the width
    of the notch. The resulting filter coefficients (b, a) can be used to filter the signal
    using the `scipy.signal.lfilter` function.

    @param cutoff: The frequency to be attenuated in Hertz.
    @param q: The quality factor of the notch filter.
    @param fs: The sampling frequency of the ECG signal in Hertz.
    @return: The filter coefficients (b, a) for the notch filter.
    """
    nyq = 0.5*fs
    freq = cutoff/nyq
    b, a = iirnotch(freq, q)
    return b, a

def highpass(data, fs, order=5):
    """!
    @brief Apply a high-pass filter to input data.

    This function applies a high-pass filter to the input data using a Butterworth
    high-pass filter with the specified order. The resulting filtered signal is
    returned.

    @param data: The input signal data to be filtered.
    @param fs: The sampling frequency of the input signal, in Hertz.
    @param order: The order of the Butterworth high-pass filter (default is 5).
    @return: The filtered signal after applying the high-pass filter.
    """
    b,a = butter_highpass(cutoff_high, fs, order=order)
    x = lfilter(b,a,data)
    return x

def lowpass(data, fs, order=5):
    """!
    @brief Apply a low-pass filter to input data.

    This function applies a low-pass filter to the input data using a Butterworth
    low-pass filter with the specified order. The resulting filtered signal is
    returned.

    @param data: The input signal data to be filtered.
    @param fs: The sampling frequency of the input signal, in Hertz.
    @param order: The order of the Butterworth low-pass filter (default is 5).
    @return: The filtered signal after applying the low-pass filter.
    """
    b,a = butter_lowpass(cutoff_low, fs, order=order)
    y = lfilter(b,a,data)
    return y

def notch(data, powerline, q):
    """!
    @brief Apply a notch filter to remove powerline interference from input data.

    This function applies a notch filter to the input data in order to remove
    powerline interference at a specific frequency. The resulting filtered signal
    is returned.

    @param data: The input signal data to be filtered.
    @param powerline: The frequency of the powerline interference to be removed, in Hertz.
    @param q: The quality factor (Q) of the notch filter.
    @return: The filtered signal after applying the notch filter.
    """
    b,a = notch_filter(powerline,q)
    z = lfilter(b,a,data)
    return z

def final_filter(data, fs, order=5):
    """!
    @brief Apply a series of filters to the input data for noise reduction and signal enhancement.

    This function applies a series of filters in sequence to the input data in order to
    achieve noise reduction and enhance the signal. The process includes a high-pass filter,
    a low-pass filter, and a notch filter to remove unwanted frequency components.

    @param data: The input signal data to be filtered.
    @param fs: The sampling frequency of the input data, in Hertz.
    @param order: The order of the Butterworth filters used for high-pass and low-pass filtering.
    @return: The filtered and enhanced signal after applying the series of filters.
    """
    # Apply high-pass filter
    b, a = butter_highpass(cutoff_high, fs, order=order)
    x = lfilter(b, a, data)

    # Apply low-pass filter
    d, c = butter_lowpass(cutoff_low, fs, order = order)
    y = lfilter(d, c, x)

    # Apply notch filter
    f, e = notch_filter(powerline, 30,fs)
    z = lfilter(f, e, y)    
     
    return z

cutoff_high = 20
cutoff_low = 600
powerline = 60

