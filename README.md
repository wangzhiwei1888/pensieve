# Pensieve
Pensieve is a system that generates adaptive bitrate algorithms using reinforcement learning.
http://web.mit.edu/pensieve/

### Prerequisites
- Install prerequisites (tested with Ubuntu 16.04, Tensorflow v1.1.0, TFLearn v0.3.1 and Selenium v2.39.0)
```
python setup.py
```

### Training
- To train a new model, put training data in `sim/cooked_traces` and testing data in `sim/cooked_test_traces`, then in `sim/` run `python get_video_sizes.py` and then run
```
python multi_agent.py
```

The reward signal and meta-setting of video can be modified in `multi_agent.py` and `env.py`. More details can be found in `sim/README.md`.

### Testing
- To test the trained model in simulated environment, first copy over the model to `test/models` and modify the `NN_MODEL` field of `test/rl_no_training.py` , and then in `test/` run `python get_video_sizes.py` and then run 
```
python rl_no_training.py
```

Similar testing can be performed for buffer-based approach (`bb.py`), mpc (`mpc.py`) and offline-optimal (`dp.cc`) in simulations. More details can be found in `test/README.md`.

### Running experiments over Mahimahi
- To run experiments over mahimahi emulated network, first copy over the trained model to `rl_server/results` and modify the `NN_MODEL` filed of `rl_server/rl_server_no_training.py`, and then in `run_exp/` run
```
python run_all_traces.py
```
This script will run all schemes (buffer-based, rate-based, Festive, BOLA, fastMPC, robustMPC and Pensieve) over all network traces stored in `cooked_traces/`. The results will be saved to `run_exp/results` folder. More details can be found in `run_exp/README.md`.

### Real-world experiments
- To run real-world experiments, first setup a server (`setup.py` automatically installs an apache server and put needed files in `/var/www/html`). Then, copy over the trained model to `rl_server/results` and modify the `NN_MODEL` filed of `rl_server/rl_server_no_training.py`. Next, modify the `url` field in `real_exp/run_video.py` to the server url. Finally, in `real_exp/` run
```
python run_exp.py
```
The results will be saved to `real_exp/results` folder. More details can be found in `real_exp/README.md`.


Pensieve 是一个利用强化学习自动生成自适应码率（ABR）算法的系统。
官网：http://web.mit.edu/pensieve/
一、环境准备
    （已在 Ubuntu 16.04 + TensorFlow 1.1.0 + TFLearn 0.3.1 + Selenium 2.39.0 测试通过）
    一键安装依赖：
    python setup.py

二、训练新模型
    把训练 traces 放进 sim/cooked_traces，测试 traces 放进 sim/cooked_test_traces。
    
    在 sim/ 目录下执行：
    python get_video_sizes.py
    python multi_agent.py

    奖励函数、视频元参数等可在 multi_agent.py 和 env.py 中修改，详见 sim/README.md。

三、在仿真环境中测试
    将训练好的模型复制到 test/models。
    修改 test/rl_no_training.py 中的 NN_MODEL 路径。
    在 test/ 目录下执行：

    python get_video_sizes.py
    python rl_no_training.py

    同样方式可测试
        基于缓冲的算法（bb.py）
        MPC（mpc.py）
        离线最优（dp.cc）
        详见 test/README.md。

四、使用 Mahimahi 模拟网络做实验
    把模型复制到 rl_server/results 并修改 rl_server/rl_server_no_training.py 中的 NN_MODEL 路径。
    在 run_exp/ 目录下执行：

    python run_all_traces.py

    该脚本会自动对比以下算法：
    buffer-based、rate-based、Festive、BOLA、fastMPC、robustMPC 以及 Pensieve。
    结果保存在 run_exp/results/，详见 run_exp/README.md。

