#=========================================================================================================================================
# Name           : IOT_Change_Send_Functions.py
# Authors        : 
#    - Mr. Mohamed Ali Haoufa
#    - Mr. Mohamed Nacer Namane
# Created on     : Jun 7, 2022
# Description    : In this sub-program, we developed certain functions to encrypt, change and send the collected data to the IoT platform.
#=========================================================================================================================================

import os
from   pickle import FALSE
import time
import sys
import paho.mqtt.client as mqtt
import json
import numpy as np
import base64
import matplotlib.pyplot as plt
import cryptography
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

INTERVAL= 0

# Variables Initialization
temp_min = 0
temp_max = 0
BPM_min = 0
BPM_max = 0
IBI_min = 0
IBI_max = 0
RMSSD_min = 0
RMSSD_max = 0

THINGSBOARD_HOST = 'thingsboard.cloud'  
ACCESS_TOKEN = 'REPLACE_With_YOUR_ACCESS_TOKEN'    

# Data capture and upload interval in seconds. 
INTERVAL= 1

temp_data = {'temperature': 0}
BPM_data = {'BPM': 0}
IBI_data =  {'IBI' : 0}
RMSSD_data = {'RMSSD': 0}
image_data = {'image':0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

def encrypt(data,key,iv):
    data= pad(str(data).encode(),16)
    cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
    return base64.b64encode(cipher.encrypt(data))

def MAX_value (parameter,number): 
    val_max = parameter+number
    return val_max 
def MIN_value (parameter,number): 
    val_min = parameter-number
    return val_min 


def Temp_Sending_Condition (temp,temp_min,temp_max,temp_data ):
    if temp < temp_min or temp > temp_max :
        print("temp pass ")
        client.publish('v1/devices/me/telemetry', json.dumps(temp_data), 1)
        return True
    else:
        print("temp don't pass")
        return False
        
def BPM_Sending_Condition(BPM,BPM_min,BPM_max, BPM_data):
    if BPM < BPM_min or BPM > BPM_max :
        print("BPM pass")
        client.publish('v1/devices/me/telemetry', json.dumps(BPM_data), 1)
        return True
    else:
        print("BPM don't pass")
        return False

def IBI_Sending_Condition(IBI,IBI_min,IBI_max, IBI_data): 
    if IBI < IBI_min or IBI > IBI_max:
        print("IBI pass")
        client.publish('v1/devices/me/telemetry', json.dumps(IBI_data), 1)
        return True
    else:
        print("IBI don't pass")
        return False

def RMSSD_Sending_Condition(RMSSD,RMSSD_min,RMSSD_max, RMSSD_data):
    if RMSSD < RMSSD_min or RMSSD > RMSSD_max:
        print("RMSSD pass")
        client.publish('v1/devices/me/telemetry', json.dumps(RMSSD_data), 1)
        return True
    else:
        print("RMSSD don't pass")
        return False

def cvt_2_base64(filename):
    with open(filename , "rb") as image_file :
        b64_bytes = base64.b64encode(image_file.read())
    return b64_bytes.decode()

def image_generator(data):
        plt.plot(data, label = 'ECG signal', color='#1f77b4') 
        plt.xlim(600,1200) # To decide the interval that we want to send 
        #plt.ylim(-300,400)
        plt.xlabel('time (seconds)' ) # number of points 
        plt.grid(True) 
        #plt.axis('tight')  
        figure = plt.gcf()  # To Get the current figure
        figure.set_size_inches(8.54,4.03) # Set figure's size manually to your full screen (32x18)
        plt.savefig('ECG_signal.png', bbox_inches='tight') # bbox_inches removes extra white spaces
        # convert the image to the code Base64 :
        b64_string = cvt_2_base64 ('ECG_signal.png')
        return b64_string
