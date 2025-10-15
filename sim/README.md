Make sure actual video files are stored in `video_server/video[1-6]`, then run
```
python get_video_sizes
```

Put training data in `sim/cooked_traces` and testing data in `sim/cooked_test_traces` (need to create folders). The trace format for simulation is `[time_stamp (sec), throughput (Mbit/sec)]`. Sample training/testing data we used can be downloaded separately from `train_sim_traces` and `test_sim_traces` in https://www.dropbox.com/sh/ss0zs1lc4cklu3u/AAB-8WC3cHD4PTtYT0E4M19Ja?dl=0. More details of data preparation can be found in `traces/`.

To train a model, run 
```
python multi_agent.py
```

As reported by the A3C paper (http://proceedings.mlr.press/v48/mniha16.pdf) and a faithful implementation (https://openreview.net/pdf?id=Hk3mPK5gg), we also found the exploration factor in the actor network quite crucial for achieving good performance. A general strategy to train our system is to first set `ENTROPY_WEIGHT` in `a3c.py` to be a large value (in the scale of 1 to 5) in the beginning, then gradually reduce the value to `0.1` (after at least 100,000 iterations). 


The training process can be monitored in `sim/results/log_test` (validation) and `sim/results/log_central` (training). Tensorboard (https://www.tensorflow.org/get_started/summaries_and_tensorboard) is also used to visualize the training process, which can be invoked by running
```
python -m tensorflow.tensorboard --logdir=./results/
```
where the plot can be viewed at `localhost:6006` from a browser. 

Trained model will be saved in `sim/results/`. We provided a sample pretrained model with linear QoE as the reward signal. It can be loaded by setting `NN_MODEL = './results/pretrain_linear_reward.ckpt'` in `multi_agent.py`.




请确保实际的视频文件已存放在 video_server/video[1-6] 目录下，然后运行
python get_video_sizes
将训练数据放入 sim/cooked_traces 文件夹，测试数据放入 sim/cooked_test_traces 文件夹（需要自行创建这两个文件夹）。仿真用的 trace 格式为 [时间戳（秒）, 吞吐量（兆比特/秒）]。我们所使用的示例训练/测试数据可从以下链接单独下载：
https://www.dropbox.com/sh/ss0zs1lc4cklu3u/AAB-8WC3cHD4PTtYT0E4M19Ja?dl=0
其中 train_sim_traces 为训练数据，test_sim_traces 为测试数据。有关数据准备的更多细节，请参见 traces/ 目录下的说明。
要训练模型，请运行
python multi_agent.py
正如 A3C 原论文（http://proceedings.mlr.press/v48/mniha16.pdf）以及一项忠实复现（https://openreview.net/pdf?id=Hk3mPK5gg）所指出的，我们发现 actor 网络中的探索因子对最终性能至关重要。训练系统的一个通用策略是：
初始阶段将 a3c.py 中的 ENTROPY_WEIGHT 设为一个较大值（1 到 5 之间）；
随后逐渐减小该值，最终降至 0.1（建议至少在 100,000 次迭代后再开始降低）。
训练过程可通过以下文件进行监控：
sim/results/log_test：验证集表现
sim/results/log_central：训练集表现
此外，我们还使用 TensorBoard（https://www.tensorflow.org/get_started/summaries_and_tensorboard）来可视化训练过程。可通过以下命令启动 TensorBoard：
python -m tensorflow.tensorboard --logdir=./results/
然后在浏览器中访问 localhost:6006 查看图表。
训练好的模型将保存在 sim/results/ 目录下。我们提供了一个以线性 QoE 为奖励信号的预训练模型示例。如需加载该模型，请在 multi_agent.py 中设置：
NN_MODEL = './results/pretrain_linear_reward.ckpt'







-------------------

python multi_agent.py ，训练需要 人工 Ctrl-C 停止

Avg_entropy 稳定在 0.8–1.0 至少 20 k 步
Eps_total_reward 震荡范围缩小到 ±10 以内 且均值向上
TD_loss 保持在 0.5–2.0 小范围波动，不再穿 0 躺平