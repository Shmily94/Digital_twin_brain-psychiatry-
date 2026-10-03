# 图表复现包 — 操作指引

本包的目标只有一个：**让文章里每一张图、每一个统计数字，都能从数据一路追到产生它的代码。**

基准是 `revision/text/submission/` 里的最终交稿文件，不是任何中间版本：

| 交稿件 | 内容 |
|---|---|
| `290926NatMed_Manuscript_FINAL.docx` | 正文，内嵌 Fig. 1–5 |
| `290926Supplementary_Information_FINAL.docx` | SI，内含 Fig. S1–S14 |
| `ExtendedData/Extended_Data_Fig_1–9` | Extended Data 图 |
| `290926Suppl.Table_FINAL.xlsx` | Table S1–S24 |

这三份文件的副本存放在 `04_figures/_final_deliverables/`，作为**基准物**（reference of
record）——包里所有比对都以它们为准。

## 两条绝对规则

1. **本包内的所有文件都是复制品。** 建包过程没有修改、移动或删除你原有目录中的任何一个
   文件。`MANIFEST.csv` 逐行记录了每个文件的来源绝对路径、字节数与 SHA256，可随时核对。
2. **`04_figures/` 是只读基准。** 里面的数据文件是验证统计代码时的比对对象。任何脚本都
   不应往里写——重跑时输出到临时目录再比对。

## 目录结构

```
reproducibility_package/
├── README_zh.md / README_en.md      本指引
├── PROVENANCE.csv                   全链路溯源总表（见下）
├── MANIFEST.csv                     1190 个文件的来源 + SHA256
├── OPEN_QUESTIONS.md                需要你确认的遗留项
├── VERIFICATION_REPORT.md           重跑验证结果
├── 00_environment/                  三套环境说明 + 依赖清单 + 自检脚本
├── 01_model_dtb/                    DTB 模型引擎（纯代码，5.6 MB）
├── 02_model_benchmark/              SAR / rWW / Hopf 三个基准模型（代码）
│                                    注：基准模型的拟合结果数据在 04_figures/Model_Benchmark/
├── 03_analysis/                     统计分析代码（本次新增，见「统计层」）
│   ├── 00_upstream_matlab_pipeline/ 原投稿的 MATLAB 流程（CPM 识别、模型输入、仿真后处理）
│   ├── fig1_2/ fig3/ fig4/ fig5/    按图归档的可运行统计脚本
│   ├── extended_data/ supplementary/
├── 04_figures/                      作图层：脚本 + 作图数据 + 最终渲染（只读基准）
│   ├── fig.1 … fig.5, supp_*/       镜像原图树结构
│   ├── _recovered_session_b194cd74/ 5 个从会话工作目录恢复的最终脚本（关键，见下）
│   ├── _final_deliverables/         交稿件副本 + ExtendedData 成品
│   ├── figA4_kit.py, fig_color/     共享排版与配色模块
├── 05_tables/                       Supplementary Tables 生成代码
├── 06_upstream_inputs/              作图脚本需要的图树外上游数据（38.5 MB）
├── recovered/                       原始 cell 代码逐字存档（审计用）
├── docs/                            恢复协议、各轨道溯源表、图-脚本映射
└── tools/retarget_paths.py          绝对路径重定向工具（必须先跑，见下）
```

## 先做这两步

### 第 1 步：检查环境

```bash
cd reproducibility_package
python 00_environment/check_environment.py
```

需要 Python 3.11 + numpy / scipy / pandas / matplotlib / statsmodels /
scikit-learn / Pillow / python-pptx / openpyxl。缺什么按
`00_environment/requirements_figures.txt` 装。

### 第 2 步：重定向绝对路径

所有作图脚本里都硬编码了作者机器上的绝对路径：

```python
FIGDIR = "/Users/yunman/Desktop/submission/revision/text/figures"
```

包里的脚本是**与产出交稿图完全字节一致的副本**，所以这些路径仍指向原机器。先看一眼会改
什么，再执行：

```bash
python tools/retarget_paths.py            # 干跑，只报告
python tools/retarget_paths.py --apply    # 实际改写（45 个脚本），可重复执行
python tools/retarget_paths.py --restore   # 从 .orig 备份还原为字节一致状态
```

这个工具**只改两个路径字面量**，不动任何统计量、参数或绘图指令。每个文件首次改写前会存
一份 `.orig` 备份，所以字节一致的原始状态永远可恢复。

