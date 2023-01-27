#======================================================================================================================
# Name           : Resample.py
# Authors        : 
#    - Mr. Mohamed Ali Haoufa
#    - Mr. Mohamed Nacer Namane
# Created on     : Jun 7, 2022
# Description    : In this sub-program, we processed the ECG signal data and extracted the essential vital parameters.
#======================================================================================================================

import heartpy as hp

def process_signal(data,fs):
    wd, m = hp.process(data,fs)
    bpm = m['bpm']
    ibi = m['ibi']
    rmssd = m['rmssd']
    return bpm ,ibi ,rmssd 

