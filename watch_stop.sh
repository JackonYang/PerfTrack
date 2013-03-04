#!/bin/bash

pid=`ps -ef |grep sar|grep -v grep| awk '{print $2}'`
for i in $pid
do
	kill -9 $i
done
