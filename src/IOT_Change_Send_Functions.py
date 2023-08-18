"""!
@file IOT_Change_Send_Functions.py
@brief In this sub-program, we developed certain functions to encrypt, change and send the collected data to the IoT platform.
@author 
     - Mr. Mohamed Ali Haoufa
     - Mr. Mohamed Nacer Namane
@date Jun 7, 2022
@copyright Copyright (c) 2022.  All rights reserved.
"""
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

# Variables Initialization :
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

INTERVAL= 1 # Data capture and upload interval in seconds. 


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
    """!
    @brief Encrypts the given data using AES encryption.

    This function encrypts the given data using the AES encryption algorithm and returns the encrypted result.

    @param data The data to be encrypted.
    @param key The encryption key.
    @param iv The initialization vector.

    @return The encrypted data.
    """
    data= pad(str(data).encode(),16)
    cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
    return base64.b64encode(cipher.encrypt(data))

def MAX_value (parameter,number):
    """!
    @brief Calculates the maximum value by adding a number to the parameter.

    @param parameter The base value.
    @param number The number to be added.

    @return The calculated maximum value.
    """ 
    val_max = parameter+number
    return val_max 

def MIN_value (parameter,number): 
    """!
    @brief Calculates the minimum value by subtracting a number from the parameter.

    @param parameter The base value.
    @param number The number to be subtracted.

    @return The calculated minimum value.
    """
    val_min = parameter-number
    return val_min 


def Temp_Sending_Condition (temp,temp_min,temp_max,temp_data ):
    """!
    @brief Checks if the temperature value is within the specified range before sending.

    This function checks whether the temperature value is within the specified range and sends the data to ThingsBoard if the condition is met.

    @param temp The temperature value to be checked.
    @param temp_min The minimum allowed temperature.
    @param temp_max The maximum allowed temperature.
    @param temp_data The data to be sent.

    @return True if the condition is met and data is sent, False otherwise.
    """
    if temp < temp_min or temp > temp_max :
        print("temp pass ")
        client.publish('v1/devices/me/telemetry', json.dumps(temp_data), 1)
        return True
    else:
        print("temp don't pass")
        return False
        
def BPM_Sending_Condition(BPM,BPM_min,BPM_max, BPM_data):
    """!
    @brief Checks if the BPM value is within the specified range before sending.

    This function checks whether the BPM value is within the specified range and sends the data to ThingsBoard if the condition is met.

    @param BPM The BPM value to be checked.
    @param BPM_min The minimum allowed BPM value.
    @param BPM_max The maximum allowed BPM value.
    @param BPM_data The data to be sent.

    @return True if the condition is met and data is sent, False otherwise.
    """
    if BPM < BPM_min or BPM > BPM_max :
        print("BPM pass")
        client.publish('v1/devices/me/telemetry', json.dumps(BPM_data), 1)
        return True
    else:
        print("BPM don't pass")
        return False

def IBI_Sending_Condition(IBI,IBI_min,IBI_max, IBI_data):
    """!
    @brief Checks if the IBI value is within the specified range before sending.

    This function checks whether the IBI value is within the specified range and sends the data to ThingsBoard if the condition is met.

    @param IBI The IBI value to be checked.
    @param IBI_min The minimum allowed IBI value.
    @param IBI_max The maximum allowed IBI value.
    @param IBI_data The data to be sent.

    @return True if the condition is met and data is sent, False otherwise.
    """ 
    if IBI < IBI_min or IBI > IBI_max:
        print("IBI pass")
        client.publish('v1/devices/me/telemetry', json.dumps(IBI_data), 1)
        return True
    else:
        print("IBI don't pass")
        return False

def RMSSD_Sending_Condition(RMSSD,RMSSD_min,RMSSD_max, RMSSD_data):
    """!
    @brief Checks if the RMSSD value is within the specified range before sending.

    This function checks whether the RMSSD value is within the specified range and sends the data to ThingsBoard if the condition is met.

    @param RMSSD The RMSSD value to be checked.
    @param RMSSD_min The minimum allowed RMSSD value.
    @param RMSSD_max The maximum allowed RMSSD value.
    @param RMSSD_data The data to be sent.

    @return True if the condition is met and data is sent, False otherwise.
    """
    if RMSSD < RMSSD_min or RMSSD > RMSSD_max:
        print("RMSSD pass")
        client.publish('v1/devices/me/telemetry', json.dumps(RMSSD_data), 1)
        return True
    else:
        print("RMSSD don't pass")
        return False

def cvt_2_base64(filename):
    """!
    @brief Converts an image file to a Base64-encoded string.

    This function reads an image file and converts its content to a Base64-encoded string.

    @param filename The name of the image file to be converted.

    @return A Base64-encoded string representation of the image.
    """
    with open(filename , "rb") as image_file :
        b64_bytes = base64.b64encode(image_file.read())
    return b64_bytes.decode()

def image_generator(data):
    """!
    @brief Generates and saves an image of the ECG signal.

    This function generates an image of the ECG signal using the provided data and saves it as a PNG file. It also converts the image to a Base64-encoded string.

    @param data The ECG signal data.
    @return A Base64-encoded string representation of the generated image.
    """
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
