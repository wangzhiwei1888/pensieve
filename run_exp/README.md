This set of code runs experiments over Mahimahi. It loads the traces from `cooked_traces/` and invokes ABR servers from `rl_servers/`. Selenium on top of a PyVirtualDisplay is used and the actual graphics is disabled.

Trained RL model needs to be saved in `rl_server/results/`. We provided a sample pretrained model with linear QoE as the reward signal. It can be loaded by setting `NN_MODEL = '../rl_server/results/pretrain_linear_reward.ckpt'` in `rl_server/rl_server_no_training.py`.

Traces need to be put in `cooked_traces/` (in Pensieve home directory), in Mahimahi format. The format details can be found if `traces/` and we provide some preprocessed data, which can be downloaded from `cooked_traces` at https://www.dropbox.com/sh/ss0zs1lc4cklu3u/AAB-8WC3cHD4PTtYT0E4M19Ja?dl=0. 

RL, robustMPC, MPC are implemented in `rl_servers/`. Other ABR schemes, namely BB, RB, Festival, BOLA and DASH original, are natively supported in `dash.js/`, where the switch `abrAlgo` can be found in `dash.js/src/streaming/controllers/AbrController.js`. These algorithms are called from specific HTML files in `video_server/`.

To conduct the experiment, run
```
python run_all_traces.py
```

To view the results, modify `SCHEMES` in `plot_results.py` (it checks the file name of the log and matches to the corresponding ABR algorithm), then run 
```
python plot_results.py
```


这段代码在 Mahimahi 上运行实验。它会从 cooked_traces/ 加载网络轨迹，并调用 rl_servers/ 中的 ABR 服务器。实验使用基于 PyVirtualDisplay 的 Selenium，并关闭了真实图形界面。

训练好的 RL 模型需保存在 rl_server/results/ 目录下。我们提供了一个以线性 QoE 为奖励信号的预训练模型示例，只需在 rl_server/rl_server_no_training.py 中设置
NN_MODEL = '../rl_server/results/pretrain_linear_reward.ckpt' 即可加载。

轨迹文件需放在 Pensieve 主目录下的 cooked_traces/ 中，格式须符合 Mahimahi 要求。格式细节可参考 traces/；我们也提供了一些预处理好的数据，可通过以下 Dropbox 链接下载：
https://www.dropbox.com/sh/ss0zs1lc4cklu3u/AAB-8WC3cHD4PTtYT0E4M19Ja?dl=0

RL、robustMPC、MPC 三种算法已在 rl_servers/ 中实现。其余 ABR 方案（BB、RB、Festival、BOLA 及原生 DASH）由 dash.js/ 原生支持，切换开关位于 dash.js/src/streaming/controllers/AbrController.js 中的 abrAlgo。这些算法通过 video_server/ 下的特定 HTML 文件调用。

运行实验：
    python run_all_traces.py
查看结果：先修改 plot_results.py 中的 SCHEMES（脚本会根据日志文件名匹配对应 ABR 算法），然后执行
    python plot_results.py
