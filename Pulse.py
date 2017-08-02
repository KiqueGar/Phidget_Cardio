#!/usr/bin/env python
#Basic imports

"""
No licence yet
Plots in selected interval, not configurable grid (yet)
- Scale y axis
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
import matplotlib.pyplot as plt
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetLogLevel

sys.setrecursionlimit(1500)
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
	print("|- Attached -|-			  Type			  -|- Serial No. -|-  Version -|")
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

def interfaceKitInputChanged(e):
	source = e.device
	print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

def interfaceKitSensorChanged(e):
	source = e.device
	#print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))
	#print("InterfaceKit: Sensor %i: %i" % (e.index, e.value))
	global datas
	global t_array
	max_data = 1000


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

def plot(values, times):
	#plt.close()
	print(len(values))
	times=np.asarray(times) - times[0]
	plt.plot(times, values,linewidth=1.5, markersize=20)
	plt.ylim(500,3500)
	plt.grid(True)
	plt.xlim(times[0],times[-1], .04)
    #if len(values) >150:
	#	print("BIG DATA!")
		#plt.xlim(times[-150],times[-1], .04)
	plt.pause(.0001)
	#plt.ylabel("100 measures")
	plt.show()
	plt.gcf().clear()

	
def raw_read(timestamp):
	global datas
	global  t_array

	max_data = 200
	data = interfaceKit.getSensorRawValue(2)
	print("Analog read: ")
	datas.append(int(data))
	t_array.append(timestamp)

	if len(datas)>max_data:
		trim_datas = datas[9:max_data]
		#datas=datas[1:]
		datas = trim_datas
		trim_times = t_array[9:max_data]
		t_array = trim_times
		#t_array=t_array[1:]
	if len(datas)%10==0:
		if len(datas)>250:
			plot(datas[-250::], t_array[-250::])
		else:
		  plot(datas, t_array)




###Main program
datas =[]
t_array = []
plt.ion()
plt.title("Pulse")
plt.xlabel("Time")

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
interfaceKit.setDataRate(0,2)


print("Closing...")

print("Press Enter to quit....")

#chr = sys.stdin.read(1)
old_time= time.time()
i=0;
#	_init()
while(i<15000000):
	ts=time.time()
	if ts-old_time > .02:
		print("Reading... %i"%(i))
		raw_read(ts)
		old_time = ts
		i += 1
"""
	if (i %100 == 0 and len(datas)>=100):
		print("Graph and continue")
			(t_array[:90], datas[:90])
"""


try:
	interfaceKit.closePhidget()
except PhidgetException as e:
	print("Phidget Exception %i: %s" % (e.code, e.details))
	print("Exiting....")
	exit(1)

print("Done.")
exit(0)
