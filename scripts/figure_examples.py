# -*- coding: utf-8 -*-
"""汇报配图示例模板（matplotlib + numpy）。四种最常用的图，按需取用：

  1) fig_trajectory  轨迹对比图（结果类：预测 vs 真实）——有仿真/测试数据时用
  2) fig_training    训练过程图（loss / 指标随轮次曲线）——模型训练汇报用
  3) fig_structure   结构框图（框架图：模块方框＋箭头）——新旧模型/系统结构对比用
  4) fig_sketch      方法示意图（如"旧分格 vs 新分段"）——没有真实数据时自造的示意

用法：把对应函数里的示例数据换成你的真实数据；没有真实数据就用示意数据，
图注里必须写"示意图"。输出建议存到工作目录的 汇报图/ 文件夹，再插入汇报 docx。

依赖：pip install matplotlib numpy
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False

OUT = Path("汇报图")
OUT.mkdir(exist_ok=True)


# 1) 轨迹对比图：预测 vs 真实
def fig_trajectory(path):
    t = np.linspace(0, 30, 300)          # ← 换成你的时间轴
    true_x, true_y = 8 * t, 20 * np.sin(t / 6)                          # ← 真实轨迹
    pred_x, pred_y = true_x + .5 * t * np.sin(t / 4), true_y + .4 * t   # ← 预测轨迹
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(true_x, true_y, "k-", lw=1.6, label="真实轨迹")
    ax.plot(pred_x, pred_y, "r--", lw=1.2, label="预测轨迹")
    ax.annotate("误差开始增大", xy=(250, 5), xytext=(150, -30),
                arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.set_xlabel("X (m)"); ax.set_ylabel("Y (m)")
    ax.legend(); ax.axis("equal")
    fig.savefig(path, dpi=200, bbox_inches="tight"); plt.close(fig)


# 2) 训练过程图：loss / 指标曲线
def fig_training(path):
    ep = np.arange(0, 1501, 25)
    loss = 500 * np.exp(-ep / 300) + 5          # ← 换成你的真实曲线
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(ep, loss, "k-", lw=1.2)
    ax.set_yscale("log")
    ax.set_xlabel("训练轮次"); ax.set_ylabel("误差（对数轴）")
    ax.grid(alpha=0.3)
    fig.savefig(path, dpi=200, bbox_inches="tight"); plt.close(fig)


# 3) 结构框图：新旧结构对比
def fig_structure(path):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))

    def box(ax, x, y, w, h, text, fc="#eef3fb", ec="#3b6db4"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=fc, ec=ec, lw=1.3))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5)

    def arrow(ax, p, q):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", color="0.35", lw=1.2, mutation_scale=12))

    for ax in (a1, a2):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    a1.set_title("旧：单一大网络", fontsize=11)
    box(a1, 2, 7.5, 6, 1.4, "输入")
    box(a1, 2, 4.5, 6, 1.6, "大网络（硬拟合）", fc="#fdeeee", ec="#c05050")
    box(a1, 2, 1.5, 6, 1.4, "输出")
    arrow(a1, (5, 7.5), (5, 6.1)); arrow(a1, (5, 4.5), (5, 2.9))
    a2.set_title("新：双通路（先估基准＋修正）", fontsize=11)
    box(a2, 2, 7.5, 6, 1.4, "输入")
    box(a2, 0.5, 4.5, 4, 1.8, "物理模块\n（估基准）", fc="#eaf7ec", ec="#3f8f4f")
    box(a2, 5.5, 4.5, 4, 1.8, "修正模块\n（削偏差）", fc="#eaf7ec", ec="#3f8f4f")
    box(a2, 2, 1.5, 6, 1.4, "基准＋修正")
    arrow(a2, (4, 7.5), (2.5, 6.3)); arrow(a2, (6, 7.5), (7.5, 6.3))
    arrow(a2, (2.5, 4.5), (4, 2.9)); arrow(a2, (7.5, 4.5), (6, 2.9))
    fig.savefig(path, dpi=200, bbox_inches="tight"); plt.close(fig)


# 4) 方法示意图：旧分类 vs 新分类（示意数据；图注写"示意图"）
def fig_sketch(path):
    t = np.arange(600) / 60.0                     # 10 秒示意
    spd = np.clip(14 * (1 - np.exp(-t / 1.2)) - 6 * (t > 6.5), 0, None)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 4.2), sharex=True)
    cell = (spd * 4).astype(int)                  # 示意：按状态分格
    a1.scatter(t, spd, c=cell, cmap="hsv", s=6, marker="s")
    a1.set_title("旧：按单帧状态分格（同一段动作被切成几十格）", fontsize=10.5)
    a2.plot(t, spd, "k-", lw=1.2)
    for s in (1.2, 2.3, 6.5, 7.2):
        a2.axvline(s, color="tab:red", ls="--", lw=0.8)
    a2.set_title("新：按完整动作分段（起步 / 巡航 / 减速 / 滑行）", fontsize=10.5)
    a2.set_xlabel("时间（秒）")
    for ax in (a1, a2):
        ax.set_ylabel("速度 (m/s)")
    fig.savefig(path, dpi=200, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    fig_trajectory(OUT / "图_轨迹对比.png")
    fig_training(OUT / "图_训练过程.png")
    fig_structure(OUT / "图_结构对比.png")
    fig_sketch(OUT / "图_分类示意.png")
    print("示例图已输出到", OUT)