> 若你就在本机、且原目录 `revision/text/figures` 仍在原处，则**不必**重定向——副本脚本
> 会直接读原目录，一样能跑。重定向是为了把包交给别人或换机器时用。

## 作图层：图 → 脚本

`docs/FIG_SCRIPT_MAP_final.csv` 是逐图的对应表，28 张图里 26 张已锁定脚本。对应关系不是
按文件名猜的，而是用哈希/像素比对确定的，证据写在表的 `identification_evidence` 列：

- **Fig. 3 / Fig. 4 / Fig. 5**：稿件内嵌 PNG 与脚本输出 PNG 的 **SHA256 完全一致**。
- **Extended Data Fig. 1–9**：ED 的 png/pdf 与恢复目录中的副本 SHA256 完全一致。
- **Fig. S1**：SI 内嵌图与 `figS1_new_image1.png` SHA256 完全一致。
- 其余用感知哈希 + 高分辨率 RMS 判定，表中给出与次优候选的距离。

### 三件必须知道的事

**（一）有 5 个最终脚本不在原图树里。**
它们在最后一次分析会话的工作目录中，已恢复为真实 `.py` 放进
`04_figures/_recovered_session_b194cd74/`：

| 脚本 | 产出 |
|---|---|
| `fig5_main_A4_np12_adj.py` | 正文 Fig. 5 |
| `figS15_models_all_v4.py` | Extended Data Fig. 6 |
| `ed5_wbdrug.py` | Extended Data Fig. 5 |
| `ed7_finger.py` | Extended Data Fig. 7 |
| `figS1_stratify_k2.py` | Supplementary Fig. S1 |

**只打包 `revision/text/figures` 的话，这 5 张图是复现不出来的。**

**（二）Extended Data 图有一道缩放工序。**
`Extended_Data_Fig_*.png` 不是脚本的直接输出，而是把 A4 渲染图缩放到 **1270 px 宽**得到
的：

```python
from PIL import Image
im = Image.open('figS_wbdrug_A4_nocaption.png')
im.resize((1270, int(1270 * im.size[1] / im.size[0])), Image.LANCZOS).save(
    'ExtendedData/Extended_Data_Fig_5.png')
```

**（三）Fig. 1 与 Fig. 2 的整图是 PowerPoint 拼版。**
面板本身由脚本生成（`fig.1/fig1_v4.py`、`fig.2/fig2.py` → `panels/`），但整页由
`fig.1/fig1_editable.pptx` 拼成，所以整图没有"一条命令产出"的路径。面板级是可复现的。

### 重跑一张图

```bash
cd 04_figures/fig.4
python fig4_main_A4.py                  # 输出 png + pdf + pptx（含可编辑文字层）
python fig4_main_A4.py --no-caption     # 不带图注的版本
```

每个脚本同时写出一个 `*_caption_values.csv`，里面是图注中所有统计量的机器可读版本——核对
图注数字时用这个，不要手抄。

## 统计层：作图数据 → 统计代码

这是本次补齐的部分，也是原先最大的缺口。

**原先的状态：** 图树下 162 个作图数据文件，作图脚本对它们**只读不写**；仓库里没有任何
脚本生成它们。这些分析（组间比较、配对检验、置换检验零分布、嵌套模型增量、交叉验证）当
初是交互式跑的，从未落成文件。

**现在的做法：** 这些交互 cell 逐字保存在平台执行记录里，可检索。162 个文件中 156 个在开
工前已确认能定位到候选生成 cell。恢复方法固定在
`docs/RECOVERY_PROTOCOL.md`（这是约束性文档，不是建议），要点：

- 用执行记录检索写入该文件的 cell（`to_csv` / `to_excel` / `savemat`）。
- 同一文件被多次写过时，**按证据判定**而非按时间取最新：读包里实际存在的那份数据文件，
  保留能产出其确切列名、行数与分组的那个 cell。
- 每个数据文件交付三样东西：
  1. `03_analysis/<轨道>/<NN>_<文件名>.py` — 整理后的可运行脚本，文件头注明计算内容、输
     入、输出、所用统计检验、是否可本机运行、以及恢复自哪个 cell；
  2. `recovered/<轨道>/<文件名>__cell_<id>.py` — 原始 cell 逐字存档（审计副本，可与整理版
     对比确认只改了呈现方式）；
  3. `docs/provenance_<轨道>.csv` — 逐文件溯源行。

