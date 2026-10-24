# Reasoning Workflow — 实际测试报告

## 3.1.0 路由与工作深度候选验证（2026-10-24）

- 34 项仓库级宿主契约测试：通过；使用隔离环境中的 `jsonschema==4.23.0` 与 `markdown==3.8.2`。
- 75 项 Portable 回归测试：通过，0 failure、0 error；包含 39 项保留基线、36 项新增回归检查和 38 次真实 CLI 子进程调用。测试摘要明确记录 `model_evaluated=false`。
- 路由行为协议新增 V3-RD，跨任务案例新增 `v3_context_led_research_lens_and_depth`；合计 19 个 V3 场景、24 个跨任务案例。它们是静态协议/夹具，不是模型执行结果。
- 编译检查：`python -m compileall -q skills/reasoning-workflow/scripts skills/reasoning-workflow/tests` 通过；`git diff --check` 通过。
- 静态包检查：78 个 Markdown、353 个本地 Markdown 链接、13 个锚点、29 个 Python AST、54 个 JSON、14 个 JSON Schema、30 个路由引用；169 个包校验项通过。3.1.0 ZIP 与源码 170 个文件逐项一致，归档内 SHA-256 检查通过；dist 中 2.1.1、3.0.0、3.0.1、3.1.0 四个 ZIP 的 SHA-256 均通过。
- 候选规则按场景推断现实/经验、工程/架构或混合证据路径；默认保留宿主选择的模型，自动选择工作流深度，明确的用户深度要求优先。深度不代表模型切换。没有执行真实模型对照或盲评，故不声称模型服从率或调研质量提升。

复现：

```sh
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python skills/reasoning-workflow/tests/run_all.py
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python -m unittest discover -s tests -v
python -m compileall -q skills/reasoning-workflow/scripts skills/reasoning-workflow/tests
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python skills/reasoning-workflow/scripts/build_distribution.py
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python skills/reasoning-workflow/tests/check_package.py
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python skills/reasoning-workflow/tests/check_package.py --archive dist/reasoning-workflow-3.1.0.zip
(cd dist && sha256sum -c SHA256SUMS)
```

---

## 3.0.1 维护版验证（2026-10-24）

- 34 项仓库级宿主契约测试：通过；使用隔离环境中的 `jsonschema==4.23.0` 与 `markdown==3.8.2`。
- 74 项 Portable 回归测试：通过，0 failure、0 error；包含 39 项保留基线、35 项新增回归检查和 38 次真实 CLI 子进程调用。测试回执 `model_evaluated=false`。
- 编译检查：`python -m compileall -q scripts tests` 通过；`git diff --check` 通过。
- 静态包检查：76 个 Markdown、353 个本地 Markdown 链接、13 个本地锚点、29 个 Python AST、54 个 JSON、14 个 JSON Schema、30 个路由引用；168 个归档文件、167 个内部校验和条目，源码/归档完全一致，失败数为 0。
- `dist/SHA256SUMS` 中 2.1.1、3.0.0、3.0.1 三个档案均通过 SHA-256 校验。
- 新增内容绑定的历史检查点工件、混合观点访谈夹具和稀疏检索/无需联网控制。共 18 个 V3 场景、23 个跨任务案例，均仍是协议材料，不是模型运行结果。
- 本版本补强夹具与完整性测试，不声称研究工作流规则或真实模型表现有所提升；没有执行真实模型 A/B 或盲评。

复现：

```sh
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python tests/run_all.py
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python tests/check_package.py
python -m compileall -q scripts tests
python scripts/build_distribution.py
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python tests/check_package.py --archive ../../dist/reasoning-workflow-3.0.1.zip
(cd ../../dist && sha256sum -c SHA256SUMS)
```

---

## 3.0.0 合并主分支基线验证（历史，2026-10-24）

- 34 项仓库级宿主契约测试：通过；使用隔离环境中的 `jsonschema==4.23.0` 与 `markdown==3.8.2`。
- 74 项 Portable 回归测试：通过，0 failure、0 error；包含 39 项保留基线、35 项新增回归检查和 38 次真实 CLI 子进程调用。回执报告 `model_evaluated=false`、`business_actions_executed=false`。
- 编译检查：`python -m compileall -q skills/reasoning-workflow/scripts` 通过。
- 静态包检查：73 个 Markdown、352 个本地链接、13 个本地锚点、29 个 Python AST、52 个 JSON、14 个 JSON Schema、30 个路由引用通过；分发包 163 个文件，162 个校验条目，源码/归档一致，失败数为 0。
- 分发档案：`reasoning-workflow-3.0.0.zip`；`dist/SHA256SUMS` 中 2.1.1、2.2.0、3.0.0 三个档案均通过校验。
- V3 在线因果搜索新增合成来源包，检查竞争结果、混杂观察与二手来源的重复依赖；它只验证证据处理协议，明确不是现实研究证据。17 个 V3 场景与 21 个跨任务案例仍是评测协议，尚未在真实模型上运行或盲评。
- 本报告不证明研究质量、服从率、真实联网检索表现、成本、延迟或长任务成功率提升。检查点身份对照也是确定性比较：CLI 参数不是可信的宿主现场状态；生产宿主仍须提供本次运行观察到的环境与工作区信息。

