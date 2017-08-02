#!/usr/bin/env python
#Basic imports

"""
No licence yet

"""
__author__ = 'Enrique Garcia'
__version__ = '0.1'
__date__ = 'Jun 22 201'

#Basic imports
from ctypes import *
import sys
import random
import time
import numpy as np
from matplotlib.pyplot import plot, show, draw
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetLogLevel

#Create interface object
try:
    interfaceKit = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

#Event Handler Callback Functions
def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))

def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))

def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def interfaceKitSensorChanged(e):
    source = e.device
    print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))

def interfaceKitInputChanged(e):
    global timestamp, toogle, past_bool
    current_bool =  e.state
    #print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))
    #print("InterfaceKit: Sensor %i: %i" % (e.index, current_bool))
    if (current_bool  and not past_bool ):
        if (toogle):
            ts = time.time()
            toogle = False
            frequency(ts - timestamp)
            timestamp = ts
        else:
            timestamp = time.time()
            toogle = True
    past_bool = current_bool

    
def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))

def differential(data_array):
	print("Last 2 Values (latest last): %i, %i" %(data_array[-1], data_array[-2]))
	print("Difference: %i" %(int(data_array[-1])-int(data_array[-2])))

def threshold_absolute(value, thresh):
	if value[0] > thresh:
		global ts
		print ("Mayor que valor")
		print( value[1])

def frequency(time_diff):
    time_diff*=2
    print("BPM", 60/time_diff)
    #print("time Diff (seconds)", time_diff)




###Main program
toogle = False;
past_bool = False;
timestamp = 0;
try:
	interfaceKit.setOnAttachHandler(interfaceKitAttached)
	interfaceKit.setOnDetachHandler(interfaceKitDetached)
	interfaceKit.setOnErrorhandler(interfaceKitError)
	interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
	interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
	interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    interfaceKit.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    interfaceKit.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Reading @ms")
print("Sensor in Analog 0")
interfaceKit.setDataRate(7,4)


print("Closing...")

print("Press Enter to quit....")

chr = sys.stdin.read(1)



try:
    interfaceKit.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
