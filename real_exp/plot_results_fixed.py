# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')        # ① 无头
import matplotlib.pyplot as plt

RESULTS_FOLDER = './results/'
NUM_BINS       = 100
BITS_IN_BYTE   = 8.0
MILLISEC_IN_SEC = 1000.0
M_IN_B         = 1000000.0
VIDEO_LEN      = 48
VIDEO_BIT_RATE = [350, 600, 1000, 2000, 3000]
COLOR_MAP      = plt.cm.jet
SCHEMES        = ['fastMPC', 'robustMPC', 'BOLA', 'RL']
SIM_DP         = 'sim_dp'

def main():
    time_all = {s:{} for s in SCHEMES}
    bit_rate_all = {s:{} for s in SCHEMES}
    buff_all = {s:{} for s in SCHEMES}
    bw_all = {s:{} for s in SCHEMES}
    raw_reward_all = {s:{} for s in SCHEMES}

    # ---------- 1. 读取日志 ----------
    if not os.path.exists(RESULTS_FOLDER):
        print('results folder not found!')
        return

    log_files = [f for f in os.listdir(RESULTS_FOLDER)
                 if os.path.isfile(os.path.join(RESULTS_FOLDER, f))]
    if not log_files:
        print('no log files!')
        return

    for log_file in log_files:
        print('processing', log_file)
        time_ms, bit_rate, buff, bw, reward = [], [], [], [], []
        with open(os.path.join(RESULTS_FOLDER, log_file), 'rb') as f:
            if SIM_DP in log_file:
                for line in f:
                    parse = line.split()
                    if len(parse) == 1:
                        reward.append(float(parse[0]))
                    elif len(parse) >= 6:
                        time_ms.append(float(parse[3]))
                        bit_rate.append(VIDEO_BIT_RATE[int(parse[6])])
                        buff.append(float(parse[4]))
                        bw.append(float(parse[5]))
            else:
                for line in f:
                    parse = line.split()
                    if len(parse) <= 1:
                        continue
                    # ---- 新增：除零保护 ----
                    if float(parse[5]) == 0:
                        continue
                    # ------------------------
                    time_ms.append(float(parse[0]))
                    bit_rate.append(int(parse[1]))
                    buff.append(float(parse[2]))
                    bw.append(float(parse[4]) / float(parse[5]) *
                             BITS_IN_BYTE * MILLISEC_IN_SEC / M_IN_B)
                    reward.append(float(parse[6]))

        if SIM_DP in log_file:
            time_ms = time_ms[::-1]; bit_rate = bit_rate[::-1]
            buff = buff[::-1]; bw = bw[::-1]

        time_ms = np.array(time_ms)
        if time_ms.size == 0:          # ② 防御空文件
            print('skip empty file', log_file)
            continue
        time_ms -= time_ms[0]

        # 按 scheme 归档
        for s in SCHEMES:
            if s in log_file:
                key = log_file[len('log_' + s + '_'):]
                time_all[s][key]      = time_ms
                bit_rate_all[s][key]  = bit_rate
                buff_all[s][key]      = buff
                bw_all[s][key]        = bw
                raw_reward_all[s][key]= reward
                break

    # ---------- 2. 汇总奖励 ----------
    log_file_all = []
    reward_all   = {s:[] for s in SCHEMES}
    for key in time_all[SCHEMES[0]]:
        if all(key in time_all[s] and len(time_all[s][key])>=VIDEO_LEN for s in SCHEMES):
            log_file_all.append(key)
            for s in SCHEMES:
                reward_all[s].append(
                    raw_reward_all[s][key] if s==SIM_DP else
                    np.sum(raw_reward_all[s][key][1:VIDEO_LEN])
                )

    mean_rewards = {s: np.mean(reward_all[s]) for s in SCHEMES}

    # ---------- 3. 画总奖励对比 ----------
    fig, ax = plt.subplots(figsize=(8,5))
    for s in SCHEMES:
        ax.plot(reward_all[s], label=s + ': {:.2f}'.format(mean_rewards[s]))
    ax.legend(loc='lower right')
    ax.set_ylabel('total reward'); ax.set_xlabel('trace index')
    fig.tight_layout()
    fig.savefig('reward_comparison.png', dpi=150)
    print('saved reward_comparison.png')

    # ---------- 4. CDF ----------
    fig, ax = plt.subplots(figsize=(6,5))
    for s in SCHEMES:
        values, base = np.histogram(reward_all[s], bins=NUM_BINS)
        cumulative = np.cumsum(values) / float(values.sum())
        ax.plot(base[:-1], cumulative, label=s)
    ax.legend(loc='lower right')
    ax.set_ylabel('CDF'); ax.set_xlabel('total reward')
    fig.tight_layout()
    fig.savefig('reward_cdf.png', dpi=150)
    print('saved reward_cdf.png')

    # ---------- 5. 单 trace 时序图 ----------
    for key in time_all[SCHEMES[0]]:
        if all(key in time_all[s] and len(time_all[s][key])>=VIDEO_LEN for s in SCHEMES):
            fig, axes = plt.subplots(3, 1, figsize=(10,8), sharex=True)
            schemes_rew = []
            for i, s in enumerate(SCHEMES):
                color = COLOR_MAP(i / float(len(SCHEMES)))
                axes[0].plot(time_all[s][key][:VIDEO_LEN], bit_rate_all[s][key][:VIDEO_LEN],
                            color=color, label=s)
                axes[1].plot(time_all[s][key][:VIDEO_LEN], buff_all[s][key][:VIDEO_LEN], color=color)
                axes[2].plot(time_all[s][key][:VIDEO_LEN], bw_all[s][key][:VIDEO_LEN], color=color)
                rew = raw_reward_all[s][key] if s==SIM_DP else np.sum(raw_reward_all[s][key][1:VIDEO_LEN])
                schemes_rew.append('{}: {:.2f}'.format(s, rew))

            axes[0].set_ylabel('bit rate (Kbps)')
            axes[1].set_ylabel('buffer (sec)')
            axes[2].set_ylabel('bandwidth (Mbps)')
            axes[2].set_xlabel('time (sec)')
            axes[0].legend(schemes_rew, loc=9, bbox_to_anchor=(0.5, 1.15), ncol=len(SCHEMES))
            fig.tight_layout()
            fig.savefig('trace_{}.png'.format(key), dpi=150)
            plt.close(fig)
    print('all figures saved.')


if __name__ == '__main__':
    main()