五、真实网络实验

    执行 setup.py 会自动安装 Apache 服务器，并把所需文件放到 /var/www/html。
    将模型复制到 rl_server/results 并修改 rl_server/rl_server_no_training.py 中的 NN_MODEL 路径。

    修改rl_server_no_training.py 的内容 server_address 改为 server_address = ('0.0.0.0', port)
    python rl_server_no_training.py
    http://192.168.40.81:8333/

    因为上面 已经安装过Apache服务器所以现在可以通过 访问

    http://192.168.40.81/

    查看 /var/www/html 目录下的文件
    
    dash.all.min.js  Manifest.mpd     myindex_BOLA.html     myindex_FESTIVE.html  myindex_newdash.html  myindex_RL.html         video1  video3  video5
    index.html       myindex_BB.html  myindex_fastMPC.html  myindex_FIXED.html    myindex_RB.html       myindex_robustMPC.html  video2  video4  video6

    修改 dash.all.min.js 文件中的 内容 将 localhost:8333 换为 192.168.40.81:8333
    :%s/localhost/192.168.40.81/g


    修改 real_exp/run_video.py 里的 url 字段，指向你的服务器地址。

    localhost -> 192.168.40.81

    
    sudo pip install 'pyvirtualdisplay==0.2.5' 'easyprocess==0.2.3'
    sudo dpkg -r google-chrome-stable
    sudo apt-get -f install
    sudo apt install chromium-browser
    
    python run_video.py robustMPC 280 0

    Message: u'timeout: cannot determine loading status\nfrom timeout: Timed out receiving message from renderer: -0.004\n  (Session info: chrome=90.0.4430.72)\n  (Driver info: chromedriver=2.27.440175 (9bc1d90b8bfa4dd181fbbf769a5eb5e575574320),platform=Linux 4.15.0-112-generic x86_64)'
    
    chromedriver 2.27 太老，无法驱动 Chromium 90（2021 年发布）的新协议，于是打开页面后 “收不到 renderer 心跳” 而超时。

    # 1. 备份旧 driver（可选）
    mv ../abr_browser_dir/chromedriver ../abr_browser_dir/chromedriver.old

    # 2. 下载并解压 90 版
    cd /tmp
    wget https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    mv chromedriver ../abr_browser_dir/chromedriver   # 放回脚本目录

    # 3. 确认版本
    ../abr_browser_dir/chromedriver --version
    # 应显示 90.0.4430.24
    
    在 rl_server/ 目录下执行：
    python simple_server.py 监听 8333 端口，

    在 real_exp/ 目录下执行：
    测试可以先执行
    python run_video.py BOLA 280 0
    并在 本目录下生成 result/log 文件，
    执行 python plot_log.py 生成 log.png 文件
    
    在 real_exp/ 目录下执行：（此时要停止本地监听的 8333 端口，因为代码中会自动启动该端口）
    python run_exp.py


    日志格式 log_robustMPC_0 文件为例
    wall_time(ms) | 实际bitrate(Kbps) | buffer(s) | 本次卡顿(s) | chunk大小(Byte) | 下载时间(ms) | reward
    1760583352.72	750	    4	0.011	450283	2	-0.04730000000000001
    1760583352.78	4300	8	0.0	2123065	6	0.75
    1760583352.84	4300	12	0.0	2177073	6	4.3
    1760583352.9	4300	16.0	0.0	2160877	6	4.3
    1760583352.96	4300	20	0.0	2233056	8	4.3
    1760583353.02	4300	24	0.0	1941625	6	4.3
    1760583353.07	4300	28	0.0	2157535	6	4.3
    1760583353.13	4300	32	0.0	2290172	6	4.3
    1760583353.19	4300	36	0.0	2055469	7	4.3
    1760583353.25	4300	40	0.0	2169201	6	4.3
    1760583353.3	4300	44	0.0	2173522	6	4.3
    1760583353.36	4300	48	0.0	2102452	6	4.3
    1760583353.42	4300	52	0.0	2209463	7	4.3
    1760583353.48	4300	56	0.0	2275376	7	4.3


    实验结果将保存在 real_exp/results/，详见 real_exp/README.md。


    问题处理：
    https://www.kimi.com/share/d3nkrs9nu955ikd1a910


