This set of code runs experiments over real world networks. Selenium on top of a PyVirtualDisplay is used and the actual graphics is disabled.

Trained RL model needs to be saved in `rl_server/results/`. We provided a sample pretrained model with linear QoE as the reward signal. It can be loaded by setting `NN_MODEL = '../rl_server/results/pretrain_linear_reward.ckpt'` in `rl_server/rl_server_no_training.py`.

RL, robustMPC, MPC are implemented in `rl_servers/`. Other ABR schemes, namely BB, RB, Festival, BOLA and DASH original, are natively supported in `dash.js/`, where the switch `abrAlgo` can be found in `dash.js/src/streaming/controllers/AbrController.js`. These algorithms are called from specific HTML files in `video_server/`. Experiments run over RL, robustMPC, MPC and BOLA in random shuffles.

To conduct the experiment, modify `url` in `run_video.py` to the server address, and then run
```
python run_exp.py
```

To view the results, modify `SCHEMES` in `plot_results.py` (it checks the file name of the log and matches to the corresponding ABR algorithm), then run 
```
python plot_results.py
```


这组代码用于在真实网络环境下跑实验。
它用 Selenium + PyVirtualDisplay 做无头浏览器，不显示真实图形界面。


文件与模型准备
    训练好的 RL 模型请放到 rl_server/results/。
    我们给了一个预训练模型（线性 QoE 奖励），
    在 rl_server/rl_server_no_training.py 里设
    NN_MODEL = '../rl_server/results/pretrain_linear_reward.ckpt' 即可加载。


算法位置
    | 算法                                      | 实现位置                                                                                  |
    | --------------------------------------- | ------------------------------------------------------------------------------------- |
    | **RL / robustMPC / MPC**                | `rl_server/` 下的独立 Python 服务                                                           |
    | **BB / RB / Festival / BOLA / DASH 原生** | 由 `dash.js` 原生支持，开关在 `dash.js/src/streaming/controllers/AbrController.js` 的 `abrAlgo` |


    每种算法对应 video_server/ 里一个专用 HTML 文件；
    实验会在 RL / robustMPC / MPC / BOLA 之间随机打乱顺序重复跑。

跑实验
    把 run_video.py 里的 url 改成你的服务器地址；
    执行
    python run_exp.py
    脚本会自动轮流调用各算法，持续指定时长，日志落盘。

看结果
    打开 plot_results.py，把 SCHEMES 列表改成你跑过的算法（脚本按日志文件名匹配算法）；
    运行
    python plot_results.py
    

一句话总结
把模型放好 → 改服务器地址 → python run_exp.py 跑实验 → python plot_results.py 出图。


plot_results_fixed.py 文件执行方式
MPLBACKEND=Agg python plot_results_fixed.py
