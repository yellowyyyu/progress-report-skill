# progress-report-skill

一个 Claude Code 技能：把项目进展写成人能一眼看懂的**进展汇报 Word 文档**。

写作规范来自一份真实定稿（读者是领导），核心要求：每节都是"**发现了什么问题 → 用了什么办法（方法可专业）→ 效果如何（要简单，带数字）**"，不写套话、不粉饰短板。

## 特点

- **写法固定**：总览 → 按时间分节（日期行＋版本/主题行）→ 问题/做法/结果 → 新旧对比用左右对照表 → 诚实写短板 → 一两页收尾
- **排版固定**：宋体＋Times New Roman、全部五号、单倍行距、首行缩进、两端对齐、黑色、仅标题行加粗
- **块与块之间空一行**，方便阅读（总览后、每个标题前、每张表后、图前后、结尾句前）
- **配图规则**：结果必须有图（轨迹对比图/训练过程图/仿真图）；没有现成数据就自造框架图、示意图（示意必须标注"示意图"）
- 附 python-docx 与 matplotlib 生成模板，一条命令出 .docx 和配图

## 效果示例（节选）

```
进展汇报（9月30日—10月7日）

总览：这项工作让模型学会根据动作预测车辆状态变化……误差从160米降到33.3米。

10月2日            ← 日期行（加粗）
Model-v11          ← 版本/主题行（加粗）
问题：模型自推演前30秒还准，后面越推越偏，终点差160米。
查因：误差全部出在转弯上；训练数据里"高速持续右转"只有3帧。
（空行）
10月2日、3日
Model-v12/v13
1.输入加长：模型看的历史从16帧加到32帧……
2.镜像增广：把已有的左转数据镜像成右转……
结果：推演误差从160米降到7.8米。成绩算样本内，只能说明方法可行。
```

完整格式见 `examples/sample-report.md`。

## 安装

### 方式一：作为 Claude Code 技能（推荐）

把本仓库的 `SKILL.md` 和 `scripts/` 放进技能目录：

```
# 用户级（所有项目可用）
~/.claude/skills/progress-report/SKILL.md
~/.claude/skills/progress-report/scripts/make_report_docx.py

# 或项目级
<你的项目>/.claude/skills/progress-report/...
```

之后直接对 Claude 说"给××项目写一份进展汇报"，技能自动触发。

### 方式二：不用 Claude，手动生成

```bash
pip install python-docx
python scripts/make_report_docx.py   # 编辑脚本顶部 OUT 和结尾"内容区"
```

## 依赖与需求

| 依赖 | 说明 |
|---|---|
| Python | 3.9+ |
| python-docx | `pip install python-docx`（生成 Word） |
| matplotlib + numpy | `pip install matplotlib numpy`（画配图用） |
| 中文字体 | 宋体、Times New Roman（Windows 自带；macOS/Linux 请在脚本顶部把 `CN_FONT` 换成等效字体，如 Songti SC / Noto Serif CJK） |
| 打开工具 | Microsoft Word / WPS（可选，仅查看时用） |
| Claude Code | 仅"方式一"需要；技能机制要求 Claude Code 支持 skills |

## 目录结构

```
progress-report-skill/
├── SKILL.md                  # 技能本体：写作规范＋图表规则＋排版规范＋检查清单
├── scripts/
│   ├── make_report_docx.py   # Word 生成脚本模板（python-docx）
│   └── figure_examples.py    # 配图模板：轨迹对比/训练曲线/结构框图/方法示意图
├── examples/
│   └── sample-report.md      # 成品格式示例
├── README.md
└── LICENSE
```

## 自定义

- 改写作规范：编辑 `SKILL.md`
- 改排版：编辑 `scripts/make_report_docx.py` 顶部的 `SIZE / INDENT / CN_FONT / EN_FONT` 等常量

## License

MIT
