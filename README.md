performance-monitoring
======================

linux performance monitoring and 可视化

#### 启动性能监控脚本，cpu与memory信息记录于文件中。

`./watch_start times filePrefix`

times暂时为运行次数。根据runtime计算最佳统计间隔和次数的模块未实现。

记录文件名：`filePrefix_timestamp_cpu.txt` 或 `filePrefix_timestamp_mem.txt`

#### 查看CPU与mem统计图像。

`python watch_show.py timestamp`

#### 脚本停止与环境清理

`./watch_stop.sh`

`./watch_clean.sh`: 清理脚本执行时生成的全部cpu和mem记录文件。

[pic]:example_monitor.jpeg 'example of monitor'


#### 监控指标及图像分析

1. user是用户进程占用的百分比，system是系统进程的CPU占有率。all是总的cpu占有率。
2. 正常情况下，sys占有率很低。
3. 总的CPU占有率持续超过70%，属于过负荷运行。需定位问题原因并解决。
