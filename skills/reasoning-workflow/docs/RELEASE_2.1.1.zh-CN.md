# Reasoning Workflow 2.1.1：修复与升级说明

2026-10-21 · 原独立修订包记录；main 集成差异见 [MAIN_INTEGRATION.md](MAIN_INTEGRATION.md)。不自动安装。

## 结论

2.1 的短入口、按需加载和通用任务策略保留。这次集中补上五处已复现的执行/校验缺口，增加两个衔接功能，不另造状态引擎，也不把简单问题变成必须登记的工程流程。Ultra 研究正文保持原有内容；这里没有用“增加篇幅”冒充研究能力提升。

项目初衷仍按 GitHub README：从问题和下一行动出发，合理投入，追到实际结果；不固定 SOP、来源数量或 Agent 阵容。README 对照基线为 `zy839971925-zyy/Agent--deep-research-Workflow-Skills`，审查时 commit `7d4b31f37aa95fac1b05003b626b9fccea60abaa`，该独立包生成时没有向仓库提交；随后经用户明确授权集成至 main，当前状态以仓库根 README 为准。

## 五处修复

1. 审查失效追踪：指纹现在覆盖单数、复数引用与传递依赖，包括 relationship 的 `from_ref`/`to_ref`；环路可终止，缺失引用、重复 ID 拒绝通过。修改关系指向的 observation 后，旧审查不能继续领取有效信用。仅跳过 `verification_refs` 的反向审查遍历，避免把 review 自己带回目标；字段本身仍参与目标字节指纹。
2. 跨 lane 交付义务：Question、Action、Mixed 都检查显式 material requirement/acceptance 等义务。状态与 manifest 一致地写 blocked，仍然是未完成，不再因为 Question lane 就判可完整交付。
3. 禁止并行：不再依赖可省略的 `concurrency_group` 标签。parallel/hybrid 下，forbidden 节点必须由实际依赖或 `starts_after` 链与其他节点错开；未知引用和等待环拒绝。合法独立任务仍可并行，串行/有序混合控制例通过。它是调度声明校验，不是已运行的外部调度器。
4. Ultra 方法可达：Ultra 路由必带 `required_reference_ids=["ultra-research"]`，没有 gap tag 也不能漏选。手工删改路由、漏掉必需参考都拒绝；准备入口还检查必需文件确实存在。缺少工具/宿主能力须明确受限或阻塞，不能声称已执行完整 Ultra，也不悄悄降档。
5. 晋升证据：Tier3 的 regression、held-out、baseline、dual-review、rollback 不再只检查字符串非空；需解析存在的宿主证据，检查类型、用途、lesson 范围/内容指纹、current/pass 及文件哈希。dual review 还需独立性证据标签由宿主核实。Tier2 held-out 也补了同一门槛。普通检索仍仅 Tier1；maintenance 的 Tier2/3 仍只是建议，不自动改写 Skill。

## 两项功能完善

### 一步准备，但不代替执行

可选 `scripts/prepare_task.py` 串接 profile 规范化 → 确定性路由 → 必需资源选择 → 本地路径检查；给出本阶段参考、因阶段容量延后的 gap 参考和明确阻塞原因。它不调用外部服务，不授予权限，不假报模型已读取或任务已执行。简单 Light 控制例保持零参考加载；简单任务根本不必生成 profile。

```sh
uv run --no-project --with jsonschema==4.23.0 python scripts/prepare_task.py \
  tests/fixtures/standard_profile.json --signal ultra_requested
```

输出 `task_executed=false`、`authority_granted=false` 是预期边界，不是故障。模型/宿主仍需真正读取参考、执行可用工具、验证和交付。

### 可以诚实交付阶段性结果

manifest 可用 `delivery_kind="partial"`，并提供非空 `remaining_work`、`remaining_obligation_refs` 和 `declared_delivery_ready=false`。未解决的 material requirement/acceptance ID 不能漏报；canonical task 也不能标 closed/ready。文件和状态一致性检查仍照常生效。

