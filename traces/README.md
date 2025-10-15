- To download the raw data, follow

```
# FCC broadband dataset
$ wget http://data.fcc.gov/download/measuring-broadband-america/2016/data-raw-2016-jun.tar.gz
$ tar -xvzf data-raw-2016-jun.tar.gz -C fcc

# Norway HSDPA bandwidth logs
$ wget -r --no-parent --reject "index.html*" http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/

# Belgium 4G/LTE bandwidth logs (bonus)
$ wget http://users.ugent.be/~jvdrhoof/dataset-4g/logs/logs_all.zip
$ unzip logs_all.zip -d belgium
```

- For actual video streaming over Mahimahi (http://mahimahi.mit.edu), the format of the traces should be converted to the following
```
Each line gives a timestamp in milliseconds (from the beginning of the
trace) and represents an opportunity for one 1500-byte packet to be
drained from the bottleneck queue and cross the link. If more than one
MTU-sized packet can be transmitted in a particular millisecond, the
same timestamp is repeated on multiple lines.
```
An example mahimahi trace `run_exp/12mbps` depicts 12Mbit/sec bandwidth. More details of mahimahi trace file requirements can be found in https://github.com/ravinet/mahimahi/tree/master/traces. In our case, the script `convert_mahimahi_format.py` in `traces/norway/` and `traces/fcc/` can be used. Some samples of preprocessed data can be downloaded in `cooked_traces` from https://www.dropbox.com/sh/ss0zs1lc4cklu3u/AAB-8WC3cHD4PTtYT0E4M19Ja?dl=0.

- For simulations, the format should be `[time_stamp (sec), throughput (Mbit/sec)]`. Some sample can be downloaded in `train_sim_traces` and `test_sim_traces` from https://www.dropbox.com/sh/ss0zs1lc4cklu3u/AAB-8WC3cHD4PTtYT0E4M19Ja?dl=0.








下载原始数据
FCC 宽带数据集
    wget http://data.fcc.gov/download/measuring-broadband-america/2016/data-raw-2016-jun.tar.gz
    tar -xvzf data-raw-2016-jun.tar.gz -C fcc
挪威 HSDPA 带宽日志
    wget -r --no-parent --reject "index.html*" http://home.ifi.uio.no/paalh/dataset/hsdpa-tcp-logs/
比利时 4G/LTE 带宽日志（额外补充）
    wget http://users.ugent.be/~jvdrhoof/dataset-4g/logs/logs_all.zip
    unzip logs_all.zip -d belgium
用于 Mahimahi 实际视频流实验的格式要求
    Mahimahi（http://mahimahi.mit.edu）要求的 trace 格式如下：
    每一行是一个毫秒级时间戳（从 trace 开始计时），表示一个 1500 字节的数据包可以被送出瓶颈队列的时刻。如果某一毫秒内可以传输多个 MTU 大小的包，则同一时间会重复多行。
    示例：run_exp/12mbps 就是一个表示 12Mbps 带宽的 Mahimahi trace 文件。
    更详细的格式说明见：https://github.com/ravinet/mahimahi/tree/master/traces
    我们在 traces/norway/ 和 traces/fcc/ 中提供了转换脚本 convert_mahimahi_format.py，可将原始数据转为 Mahimahi 所需格式。
    预处理好的样例数据可在下方链接的 cooked_traces 文件夹中下载：
    https://www.dropbox.com/sh/ss0zs1lc4cklu3u/AAB-8WC3cHD4PTtYT0E4M19Ja?dl=0
用于仿真的格式要求
    仿真用的 trace 格式更简单：
    每行两个数字，空格分隔：
    [时间戳（秒）, 吞吐量（兆比特/秒）]
    样例数据可在上方链接的 train_sim_traces 和 test_sim_traces 文件夹中直接下载使用。