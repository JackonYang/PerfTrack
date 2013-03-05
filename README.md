linux performance monitoring and visualization
==============================================

linux 性能监控与图像显示

#### Introduction

启动、关闭~sar~监控系统运行状态，并将性能运行信息写入文件,
显示性能曲线，清理数据文件。
显示性能曲线时，根据性能测试的需求，对原始数据进行滤波。

滤波原理: 消除周期小、波动幅度低
的短脉冲，保留缓慢变化曲线和波动幅度大于阈值(默认 5%)的短脉冲。

#### usage

<pre><code>
# start, output in: filePrefix_timestamp_cpu.txt,filePrefix_timestamp_mem.txt
$ ./watch.sh start filePrefix`
# stop script
$ ./watch.sh stop
# show visually
$ ./watch.sh show filePre_with_timestamp
# rm data files
$ ./watch.sh clean
</code></pre>

![example of monitor][exp_monitor]

#### 监控指标及图像分析

1. user是用户进程占用的百分比，system是系统进程的CPU占有率。all是总的cpu占有率。
2. 正常情况下，sys占有率很低。
3. 总的CPU占有率持续超过70%，属于过负荷运行。需定位问题原因并解决。


[exp_monitor]:example_monitor.jpeg 'example of monitor'
