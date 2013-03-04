import readdata
import sys

filename=sys.argv[1]
nskip=2
dataToRead=[2,4,7]

res=readdata.readData(filename, nskip, dataToRead)

print len(res),len(res[0])
