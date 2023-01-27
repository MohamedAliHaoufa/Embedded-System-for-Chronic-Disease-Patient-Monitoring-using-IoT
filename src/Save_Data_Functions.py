#======================================================================================================================
# Name           : Save_Data_Functions.py
# Authors        : 
#    - Mr. Mohamed Ali Haoufa
#    - Mr. Mohamed Nacer Namane
# Created on     : Jun 7, 2022
# Description    : This sub-program includes the functions needed to save and remove/delete data ( CSV, png ).
#======================================================================================================================

import os 
import csv
import time

def write_to_csv(data,filename):
    time0=time.time()
    print ( time0 )
    apend = [time0 , data]
# the a is for append, if w for write is used then it overwrites the file
    with open(filename,'a') as sensor_readings:
       sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"' , quoting=csv.QUOTE_MINIMAL)
       write_to_log = sensor_write.writerow(apend)
       return(write_to_log)

def remove_csv(filename):
    file =filename 
    if(os.path.exists(file) and os.path.isfile(file)):
      os.remove(file)
      return   print("file deleted")
    else:
      return   print("file not found")  

def delete_png(png_name): 
  import os
  os.remove(png_name) 
  return 