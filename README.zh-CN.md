<div align="center">
<img src="skills/reasoning-workflow/assets/icon.svg" width="88" height="88" alt="Reasoning Workflow" />

# Reasoning Workflow

理解问题，选择下一步，验证实际结果。

[English](README.md) · 简体中文

[从这里开始](skills/reasoning-workflow/SKILL.md) · [下载 2.1.1](dist/reasoning-workflow-2.1.1.zip) · [升级说明](skills/reasoning-workflow/docs/RELEASE_2.1.1.zh-CN.md)
</div>

## 项目初衷

Reasoning Workflow 是面向 AI Agent 的泛用推理与执行框架，深度调研仍是它的强项。它帮助模型弄清真正要达成的结果，找到影响结论的关键不确定性或执行瓶颈，选择合适的方法，并区分“有用的阶段成果”和“任务已经完成”。

项目的出发点没有变：调研应顺着问题的结构展开，而不只是搜索提示词中的几个词。下一步可能是计算、核查来源、调用专门的 Skill、执行已授权的操作、提出一个关键问题，也可能就是直接回答。流程更多，不代表工作更好。

它不规定固定 SOP、来源配额、Agent 阵容或必写的长计划。简单任务保持轻量；参考文档、Schema、持久状态和委派只在当前工作确实需要时启用。思考更深入，不意味着权限更多。

## 能帮助什么

- 调研：问题重构、竞争假设、原始证据、来源与主张的对应、缺失信息、反例和关键结论核验。
- 决策：备选方案、约束、取舍、敏感性，以及说明何时应该改变选择的建议。
- 文件与代码：可用成品、明确的验收条件、测试和交付检查。
- 长期工作：依赖、统一状态、受控委派、中断恢复和诚实的阶段性交接。
- 外部行动：分清准备、授权、执行回执和实际结果，避免把“请求已提交”当作“事情已完成”。

六个按需启用的 Family 提供支持：Core Reasoning、Deep Research、Decision Analysis、Execution Control、Audit & Verification、Workflow Learning。学习属于明确的维护场景，不在普通任务中悄悄改写 Skill。

它不能替代模型能力、领域知识、工具、权限或可信宿主，也不要求展示隐藏思维链。仅仅安装 Skill，不足以让任意 Agent 变得可靠。

## 安装完整 Skill

当前规范版本位于 [`skills/reasoning-workflow/`](skills/reasoning-workflow/)，给模型的入口是 [`SKILL.md`](skills/reasoning-workflow/SKILL.md)。

1. 克隆仓库，或下载并解压完整的 [2.1.1 压缩包](dist/reasoning-workflow-2.1.1.zip)。
2. 将整个 `reasoning-workflow` 目录放入宿主识别的 Skill 目录。Codex 用户级安装常用 `~/.agents/skills/reasoning-workflow/`；其他宿主以其实际文档为准。
3. 在宿主中启用或选中这个 Skill，让模型从 `SKILL.md` 开始，只在需要时读取链接的参考文档，不必把整套资料一次塞进上下文。
4. Python 辅助工具是可选的。使用时准备 Python 3.10+ 和下方依赖；仓库 CI 使用 Python 3.12。工具能力和行动授权仍须由宿主单独提供。

不要只复制 `SKILL.md`：它依赖同目录下的 references、schemas、scripts 和 templates。安装不会自动连接账号，也不会自动拦截工具调用。

克隆与隔离 Python 环境示例：

```sh
git clone https://github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills.git
cd Agent--deep-research-Workflow-Skills
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/reasoning-workflow/scripts/requirements.txt
```

偏好多项独立 Skill 的宿主仍可使用 [Modular 版](modular/README.md)。共享参考内容保持同步；Python 路由与 runtime 辅助工具只放在规范版，不在六个 Modular Skill 中重复。需要完整 2.1.1 行为时，使用规范版。

## 快速开始

普通请求不需要先写 JSON profile：

> 使用 Reasoning Workflow。比较这个问题的实际方案，查清足以改变建议的不确定性，交付一个可用结果。投入与问题相称，不在未经授权时采取外部行动。

要试验确定性路由，可以在仓库根目录运行内置合成示例：

```sh
python skills/reasoning-workflow/scripts/prepare_task.py \
  skills/reasoning-workflow/tests/fixtures/standard_profile.json

python skills/reasoning-workflow/scripts/prepare_task.py \
  skills/reasoning-workflow/tests/fixtures/standard_profile.json \
  --signal ultra_requested
```

`prepare_task.py` 串接 profile 规范化、路由生成、本阶段参考选择和必需文件检查，并列出延后处理的 gap 参考。预期输出包含 `status="prepared"`、`task_executed=false`、`authority_granted=false`。它只是准备任务，不运行模型、不替模型阅读文档，也不执行外部工具。简单 Light 任务可以零参考加载。

## 深度、Ultra 与能力不足

Light → Standard → Deep → Max → Ultra 根据不确定性、后果和进一步工作的价值调整投入。研究深度、核验、自治和持久化是分开的维度，不是一个全局“什么都加码”的开关。

