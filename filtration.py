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
