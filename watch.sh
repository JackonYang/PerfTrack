#!/bin/bash

function start {
	#usage ./watch_start filePrefix runtime

	inteval=1
	filePrefix=$1
	timestamp=`date +%m%d%H%M`

	cpuFile=`echo $filePrefix\_$timestamp\_cpu.txt`
	memFile=`echo $filePrefix\_$timestamp\_mem.txt`
	#ioFile=`echo $filePrefix\_$timestamp\_io.txt`

	sar $inteval >> $cpuFile &
	sar -r $inteval >> $memFile &
}

function stop {
	pid=`ps -ef |grep sar|grep -v grep| awk '{print $2}'`
	for i in $pid
	do
		kill -9 $i
	done
}

function clean {
	rm -f *_cpu.txt *_mem.txt
}

function show {
	python show.py $1
}

# cmd, filename_pre
$1 $2
