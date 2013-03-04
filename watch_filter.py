#show cpu and memory runtime infomation
import filtration

import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def keepPeak(data,colsToFilter):
	#one of wave filtration methods
	#input: a list and colsTofilter
	#output: return a list contains data of  colsTofilter.
	# each column two data
	#if max-min <= 5, return 2 middle data
	#else return max and min row

	delta=5 #peak range
	nCols=len(colsToFilter)
	#copy userful data to a new list in columns
	colData=[]
	for i in range(nCols):
		colData.append([])

	for line in data:
		line=line.split()
		for i in range(nCols):
			colData[i].append(line[colsToFilter[i]])
	#choose 2 data for each column
	res=[]
	for idata in colData:
		maxData=max(idata)
		minData=min(idata)
		if (float(maxData)-float(minData)>delta):
			if(idata.index(maxData)<idata.index(minData)):
				res.append([maxData,minData])
			else:
				res.append([minData,maxData])
		else:
			idata.sort()
			n=len(idata)/2
			res.append(idata[n-1:n+1])
	return res

def readData(filename,nskip,dataToRead):
	""" read columns of dataToRead from filename
	return a list of data, each dataToRead a column
	considering the amount of memory, keep peak filteration is used"""

	f=open(filename,'r')
	#skip n lines
	while(nskip):
		f.readline()
		nskip=int(nskip)-1
	#get 1st line to init the title
	titleline=f.readline().split()
	#init the 1st line of data with title
	data=[]
	for i in range(len(dataToRead)):
		data.append([])
		data[i].append(titleline[dataToRead[i]])

	#read data
	dataBuffer=f.readlines(1)
	while (len(dataBuffer)!=0):
		#every 7 rows a group to filter, 
		#extend filter result list to data list
		filterStep=7
		for i in range(0,len(dataBuffer),filterStep):#[:-1]:
			filterRes=filtration.keepPeak(dataBuffer[i:i+filterStep],dataToRead)
			for j in range(len(dataToRead)):
				data[j].extend(filterRes[j])
		dataBuffer=f.readlines(1)
	return data

def plot():
	"""plot data"""
	global colsCpu
	global colsMem

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
files=[files for files in os.listdir(s) if (files.find(timestamp) > -1)]

for datafile in files:
	if(datafile.find("cpu") != -1):
		cpudata=readdata.readData(datafile,nskip,colsCpu)
	if(datafile.find("mem") != -1):
		memdata=readdata.readData(datafile,nskip,colsMem)

#cpu idle operate
cpudata[idxIdle][0]="%totalCPUUsed"
for i in range(1,len(cpudata[idxIdle])):
	cpudata[idxIdle][i]=100-float(cpudata[idxIdle][i])

plot()
