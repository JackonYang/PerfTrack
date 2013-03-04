#read data from datafile and plot cpu/mem

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

timestamp=sys.argv[1]
#timestamp='03041503'

#lines to skip
nskip=2
#colums to plot
cpuCols=[2,4,7]
memCols=[3,7]
#special date in cpuCols
idleIdx=2
#data files to plot
files=[files for files in os.listdir(os.getcwd()) if (files.find(timestamp) > -1)]

#def readData function
def readData(filename, nskip, colsToPlot):
	f=open(filename, 'r')
	#skip lines before title line
	while(nskip):
		f.readline()
		nskip=int(nskip)-1

	#read title line and init data lists with title
	titleLine=f.readline().split()
	data=[]
	for i in range(len(colsToPlot)):
		data.append([])
		data[i].append(titleLine[colsToPlot[i]])

	#read data
	for line in f:
		line=line.split()
		for i in range(len(colsToPlot)):
			data[i].append(line[colsToPlot[i]])
	return data

#read data from files and init lists with readData function
for datafile in files:
	if(datafile.find("_cpu.txt") > -1):
		cpudata=readData(datafile, nskip, cpuCols)
	if(datafile.find("_mem.txt") > -1):
		memdata=readData(datafile, nskip, memCols)

#more operation on idle
cpudata[idleIdx][0]="%TotalCpuUsed"
for i in range(1, len(cpudata[idleIdx])):
	cpudata[idleIdx][i]=100-float(cpudata[idleIdx][i])

#plot data
title=[]
plt.figure(1)
for i in range(len(cpuCols)):
	title.append(cpudata[i].pop(0))
	plt.plot(cpudata[i])

for i in range(len(memCols)):
	title.append(memdata[i].pop(0))
	plt.plot(memdata[i])
plt.legend(title)
plt.show()
