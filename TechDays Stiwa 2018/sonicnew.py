#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import pymongo
import time
import datetime
import random
import sys
import iothub_client
# pylint: disable=E0611

from pymongo import MongoClient
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance
MONGO_CONNECTION_STRING = "mongodb://iotdbtechdays:ph8XzIZOuyYwUPUPUMWbxi2HNMPBv3hWGg3fp7opatv5nWp5HhAIGXSPlbHtoxAfWNHfYQeJcEq8DaSjyrgSGA==@iotdbtechdays.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"



# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=EK9160IoTHub.azure-devices.net;DeviceId=Raspberry_UltraSonic;ModuleId=dockersonic;SharedAccessKey=GTmpu/lHGDSUzEKDxmZI93Cddzpk1GpP+H+tUPjALRU="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

def send_confirmation_callback(message, result, user_context):
    print (message)
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
    
def getSonar():     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level 
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance
    
def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BCM)       #numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT)   #
    GPIO.setup(echoPin, GPIO.IN)    #

def loop():
    GPIO.setup(11,GPIO.IN)
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client.sonictest
    posts = db.posts
    while(True):
        distance = getSonar()
        post = {"Distance": distance, "datetime" : time.strftime("%d.%m.%Y %H:%M:%S")}
        posts.insert_one(post)
        print ("The distance is : %.2f cm"%(distance))
        time.sleep(1)
        
if __name__ == '__main__':     #program start from here
    #setup()
    client = iothub_client_init()
    while True:
        time.sleep(1)
    
    #try:
    #    loop()
    #except KeyboardInterrupt:  #when 'Ctrl+C' is pressed, the program will exit
    #    GPIO.cleanup()         #release resource
