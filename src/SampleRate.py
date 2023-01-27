#======================================================================================================================
# Name           : SampleRate.py
# Authors        : 
#    - Mr. Mohamed Ali Haoufa
#    - Mr. Mohamed Nacer Namane
# Created on     : Jun 7, 2022
# Description    : In this sub-program, we split the collected data into two types and used them to calculate the 
#                  frequency sampling of the ECG signal.
#======================================================================================================================

import pandas as pd 

def split_and_calcul_fs(filename):
   header_list = ["datetime", "data"]
   df = pd.read_csv(filename, names=header_list)
   time=df["datetime"] 
   data=df["data"]
   timedalta = float(time.max()) - float (time.min())
   datadalta = data.index.stop 
   fs = float (datadalta)  / timedalta  
   print("Total time : "+str(timedalta))
   print("Number of data : "+str(datadalta))
   print("fs is "+str(fs))
   return time , data , fs 