复现：

```sh
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python -m unittest discover -s tests -v
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python tests/run_all.py
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python tests/check_package.py
python scripts/build_distribution.py
uv run --no-project --with jsonschema==4.23.0 --with markdown==3.8.2 python tests/check_package.py --archive ../../dist/reasoning-workflow-3.0.0.zip
(cd ../../dist && sha256sum -c SHA256SUMS)
```

---

## 2.2.0 本地候选验证（历史基础，2026-10-24）

此前 2.2.0 候选完成过 34 项仓库契约测试、69 项 Portable 回归测试和静态包检查；这些记录仅描述当时的候选。3.0.0 结果以上述新一轮实际输出为准。该候选同样没有真实模型行为评测。

---

# Reasoning Workflow 2.1.1 — 历史测试报告

## 最终结果

2026-10-21，本地隔离依赖环境中，原有 39 项完整保留，新增 30 项边界测试，组合运行 69 项，0 failure、0 error。记录 38 次真实 Python CLI 子进程调用；其余是直接 API/契约检查。这不是模型/Agent 数量。

- Python：3.14.7，Linux x86_64。
- jsonschema：4.23.0，通过 uv 隔离调用，不修改全局 Python。
- 回执：[汇总](tests/results/summary_2_1_1.json)、[CLI 输入/退出码/输出](tests/results/cli_receipts_2_1_1.json)、[完整运行日志](tests/results/regression_2_1_1.log)。
- 原回归脚本 `tests/run_regression.py` 未删用例、未放宽断言；[2.1 历史报告](docs/TEST_REPORT_2.1_BASELINE.md) 保留作对照，历史报告不代表本版全部验证结论。

```sh
uv run --no-project --with jsonschema==4.23.0 python tests/run_all.py
```

## 五类问题与正向控制

| 边界 | 修复后的实际结果 | 合法控制 |
| --- | --- | --- |
| 关系单数引用漏追踪 | observation/evidence/传递依赖改变，原审查失效；缺引用/重复 ID 拒绝 | 未变更 bridge 通过；环路可终止 |
| Question lane 未闭合义务 | Question/Action/Mixed 都不能跳过显式 material blocked requirement/acceptance | 合法完成通过；partial 仅阶段性 ready，不伪报 task complete |
| 无 concurrency_group 绕过 forbidden | 无组、异组的潜在重叠拒绝 | 正确串行/有序 hybrid、允许的独立 parallel 通过 |
| Ultra 升档但漏资源 | 无 gap tag 仍必选 Ultra；篡改路由/缺资源拒绝 | Light 保持零加载；正常 prepare CLI 通过 |
| Tier3 非空虚假晋升证据 | 缺失、错类型/用途/范围、过期、改 lesson、改字节、缺独立性拒绝 | 完整合成宿主 gate index 通过；普通检索仍不返回 Tier3，maintenance 仍 advisory |

新增套件包含 prepare CLI、交付 CLI、runtime CLI、learning 验证/检索 CLI 与直接 API 检查。原套件覆盖 profile→route→review→canonical→实际文件字节的 bridge、恢复与宿主边界。原审查反例脚本另行完整重跑，见 [修复后结果](tests/results/original_probes_after.json)；[原2.1观察](tests/audit_repro/original_2.1_observations.json) 保留而未改写。

```sh
uv run --no-project --with jsonschema==4.23.0 python tests/audit_repro/adversarial_probes.py \
  --skill "$PWD" --output /tmp/workflow-probes.json
```

包级检查检查 Python AST、JSON/JSON Schema、相对 Markdown 目标与锚点、路由资源、原测试脚本保留，结果写入 [PACKAGE_VALIDATION.json](docs/PACKAGE_VALIDATION.json)。运行命令：

```sh
uv run --no-project --with markdown==3.8.2 --with jsonschema==4.23.0 python tests/check_package.py
```

内部 SHA256SUMS 排除自身及缓存；发布 ZIP 的 SHA-256 单独记录，避免自引用。解压后先校验哈希，再运行测试；重新运行会更新结果文件。

## 未覆盖与不得推断

- 69 项全部是确定性代码/合成数据测试；没有真实模型服从性、质量、token、时延或成本对照。
- 历史 2.1.1 基线记录为 16 类 [cross-task case](evals/cross_task_cases.json)；现行 3.0.0 候选增至 21 类。两者均为评测协议/完整性材料，不是完成的模型实验；3.0.0 包含自动入口/显式调用情境。
- 宿主回调/index 是显式合成测试夹具；没有认证真实外部 reviewer、晋升评估或独立模型。文件摘要仅证明字节及绑定。
- 没有真实外部执行器/支付/取消栅栏/恢复重放/数据库事务的集成实验。CLIs 校验与准备，不实现这些宿主能力。
- 本地修复包没有自动安装、修改 Wabi 设置、改写远端仓库或发布版本；不能保证任意模型读取后一定服从。

## 使用与迁移

简明变更、功能衔接和重新生成 route/review/evidence 的兼容边界见 [中文发布说明](docs/RELEASE_2.1.1.zh-CN.md)、[UPGRADE](UPGRADE.md)、[宿主接口](references/host-adapter.md)。
