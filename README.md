performance-monitoring
======================

linux performance monitoring and 可视化

#### 启动性能监控脚本，cpu与memory信息记录于文件中。

``` bash cmd to run
# start, output in: filePrefix_timestamp_cpu.txt,filePrefix_timestamp_mem.txt
$ ./watch.sh start filePrefix`
# stop script
$ ./watch.sh stop
# show visually
$ ./watch.sh show filePre_with_timestamp
# rm data files
$ ./watch.sh clean

![example of monitor][exp_monitor]

#### 监控指标及图像分析

1. user是用户进程占用的百分比，system是系统进程的CPU占有率。all是总的cpu占有率。
2. 正常情况下，sys占有率很低。
3. 总的CPU占有率持续超过70%，属于过负荷运行。需定位问题原因并解决。


[exp_monitor]:example_monitor.jpeg 'example of monitor'
