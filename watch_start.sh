#!/bin/bash

#usage ./watch_start runtime filePrefix

inteval=1
runtime=$1
filePrefix=$2
timestamp=`date +%m%d%H%M`

cpuFile=`echo $filePrefix\_$timestamp\_cpu.txt`
memFile=`echo $filePrefix\_$timestamp\_mem.txt`
#ioFile=`echo $filePrefix\_$timestamp\_io.txt`

sar $inteval $runtime >> $cpuFile &
sar -r $inteval $runtime >> $memFile &
