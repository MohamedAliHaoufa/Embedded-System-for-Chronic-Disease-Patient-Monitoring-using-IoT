"""!
@file Resample.py
@brief In this sub-program, we processed the ECG signal data and extracted the essential vital parameters.
@author 
     - Mr. Mohamed Ali Haoufa
     - Mr. Mohamed Nacer Namane
@date Jun 7, 2022
@copyright Copyright (c) 2022.  All rights reserved.
"""
import heartpy as hp

def process_signal(data,fs):
    """!
    @brief Process a signal using the heartpy library.

    This function processes a given signal using the heartpy library and extracts the heart rate-related parameters.

    @param data The input signal data.
    @param fs The sampling frequency of the input signal.

    @return bpm The calculated beats per minute.
    @return ibi The calculated interbeat intervals.
    @return rmssd The calculated root mean square of successive differences.
    """
    wd, m = hp.process(data,fs)
    bpm = m['bpm']
    ibi = m['ibi']
    rmssd = m['rmssd']
    return bpm ,ibi ,rmssd 

