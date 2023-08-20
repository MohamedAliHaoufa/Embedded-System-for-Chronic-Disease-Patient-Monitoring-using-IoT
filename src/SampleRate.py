"""!
@file SampleRate.py
@brief In this sub-program, we split the collected data into two types and used them to calculate the 
       frequency sampling of the ECG signal.
@author 
     - Mr. Mohamed Ali Haoufa
     - Mr. Mohamed Nacer Namane
@date Jun 7, 2022
@copyright Copyright (c) 2022.  All rights reserved.
"""
import pandas as pd 

def split_and_calcul_fs(filename):
   """!
   @brief Read data from a CSV file and calculate the sampling frequency.

   This function reads data from a CSV file, extracts the time and data columns, and calculates the sampling frequency (fs).

   @param filename The name of the CSV file containing the data.

   @return time The time values extracted from the CSV file.
   @return data The data values extracted from the CSV file.
   @return fs The calculated sampling frequency.
   """
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

