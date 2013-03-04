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