**整理的边界：** 只加文件头、显式化导入与路径、去掉交互调试痕迹。**统计内容与原 cell 数值
完全一致**——同样的检验、同样的协变量、同样的多重比较校正、同样的随机种子。原 cell 没固定
种子的（置换、交叉验证、bootstrap），**不补种子**，而是在文件头注明"原始运行未固定种子"，
并说明重跑只能在 Monte Carlo 误差内复现。

### 哪些能本机重跑，哪些不能

相当一部分分析建立在 DTB 群体仿真的输出之上（3 M / 10 M / 100 M / 1 B 神经元）。那些中间
文件体积过大、且产自 GPU 集群，**不在本包内**。这类脚本在溯源表中标为
`local_runnable=no`，并在 `notes` 列点名所需的上游文件及其目录。这是完整且可接受的答案；
用一个小规模替代品冒充原始输入不是。

## 全链路溯源表

`PROVENANCE.csv` 是总表，一行一条链路：

```
图/表 → 面板 → 最终作图脚本 → 作图数据文件 → 统计脚本 → 原始 cell 存档
      → 上游数据来源 → 本机可重跑状态 → 验证结果
```

分轨道的明细在 `docs/provenance_fig1_2.csv`、`provenance_fig3.csv`、
`provenance_fig4.csv`、`provenance_fig5.csv`、`provenance_tables.csv`。

## 验证结果

完整报告见 `VERIFICATION_REPORT.md`。要点：

**端到端重跑（在包内、用包内数据）：**

- **Fig. 3 / Fig. 4 / Fig. 5：与稿件内嵌图 SHA256 完全一致。**
- **9 张 Extended Data 图的 A4 渲染：全部与原渲染 SHA256 一致。** 最终 1270px 成品 3/9
  完全一致，其余 6 张只差在缩放实现（RMS 3.5–4.2，满量程 255），源渲染一致故数值一致。

**统计层 274 个数据文件/表格：**

| 项 | 数量 |
|---|---|
| 定位到产出 cell | 247 |
| 未定位（NOT_FOUND） | 27 |
| 写出整理版脚本 | 228 |
| 重跑一致（match） | 176 |
| 输入不在包内（not_run） | 74 |
| 部分一致（partial） | 14 |
| 重跑不一致（mismatch） | 10 |

27 个 NOT_FOUND 不是同一类缺口：7 个是集群 benchmark 拟合与二维电导扫描的产物（全代码树
里只被读、从未被写，模型代码在 `02_model_benchmark/`）；7 个补充表格是手工编制（样本描
述、条目清单、ROI 表），本就不该有代码；13 个补充表格是转述已有溯源链的作图数据文件，已
逐格比对。

10 个 mismatch 是**关于交稿材料本身的发现**，不是恢复工作的缺陷——其中 4 个 Fig. 3 表格
在生成后被原地手工编辑过，Extended Data Fig. 2 的 Oldham 表相对其输入已过期。

## 需要你确认的事

见 `OPEN_QUESTIONS.md`，共 15 条，逐条写明已知事实、候选选项、以及我当下的处置。

**第 1–4 条涉及交稿材料里的数字，建议投稿前处理：**

1. **Extended Data Fig. 2 相对其输入已过期。** 临床氯胺酮两条序列：图上是 r = 0.116（全
   部 36 人）与 0.271（MDD 22 人），用当前输入算得 0.057 与 0.237。结论不变（两者都与 0
   无差异），但印在图上的数字与随图提供的输入文件不符。
2. **Table S23 与包内分析不符。** 该表在执行记录中无任何产出 cell；与
   `TableS26_group_effect_motion_adjustment_corrected_n288.csv` 比对，Simulated-NP 值相
   差**逾两倍**，且两个最大效应的排序反转。这不是四舍五入问题。
3. **Table S17 图注的稀疏格计数有误。** 图注称"三个格子人数少于 5"，实际是 **12 格中的
   6 格**（已从 `fig4_subject_level_n288.csv` 核实）。检验统计量不受影响，只需改这句话。
4. **Table S24 无法一条命令重建**：交稿表是构建脚本输出之后又在工作簿上直接施加了 347
   处数字格式改写与 29 处实质修正的结果。

第 5–10 条是审稿人可能追问的溯源缺口（含 `P_SAR` / `P_rWW` 两个基准预测剖面在全库中只被
使用、从未被赋值）；第 11–15 条是版本与收尾事项（两张图我无法从图像区分版本、Fig. S5 缺脚本、
6 个我无法还原的文件、ED 缩放路径、7 个未对应最终图的 supp 目录）。
