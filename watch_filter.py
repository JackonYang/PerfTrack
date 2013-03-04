#show cpu and memory runtime infomation
import readdata

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

timestamp=sys.argv[1]

#line to skip
nskip=2
#cpu col
colsCpu=[2,4,7]
colsMem=[3,7]
idxIdle=2

#path of data files
s=os.getcwd()
#data files to plot
files=[files for files in os.listdir(s) if (files.find(timestamp)!= -1)]

for datafile in files:
	if(datafile.find("cpu") != -1):
		cpudata=readdata.readData(datafile,nskip,colsCpu)
	if(datafile.find("mem") != -1):
		memdata=readdata.readData(datafile,nskip,colsMem)

#cpu idle operate
cpudata[idxIdle][0]="%totalCPUUsed"
for i in range(1,len(cpudata[idxIdle])):
	cpudata[idxIdle][i]=100-float(cpudata[idxIdle][i])

#plot data
title=[]
for i in range(len(colsCpu)):
	title.append(cpudata[i].pop(0))
	plt.plot(cpudata[i])

for i in range(len(colsMem)):
	title.append(memdata[i].pop(0))
	plt.plot(memdata[i])	
	plt.legend(title)
#plt.title("cpu and memory runtime info")
plt.show()
