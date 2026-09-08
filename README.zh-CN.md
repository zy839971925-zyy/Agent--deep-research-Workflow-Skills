<div align="center">

<img src="./skills/reasoning-workflow/assets/icon.svg" width="88" height="88" alt="Reasoning Workflow" />

# Reasoning Workflow

### 在搜索、决策和行动之前，先真正理解问题

一套面向 AI Agent 的通用治理型 Skill：覆盖推理、Deep Research、决策、受控执行、验证，以及受证据门控的工作流学习。

[English](./README.md) · **简体中文**

[30 秒开始](#30-秒开始) · [选择版本](#选择版本) · [怎么使用](#怎么使用) · [深度等级](#深度等级light--ultra) · [工作流怎么思考](#工作流怎么思考) · [仓库结构](#仓库结构)

**[查看 Portable / canonical Skill](./skills/reasoning-workflow/)** · **[查看 Modular 版](./modular/)** · [直接阅读 `SKILL.md`](./skills/reasoning-workflow/SKILL.md)

</div>

---

## 为什么要做这个项目

现在的强 Agent 已经可以搜索、写作、编程、调用工具、分配子 Agent，甚至连续工作很久。越来越难的问题已经不是“它会不会做”，而是：

- 它解决的是不是真正的问题？
- 问题框架本身会不会就是错的？
- 它有没有把 token 和工具调用花在真正决定答案的地方？
- 搜到的内容到底是“相关”，还是能真正支持关键结论？
- 推荐方案是否稳健，还是只要假设稍微变化就会翻转？
- 工具失败到底是工具参数问题、观察问题、状态丢失、计划问题，还是说明整个问题模型都该重建？
- 第二个模型说“同意”，到底算不算独立验证？
- 最后一次工具调用成功了，是否真的意味着任务完成？

Reasoning Workflow 管的就是这一层。

它不会替代 Coding Skill、浏览器、数据分析 Skill、设计 Skill、专业领域 Skill 或具体工具，而是负责决定：**当前究竟要解决什么、应该投入多深、接下来最值得做什么、结果什么时候才算真正闭环。**

目标不是把所有任务都做长，而是让投入与**不确定性、后果和真实决策价值**相匹配。

> **研究应该沿着问题本身的结构前进，而不是沿着用户问题里的关键词前进。**

---

## 它是什么，又不是什么

Reasoning Workflow 是位于 specialist Skills 和工具之上的治理层。它可以调度编程、浏览、数据、设计、连接器、子 Agent 等能力，但不会试图把所有能力都塞进自己。

它**不是**：

- 提示词合集；
- 固定思维链模板；
- 每次必须执行的几十步 SOP；
- “固定查 N 个来源”的 Deep Research 配方；
- 固定多 Agent 组织架构；
- 让 Agent 遇到复杂任务就不断反问用户的理由；
- 权限、安全控制、领域专家或 specialist Skill 的替代品；
- “调用过 Workflow，所以答案一定对”的证明。

它更强调的是：**稳定的语义约束 + 自适应策略。**

对 GPT-5.6 及之后这类更强的模型，不应该把规划写死。模型应该可以依据当前问题状态，自由选择、重排、重复、压缩或跳过策略，只要不破坏核心语义约束。

---

## 30 秒开始

### 支持的 Coding Agent：一条命令安装

如果你使用开放的 `skills` CLI，最省事的跨 Agent 安装方式是：

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill reasoning-workflow
```

它可以把 Skill 安装到 Codex、Claude Code 等支持的 Agent。加 `-g` 可以全局安装，也可以先用 `--list` 看清楚仓库里暴露了哪些 Skill：

```bash
# 先查看，不安装
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --list

# 示例：把 Portable 全局安装到 Codex
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills \
  --skill reasoning-workflow --agent codex -g
```

这是开放 Agent Skills 生态里的便捷安装器，不是 Reasoning Workflow 的强制依赖。下面仍然保留 ChatGPT、Codex、Claude Code 的原生/手动安装方式。

### ChatGPT Skills

如果你的 ChatGPT 工作区支持上传 Skills：

1. 打开 **插件 → Skills**。
2. 选择 **创建 → 从计算机上传**。
3. 上传由 [`skills/reasoning-workflow/`](./skills/reasoning-workflow/) 组成的 Portable Skill 文件夹/压缩包。
4. 安装完成后，直接让 ChatGPT “使用 Reasoning Workflow” 完成任务即可。

如果你自己打包，请确保上传包根目录就是 `SKILL.md`，并保留它旁边的：

```text
references/
families/
schemas/
scripts/
agents/
assets/
```

不要再把整个 GitHub 仓库、测试文件或 README 一起塞进 Skill 安装包。

### Codex

Portable 遵循 Agent Skills 结构。可以直接让 Codex 的 skill installer 从 GitHub 文件夹安装：

```text
$skill-installer install https://github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills/tree/main/skills/reasoning-workflow
```

也可以直接复制到 Codex / Agent Skills 常见目录，例如：

```text
.agents/skills/reasoning-workflow/
```

仓库根目录还保留了 [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json)，用于 Codex Plugin 形式的发现和展示。

### Claude Code

把 Portable Skill 文件夹复制到项目级或用户级 Skills 目录：

```text
# 当前项目
.claude/skills/reasoning-workflow/

# 用户全局
~/.claude/skills/reasoning-workflow/
```

注意：`SKILL.md` 必须位于一个有名字的 Skill 文件夹内，不要直接放成 `.claude/skills/SKILL.md`。

### 其他兼容 Agent Skills 的客户端

核心结构始终相同：

```text
reasoning-workflow/
└── SKILL.md
```

公开的 [Agent Skills 规范](https://agentskills.io/) 规定 `SKILL.md` 是必要入口，scripts / references / assets 都是可选支持资源。不同客户端只是在“去哪里发现这个文件夹”上略有差异。

---

## 选择版本

GitHub `main` 直接公开 Portable 和 Modular 两套正常目录，不用先下载 ZIP 才能看到内部内容。

| 版本 | 位置 | 最适合 | 特点 |
| --- | --- | --- | --- |
| **Portable / canonical** | [`skills/reasoning-workflow/`](./skills/reasoning-workflow/) | 大多数用户；ChatGPT / Codex / Claude；只想装一个总控 Skill | 完整深度门、跨 Family 路由、schema 和可选确定性 runtime helper |
| **Modular** | [`modular/skills/`](./modular/skills/) | 已经有成熟 Skill 路由能力、希望独立组合模块的高级用户 | 六个轻量语义 Skill，不重复 Portable 的 Python/schema runtime |

### 默认选 Portable

Portable 是完整的 Reasoning Workflow，也是 canonical implementation。它包含：

- `SKILL.md` —— 总入口；
- 六个 Family 索引；
- 按需加载的 references；
- Task / state / runtime 的机器可读 schema；
- 少量用于确定性路由和校验的 Python runtime helper；
- OpenAI host metadata、图标和随 Skill 分发的 MIT License。

它不包含单元测试、regression/eval fixtures、benchmark harness、distribution build 工具、本地 build report 或生成的 ZIP。这些材料不属于用户运行 Workflow 所需的公开 Skill 表面。

### Modular：轻量模块版

Modular 直接公开六个独立语义 Skill：

- [`reasoning-core`](./modular/skills/reasoning-core/)
- [`deep-research`](./modular/skills/deep-research/)
- [`decision-analysis`](./modular/skills/decision-analysis/)
- [`execution-control`](./modular/skills/execution-control/)
- [`audit-verification`](./modular/skills/audit-verification/)
- [`workflow-learning`](./modular/skills/workflow-learning/)

每个 Skill 只包含自己负责的 instructions、Family references 和许可证，不复制 Portable 的 schemas / Python runtime。

如果你需要完整 deterministic router、状态校验、execution validator 或 cross-Family governing loop，就用 Portable。

也可以只安装某个 Modular Skill：

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill deep-research
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill decision-analysis
```

---

## 怎么使用

你通常**不需要**写很长的 Prompt。

最重要的是让 Agent 知道：真实目标、关键约束、交付物，以及你是否真的需要指定推理深度。

### 通用任务

```text
使用 Reasoning Workflow 完成这个任务。

目标：[我真正想得到什么]
约束：[范围、截止时间、权限、来源要求、风险边界]
交付物：[答案、建议、代码、报告、文件等]

你自己判断合理深度。
不要因为用了 Workflow 就把一个简单任务工程化。
```

### Deep Research

```text
使用 Reasoning Workflow，Deep 深度调研这个问题：[问题]

研究要围绕决定答案的前提、关系和因果链展开，而不是直接把问题拆成关键词搜索。
区分 frame uncertainty 和 answer uncertainty。
优先寻找真正能改变答案的证据。
只要证据还不能区分多个解释，就不要过早锁定其中一个。
最后给我最有依据的结论、适用边界，以及仍然重要的不确定性。
```

### Ultra Research

```text
使用 Reasoning Workflow Ultra 深度研究：[问题]

额外预算优先投入广泛思考和发现：
必要时重新定义问题、寻找隐藏关系和遗漏变量、探索真正不同的解释和证据生态，
如果当前检索路径开始同质化或被早期关键词锚定，就主动换路线。

不要把 Ultra 的大部分预算浪费在对同一个 claim 反复核验。
关键结论仍然要强验证，但先尽可能找出当前 Max 路线可能根本没有看到的东西。
```

### 做决策

```text
使用 Reasoning Workflow 帮我做这个决策。

目标：[目标]
我现在想到的方案：[A、B……]
约束：[约束]
偏好：[如果明确的话]

先检查是不是还有真正不同、且更好的备选方案被漏掉。
把事实不确定、模型不确定、偏好不确定和方案集不确定分开。
告诉我关键 trade-off、推荐在什么条件范围内仍然成立，以及什么条件会让结论切换。
只有当一个问题的答案真的可能改变决策时才来问我。
```

### 因果 / 系统分析

```text
使用 Reasoning Workflow 分析为什么会出现 [结果]。

不要把时间先后或相关性直接当成因果。
只研究真正可能改变解释的关系：
上游原因、中介、反馈、激励、替代关系、滞后、混杂、反向因果、阈值和竞争机制。
```

### 执行工程任务

```text
使用 Reasoning Workflow 执行 [任务]。

授权范围：[允许修改什么]
必须保留：[不变量]
禁止修改：[边界]

只有真实瓶颈值得并行时才分配 worker。
handoff 要留下证据和状态，不要传一大段聊天记录。
失败后先诊断发生在哪一层，再决定是否重规划。
最后验证的是有效状态，而不只是“最后一个工具调用成功”。
```

### 明确要求保持轻量

```text
使用 Reasoning Workflow，但默认保持 Light；只有发现真正重要的隐藏复杂度时再升级。
```

Workflow 既可以升级，也可以**降级**。调用它不代表自动调用 Ultra。

---

## 深度等级：Light → Ultra

Depth 控制的是**认识问题的野心和总预算**，不是固定的搜索次数、Agent 数、步骤数、reference 数或 token 数。

| 深度 | 适合 | 典型行为 |
| --- | --- | --- |
| **Light** | 稳定、直接、定义清楚的任务 | 最少 framing，直接回答/执行，只做必要检查 |
| **Standard** | 有边界的分析、写作、实现 | 正常推理和验证，少量支持 context |
| **Deep** | 重要不确定性、因果问题、争议证据 | 明确问题模型、竞争解释、更强证据和 challenge |
| **Max** | 在当前研究轨迹内做到最大有用深度 | 把当前 framing / research path 推到有效极限，并对关键结论强验证 |
| **Ultra** | 连“当前研究轨迹是否完整”都值得怀疑的问题 | 大幅增加预算，用于重新 framing、隐藏关系、替代假设、跨域和不同证据生态、missingness / boundary、强综合 |

### Max 和 Ultra 的区别

- **Max：**这条已经很强的路线，还能往多深做？
- **Ultra：**这整条路线，会不会从一开始就漏掉了什么？

Ultra 不是“Max + 更多来源”，而是高预算：

```text
发散
→ 价值剪枝
→ 深入调查
→ 新证据改变模型时重新发散
→ 收敛
```

> **Ultra：大胆扩展，聪明剪枝，选择性强验证。**

Ultra 不自动意味着固定 4 个 Agent、开局写一份巨长计划、每次调用都 max reasoning、穷尽互联网、固定来源配额或 reviewer 投票。

---

## 工作流怎么思考

核心不是线性 checklist，而是一张会被证据不断改写的依赖图：

```text
真实任务 / 目标
      ↓
问题表示与 framing
      ↓
关键前提、约束、关系、机制
      ↓
不确定性与竞争解释
      ↓
证据需求 / 观察 / 推理操作
      ↓
更新问题模型
      ↓
答案或决策
      ↓
获得授权后执行
      ↓
重新观察 + 验证
      ↓
如果现实不符合模型，就重新打开上游状态
```

### 先判断“这是什么问题”，再拆解

一个错误的问题框架，即使拆得再完美也没意义。

如果多个 materially different representations 都合理，Workflow 可以暂时保留多个表示，不急着坍缩到唯一框架。之后从最粗、但足以暴露关键依赖的粒度开始，只细化真正卡住答案的分支。

### Search 在 evidence need 之后

```text
problem graph
→ 不确定前提 / causal edge
→ evidence need
→ 想看到什么 observation
→ 哪个 evidence surface 最能观察到它
→ observation
→ model update
→ 下一项真正决定答案的不确定性
```

搜索词只是 evidence need 的压缩表达，不是研究计划本身。

### 深度不是重复

如果继续“想”已经无法改变：

- problem model；
- live hypotheses；
- pivotal uncertainty；
- answer boundary；

就不应该沿同一条逻辑继续烧 token，而应该更换问题表示、推理 operator、证据路线或抽象层级。

---

## 六个 Family

六个 Family 是一套 governing system 的不同路由，不是六个必走阶段。

| Family | 主要负责 | 典型触发 |
| --- | --- | --- |
| **Core Reasoning** | framing、问题表示、分解、关系、假设、解释 | 所有 substantive task，默认从轻量开始 |
| **Deep Research** | orientation、evidence need、retrieval、provenance、因果/系统不确定、forecast、Ultra | 需要真实证据或 frame 本身不稳定 |
| **Decision Analysis** | 备选方案生成、trade-off、偏好、robustness、机会成本、推荐 | 选择、优先级、资源配置 |
| **Execution Control** | 计划、授权、delegation、状态、checkpoint/recovery、replay safety | 持久工作或外部 side effect |
| **Audit / Verification** | contract check、独立 review、evaluator validity、effectiveness | 重要验证或 closure 风险 |
| **Workflow Learning** | CAPA、经验复用、negative transfer 控制、eval-gated promotion | 只在维护平面 |

普通问答可能只需要 Core Reasoning + 很轻的 verification。研究任务再加入 Deep Research。真正持久的工程修改才进入 Execution Control。Workflow Learning 不应该塞进普通用户任务的 context。

---

## 三种 gate 不要混在一起

Reasoning Workflow 明确区分三种不同性质的 gate：

1. **Source gate** —— 这个来源、文件、dataset、观察或私有输入，适不适合回答当前问题？
2. **Evidence gate** —— 我实际读到的材料，真的支持当前 claim、范围、机制或决策依赖吗？
3. **Action gate** —— 这个外部动作有授权吗？在范围内吗？可逆性和控制条件够吗？

这不是强制三步流程，它们发生在不同阶段。

“来源可信”不等于“它支持当前结论”；“证据很强”也绝不等于“Agent 获得了行动权限”。

---

## Delegation：按瓶颈招人，而不是按 Agent 数量招人

Reasoning Workflow 不认为“Agent 越多越强”。只有 branch 足够可分离，而且收益明显大于协调成本时，并行才有意义。

比较适合 delegation 的真实瓶颈包括：

- 需要独立研究或完全不同的 evidence ecosystem；
- 需要另一种语言、司法辖区或专业方法；
- 需要 reproduction / adversarial verification；
- 可以明确隔离的执行分支；
- 某一类 repeated rework 需要专门 owner。

handoff 之前应给 worker 一个非常紧凑的 contract：

```text
job
allowed inputs / sources
judgment boundary
acceptance criteria
output contract
forbidden actions
uncertainty to preserve
```

worker 返回时，交付的是“可继续工作的状态包”，而不是几千 token 的聊天记录：

```text
task | status | material output | evidence/source locators
| scope 内已经做出的 decision | unresolved uncertainty
| failed routes | state/items affected | next owner / next safe action
```

如果多个 Agent 共享 workspace，真正持久的信息应该放在 evidence/state/artifact 中。聊天 summary 只是视图，不应该成为 canonical reality。

---

## Progressive Context：文件多，不代表模型读得多

需要分清三件事：

1. GitHub 仓库里有多少文件；
2. 实际安装的 Skill 有多少文件；
3. 当前 turn 真正进入模型 context 的内容有多少。

Reasoning Workflow 设计的加载方式是：

```text
metadata
→ SKILL.md
→ Task Profile
→ 当前 Family
→ 当前 unresolved gap
→ 通常只加载 1–3 个相关 reference
→ gap 改变后释放 / 更换 context
```

`Related` 只是导航，不代表自动加载。

Portable 里保留几十个小文件，是为了让职责清楚地拆开，而不是让 Agent 一次性全部读进去。schema 和 Python helper 大多数时候应该由工具执行，而不是把源码塞进 prompt。

---

## 为什么还保留 Python 和 schema？

公开 Skill 不携带开发用 tests / evals / build harness。保留的 Python 和 JSON 属于 Workflow 本身的可选机器能力：

- Task Profile / Family 的确定性路由；
- progressive reference selection；
- semantic state 和 typed dependency 校验；
- execution plan / schedule / checkpoint / worker 校验；
- delivery / event / raw-lineage integrity；
- dual verification record 校验；
- Workflow Learning 的 promotion gate 和选择性 retrieval。

如果 host 本身不能执行本地 Python，Workflow 仍然可以只靠语义规则工作；但是 Agent 不能假装“机器 validator 已经执行”。

Python 唯一额外依赖写在 [`scripts/requirements.txt`](./skills/reasoning-workflow/scripts/requirements.txt) 中：用于 JSON Schema 校验的 `jsonschema`。

---

## 模型适配

当前设计主要面向 GPT-5.6 及之后这类 reasoning agent，同时避免给每个模型写一套分支。

Workflow 关注的是运行时真正拥有什么能力：

- 能否保留跨 turn 的有效 reasoning state；
- 能否做 context compaction；
- 是否有真正独立的 worker / subagent；
- 是否能动态调整 reasoning effort；
- 是否能把机械筛选、去重、聚合移到 deterministic code；
- 工具调用和状态持久化是否可靠。

强模型得到更多 outcome / invariant 约束，更少无意义 procedural scaffolding；能力弱或 adherence 不稳定的 runtime 才增加局部结构。

**Workflow 的脚手架本身也是可伸缩资源。**

Ultra 也不意味着每次模型调用都用最高 compute。贵的 reasoning 应该花在发现新结构、解决决定性不确定和复杂综合上；机械工作尽量交给便宜模型或确定性代码。

---

## Controlled Learning

正常用户任务不会自动修改 canonical Workflow。

可复用规则应该是**通过证据挣出来的，而不是一次运行看起来很聪明就写进去的**。

维护平面区分三种经验：

- clean success → strategy lesson；
- failure → recovery → success → recovery lesson；
- 成功但过程浪费 → optimization lesson。

从过去检索出的经验也不是自动适用：先检查 applicability、anti-condition 和 negative transfer，再决定：

```text
use | adapt | ignore
```

self-reflection 本身只能产生 candidate，不能单独完成 promotion。

---

## 仓库结构

公开仓库只保留：**工作流本身 + 直接支持其运行的必要 runtime 文件 + 用户发现、安装和理解项目所需的文档/元数据。**

```text
.
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CONTRIBUTING.md
├── PRIVACY.md
├── TERMS.md
├── .codex-plugin/
│   └── plugin.json
│
├── skills/
│   └── reasoning-workflow/          # Portable + canonical
│       ├── SKILL.md                 # 总入口
│       ├── routing-index.json       # progressive routing metadata
│       ├── families/                # 六个 Family 索引
│       ├── references/              # 按需加载的推理模块
│       ├── schemas/                 # runtime semantic contracts
│       ├── scripts/                 # 只保留 runtime routing / validators
│       ├── agents/                  # OpenAI host metadata
│       └── assets/                  # icon
│
└── modular/
    ├── README.md
    └── skills/
        ├── reasoning-core/
        ├── deep-research/
        ├── decision-analysis/
        ├── execution-control/
        ├── audit-verification/
        └── workflow-learning/
```

### 公开仓库的边界

仓库不包含那些对理解、安装或运行 Reasoning Workflow 没有直接作用的开发材料：私有 test/eval harness、benchmark fixtures、生成的 distribution 压缩包、构建报告、distribution tooling，以及没有 runtime consumer 的 contracts。

这样 GitHub 公开面保持为“工作流本身”，而不是作者的完整工程工作区。

### 剩下这些文件为什么存在？

可以分成四类：

| 类别 | 为什么保留 |
| --- | --- |
| `SKILL.md` / Families / references | 真正的 reasoning / workflow knowledge |
| schemas + runtime scripts | 可选的确定性 routing / state / execution / verification enforcement |
| Modular Skills | 让高级用户可以独立浏览和组合六个 Family |
| README / LICENSE / plugin metadata | 项目发现、安装、许可证和 host integration |

Portable 和 Modular 会有少量语义文字重复，因为它们都应该能直接在 GitHub 上阅读和安装；deterministic runtime 则只在 Portable 中保留一份。

---

## 核心设计原则

- **Search 在 reasoning 之后。**
- **Universal entry 不等于 universal full execution。**
- **严谨不等于仪式感。**
- **framing 不稳定时，先竞争 problem representation，再 decomposition。**
- **Reasoning depth 不等于把同一条逻辑重复更久。**
- **来源数量不等于证据独立。**
- **reviewer 数量不等于 verification independence。**
- **Declared state 是输入，effective state 才是计算出来的当前真相。**
- **Plan semantics 不因串行/并行调度而改变。**
- **按 bottleneck delegation，而不是按 Agent quota。**
- **handoff 传 evidence/state，不传 transcript volume。**
- **强证据绝不自动创造行动权限。**
- **verification credit 只属于真正被验证的那个 state/content。**
- **Learning 是受控经验复用，不是自动 self-editing。**
- **漂亮的最终答案不是遵守 Workflow 的证明。**
- **Ultra：大胆扩展，聪明剪枝，选择性强验证。**

---

## 兼容性和公开参考

Reasoning Workflow 遵循开放的 Agent Skills 基本结构：`SKILL.md` 作为入口，按需附带 references、scripts 和 assets。

可以参考：

- [Agent Skills specification](https://agentskills.io/)
- [OpenAI Plugins](https://github.com/openai/plugins)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [Claude Code Skills 文档](https://code.claude.com/docs/zh-CN/skills)

这里最重要的不是照抄某个仓库的目录，而是遵守 progressive disclosure：入口保持高信号，条件性知识放进对应 reference，只有真正需要时才加载。

---

## 验证状态

确定性检查覆盖路由、语义状态传播、授权、恢复、交付闭合、审查记录和受控学习；开发测试在可安装的公开目录之外运行

真实模型的 Task Profile 分类、Skill 触发准确率与召回率、跨模型路由、同条件 Deep Research 质量、token 与延迟节省、双重审查错误降低、长期学习效果及外部 Deep Research benchmark 仍未验证

代码检查通过不代表真实 Agent 行为效果已经得到证明

---

## 局限

Reasoning Workflow 可以提高过程质量，但它不会提供魔法保证：

- 模型依然可能理解错指令；
- 来源依然可能错；
- reviewer 可能和 solver 共享同一个盲区；
- schema 能证明结构一致，却不能证明现实世界事实一定正确；
- 不同 host 的 tool/runtime 能力并不一样；
- 模型和产品行为也会不断变化。

对于高后果任务，最终标准仍然应该是：与风险相匹配的证据、真正有价值的独立验证、明确权限，以及必要的人类/领域专家 review。

---

## Contributing

Canonical implementation 是 [`skills/reasoning-workflow/`](./skills/reasoning-workflow/)。Modular 是同一套语义的轻量投影。

任何修改都优先回答一个问题：**到底解决了什么真实 failure mode？**

不要为了显得“更完整”轻易新增 Family、schema、固定 workflow stage、mandatory checklist、Agent 数、搜索配额或 review 层。

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## License

使用 [MIT License](./LICENSE) 开源。

Reasoning Workflow 对外保持无版本号品牌。仓库持续在原项目上演进；只有在兼容性或机器完整性确实需要时，内部 plugin/schema 字段才保留机器 revision。
