#====================================================================================================================================================
# Name           : main_ECG_Prog.py
# Authors        : 
#    - Mr. Mohamed Ali Haoufa
#    - Mr. Mohamed Nacer Namane
# Created on     : Jun 7, 2022
# Description    : It's the main program of our project, where we included all the sub-programs together to implement the following functionalities :
#                  - Read and collect the ECG Data from the Serial Port and save it in the CSV file.
#                  - Spliting and calculating the frequency sampling of the Collected data.
#                  - Filtering and processing the ECG data.
#                  - The Encryption of data and then sending it to the IoT platform.
#                  - Testing the data to see if there is a remarkable change.
#====================================================================================================================================================

import serial
import Save_Data_Functions as sv 
import Resample as pr
import SampleRate as sm
from   gpiozero import MCP3008
import ECG_Noise_Filter as fl 
import IOT_Change_Send_Functions as sn 
import paho.mqtt.client as mqtt
import json
import numpy as np
import base64
import string
import os
import time
import sys
### serial port config ####
arduino = serial.Serial(
    port="/dev/ttyUSB0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)
### Channel mcp 3008 selection ### 
lectura = MCP3008(channel=2) 
temp_data = {'temperature': 0}
BPM_data = {'BPM': 0}
IBI_data =  {'IBI' : 0}
RMSSD_data = {'RMSSD': 0}
image_data = {'image':0}

### Define some values ##
order = 5
fs_of_filer = 5000
temp_min = 0
temp_max = 0
BPM_min = 0
BPM_max = 0
IBI_min = 0
IBI_max = 0
RMSSD_min = 0
RMSSD_max = 0
imagename ='ECG_signal.png'
filename1 = 'data_csv_record.csv' ### Choose name of csv file 

# The two Encryption Keys : key/iv
key = '03GosECsvhxGtbo=' #16 char for AES128

#FIX IV
iv =  'gaqIlAht+3nZWw=='.encode('utf-8') #16 char for AES128

while 1 : 
    ## Start : 
    ### Save 3600 values equivalent to 30 s of data ### 
   for i in range (3600) :
      data=str(arduino.readline()).strip(",.babcdef'rxfn\ ")
      sv.write_to_csv(data,filename1) 
      print('Collecting data'+str(i) +'%')

   try : 
         ## Split and Calcul fs ###############

         time1 , data , fs = sm.split_and_calcul_fs(filename1)

         ##  Filter data    ########################

         filtred_data = fl.final_filter(data, fs_of_filer, order) 
         
         ###  Process the ecg  data   #################

         BPM ,IBI ,RMSSD   = pr.process_signal(filtred_data,fs)

         ### Read temperature :

         temp = (lectura.value * 3.3)*100 + 0.3 #calibtion

         ###  Rounding values  ### 
         temp = round(int (temp), 2)
         BPM = round(int(BPM), 2)
         IBI = round(int(IBI), 2)
         RMSSD = round(int(RMSSD), 2)

         print(u"Temperature: {:g}\u00b0C, BPM: {:g} beat/min, IBI: {:g}ms, RMSSD: {:g}ms".format(temp, BPM, IBI, RMSSD))
         
         # Convert IBI from ms to s :
         IBI = IBI /1000

         # The Encryption of data : 
         temp_encrypted= sn.encrypt(temp,key,iv)
         temp_encrypted = temp_encrypted.decode("utf-8", "ignore")

         BPM_encrypted = sn.encrypt(BPM,key,iv)
         BPM_encrypted = BPM_encrypted.decode("utf-8", "ignore")

         IBI_encrypted= sn.encrypt(IBI,key,iv)
         IBI_encrypted = IBI_encrypted.decode("utf-8", "ignore")

         RMSSD_encrypted= sn.encrypt(RMSSD,key,iv)
         RMSSD_encrypted = RMSSD_encrypted.decode("utf-8", "ignore")

         sn.temp_data['temperature'] = temp_encrypted
         sn.BPM_data['BPM'] = BPM_encrypted
         sn.IBI_data['IBI'] = IBI_encrypted
         sn.RMSSD_data['RMSSD'] = RMSSD_encrypted

         #### Test change of data and send it to ThingsBoard IOT platform ##### 

         temp_flag = sn.Temp_Sending_Condition(temp,temp_min,temp_max, sn.temp_data)
         bpm_flag = sn.BPM_Sending_Condition(BPM,BPM_min,BPM_max, sn.BPM_data)
         ibi_flag = sn.IBI_Sending_Condition(IBI,IBI_min,IBI_max, sn.IBI_data)
         rmssd_flag = sn.RMSSD_Sending_Condition(RMSSD,RMSSD_min,RMSSD_max, sn.RMSSD_data)
         
         #### Change the intervals of each parameter if it has a remarkable change ##### 

         if temp_flag :
               temp_max = sn.MAX_value (temp,2)
               temp_min = sn.MIN_value (temp,2)
               print(u"temp_min: {:g}\u00b0C, temp_max: {:g}\u00b0C".format(temp_min, temp_max))
               print("temp limits change")
         else: 
               print("temp limits doesn't change")

         if bpm_flag:
               BPM_max = sn.MAX_value (BPM,5)
               BPM_min = sn.MIN_value (BPM,5)
               print(u"BPMmin: {:g} beat/min, BPMmax: {:g} beat/min".format(BPM_min, BPM_max))
               print("BPM limits change")
         else: 
               print ("BPM limits doesn't change")

         if ibi_flag:
               IBI_max = sn.MAX_value (IBI,0.1) 
               IBI_min = sn.MIN_value (IBI,0.1) 
               print(u"IBImin: {:g}s, IBImax: {:g}s".format(IBI_min, IBI_max))
               print ("IBI limits change")
         else: 
               print("IBI limits doesn't change")

         if rmssd_flag: 
               RMSSD_max = sn.MAX_value (RMSSD,5)
               RMSSD_min = sn.MIN_value (RMSSD,5)
               print(u"RMSSDmin: {:g}ms, RMSSDmax: {:g}ms".format(RMSSD_min, RMSSD_max))
               print("RMSSD limits change")
         else: 
               print("RMSSD limits doesn't change")

         
         if (bpm_flag or ibi_flag or rmssd_flag):
               b64_string = sn.image_generator(filtred_data)
               image_data['image'] = b64_string
               # Sending image data to ThingsBoard IOT platform :
               sn.client.publish('v1/devices/me/telemetry', json.dumps(image_data), 1)
               print(b64_string)
               print("image pass")

         sv.remove_csv(filename1)
         #sv.delete_png(imagename)
         
         if (not (temp_flag) or not(bpm_flag) or not(ibi_flag) or not(rmssd_flag)):
            print("delay activate")
            time.sleep(5)
   except KeyboardInterrupt:
         pass
   