Ultra 为重新建模、关系发现、竞争解释、正交证据路线、边界分析和关键核验留出更多空间。它不等于更长的答案、固定搜索次数、自动并行或无限 Agent。即使没有 `ultra` gap tag，路由也必须选中 Ultra 方法；参考预算会容纳必需的方法和控制。

缺工具、独立核验者、文件或可信宿主集成时，应说明具体缺什么。能独立推进的部分继续做，但不能悄悄降档后声称已完整执行 Ultra。详见 [Ultra research](skills/reasoning-workflow/references/ultra-research.md) 和 [model adaptation](skills/reasoning-workflow/references/model-adaptation.md)。

## 执行与阶段性交付

指导文档和本地校验器不是已接入的外部执行器。可选的 [harness integration](skills/reasoning-workflow/references/harness-integration.md) 必须由可信宿主实际调用，才能在工具边界生效。[Host adapter 契约](skills/reasoning-workflow/references/host-adapter.md) 说明身份、实时授权、证据准入和恢复责任。Worker 自填的 JSON 标签或文件哈希，不能证明这些事实。

工作未完成时，delivery manifest 可以声明 `delivery_kind="partial"`，保留剩余工作与未解决义务引用；根任务不能标成 closed 或 delivery-ready。`computed_partial_ready=true` 仅表示阶段性交接可接受，不代表完整完成，也不自动保存断点、安排后续或重试外部操作。Question、Action、Mixed 三种 lane 中，未满足的关键要求都仍然阻止完整交付。

## 2.1.1 的变化

- 审查指纹覆盖关系端点和传递依赖，关键内容变化后旧审查失效。
- 交付义务跨 lane 生效，不能把阻塞工作包装成已完成的 Question 任务。
- 禁止并行不再依赖可省略或更换的组名，必须有实际先后关系。
- 显式 Ultra 必须加载对应方法；资源缺失时明确阻塞，不再静默漏选。
- Tier 2/3 晋升检查证据的类型、适用对象和通过状态，而非只接受非空引用字符串。
- 一步准备与显式 partial 交接改善衔接，不增加一套强制状态引擎。

本次 main 集成还保留了仓库既有的 profile/index 指纹、自定义 index CLI、已核验前置节点 ledger、外部资源锁隔离、成品路径要求和审查分歧检查。测试 fixture 仅在更严格的 canonical artifact/证据接口需要时适配。详见 [main 集成说明](skills/reasoning-workflow/docs/MAIN_INTEGRATION.md)、[变更记录](skills/reasoning-workflow/CHANGELOG.md) 和 [升级指南](skills/reasoning-workflow/UPGRADE.md)。

升级前保留备份。旧路由应按当前规范化 profile/index 重新生成；目标指纹改变后需要真实的新审查，不是给旧 review 换个 hash。旧 manifest 不写 `delivery_kind` 仍表示完整交付；Tier 2/3 resolver 需要支持按角色核验的接口。不要靠删除未完成义务来“兼容”。

## 复现检查

安装上方 Python 依赖后，从仓库根目录运行：

```sh
python -m unittest discover -s tests -v
python skills/reasoning-workflow/tests/run_all.py
python -m pip install markdown==3.7
python skills/reasoning-workflow/tests/check_package.py
```

此次 main 集成通过了 34 项公开宿主契约测试，以及包内 69 项测试（39 项基线、30 项补丁测试，含 38 次真实 CLI 调用）。包结构、本地链接、Schema 和归档另有检查。测试会重新生成本地回执文件，下载包的哈希应先于测试核对；分发哈希见 [`dist/SHA256SUMS`](dist/SHA256SUMS)。

这些是确定性代码、合成契约和跨模块测试，不是 103 次模型试验。尚未完成多模型盲测，也没有认证真实支付、外部执行器、持久恢复或回滚集成。六类跨任务案例是评测协议，不是模型成功率数据。不能保证每个模型读完都会遵循，也不能据此声称推理质量、延迟或成本已经改善。

## 仓库与署名

- [`skills/reasoning-workflow/`](skills/reasoning-workflow/)：完整规范 Skill、源码、参考、合成测试和迁移说明。
- [`modular/`](modular/)：六项聚焦的指导型 Skill，共享相关参考。
- [`tests/`](tests/)：公开合成宿主与仓库集成契约。
- [`dist/`](dist/)：完整安装包与哈希，不依赖另外创建 GitHub release。
- [`CONTRIBUTING.md`](CONTRIBUTING.md)、[`PRIVACY.md`](PRIVACY.md)、[`TERMS.md`](TERMS.md)：贡献及项目政策。

由 [折鸢 / zy839971925-zyy](https://github.com/zy839971925-zyy) 创建和维护，按 [MIT License](LICENSE) 开源。项目从问题驱动的深度调研发展为泛用执行框架，保留最初对问题建模、合理投入、证据和实际闭环的强调。[`meta/`](skills/reasoning-workflow/meta/) 保留历史项目介绍供追溯，不是当前安装说明。
