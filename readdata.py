import filtration

def readData(filename,nskip,dataToRead):
	#read columns of dataToRead from file name filename
	#input: filename,nskip,colums of dataToRead
	#output: a list of data, each dataToRead a column
	#considering the amount of memory, keep peak filteration is used

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