`computed_partial_ready=true` 仅表示阶段性交接在结构上可接受；`computed_delivery_ready` 和 `computed_task_complete` 仍为 false。不会因此关闭根目标，也不会自动保存进度或安排重试。保留可用中间结果，和声称最终完成，是两件事。

## 升级办法与兼容边界

- 解压后保留整个 `Reasoning Workflow/`，将根 `SKILL.md` 作为入口；不要只复制脚本或 references。保留旧 2.1 目录作回退。此包没有安装脚本，没有自动连接/改设置。
- 不必迁移无关状态；需要继续的记录使用当前规范化 profile 重新生成 route，不能把旧 route 改一个版本号凑用。
- 指纹依赖闭包变化，受影响旧目标要重新计算指纹并重新审查，不能给旧 review 擅自换 hash 当新审查。
- 旧 manifest 不写 `delivery_kind` 时仍按完整交付处理。此前靠 Question lane 漏检才过关的记录会被挡住；这属于修正，不以删去义务“兼容”。
- 旧 Tier2/3 晋升 resolver 若只接受 `resolver(ref)`，现在必须实现 `resolver(ref, role=..., record=...)`；旧 Tier1 通用证据调用仍兼容。宿主 index 的新字段和证据类型见 [host adapter](../references/host-adapter.md#learning-evidence-admission)。没有可信宿主，不能把自行填写的 JSON 当认证证据。
- 并行组名不建立隔离或时间顺序；原本实际串行的工作应声明 serial 或正确的依赖/等待关系。不会自动重排或执行真实任务。
- 先检查 `SHA256SUMS`，再运行测试。测试会重写 `tests/results/` 的运行回执，因此重跑后的这些文件可能不再等于发布包的原始哈希；这不等于原下载包损坏。

## 实测结果与复现

原版 39 项回归完整保留，新增 30 项；最终组合运行 69 项、0 failure、0 error，其中 38 次真实 CLI 子进程调用。新增覆盖关系端点/传递环、缺失引用、跨 lane 阻塞、partial 误报/漏报、无标签/异组并发绕过、合法串行/独立并发、Ultra 漏资源/篡改 route、晋升证据类型/范围/过期/字节篡改，以及入口到资源衔接。

```sh
uv run --no-project --with jsonschema==4.23.0 python tests/run_all.py
# 如只复查原有39项：
uv run --no-project --with jsonschema==4.23.0 python tests/run_regression.py
# 原审查反例另行重跑（参数由该脚本提供）：
uv run --no-project --with jsonschema==4.23.0 python tests/audit_repro/adversarial_probes.py \
  --skill "$PWD" --output /tmp/workflow-probes.json
```

机器回执见 [测试汇总](../tests/results/summary_2_1_1.json)、[CLI 回执](../tests/results/cli_receipts_2_1_1.json) 和 [原反例修复后结果](../tests/results/original_probes_after.json)。跨模块 bridge 的合法/失败控制、恢复拒绝与宿主边界沿用原套件，新增 entry/partial/晋升 CLI 衔接。

## 仍不能宣称的事

69 项是确定性代码/合成契约测试，不是 69 次模型服从实验。包内六类 cross-task case 仍是协议，不是模型实测。没有第二个独立模型、同模型旧新版盲测、真实外部调度/支付/回滚/持久化集成；不能保证任意模型读完一定执行，不能声称研究正确率、成本或延迟已提升。

文件哈希和证据 index 证明本地字节/绑定，不证明事实、作者身份、独立性或权限。宿主必须认证来源和真实执行。Ultra 在这里的可观察实践是按问题拆分、反例、正向控制、回归和边界检查；没有输出或要求隐藏思维链。

建议下一步是选同一模型/宿主，对短回答、深度调研、文件/代码、协调、恢复和外部行动边界做旧新版成对试验，记录正确完成率、错误完成声明、约束保留和开销。该实验尚未运行，本包未把它写成“已经提升”。
