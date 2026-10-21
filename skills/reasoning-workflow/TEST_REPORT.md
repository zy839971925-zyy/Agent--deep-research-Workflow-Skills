# Reasoning Workflow 2.1.1 — 实际测试报告

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
- 六类 [cross-task case](evals/cross_task_cases.json) 仍是评测协议/完整性材料，不是完成的模型实验。
- 宿主回调/index 是显式合成测试夹具；没有认证真实外部 reviewer、晋升评估或独立模型。文件摘要仅证明字节及绑定。
- 没有真实外部执行器/支付/取消栅栏/恢复重放/数据库事务的集成实验。CLIs 校验与准备，不实现这些宿主能力。
- 本地修复包没有自动安装、修改 Wabi 设置、改写远端仓库或发布版本；不能保证任意模型读取后一定服从。

## 使用与迁移

简明变更、功能衔接和重新生成 route/review/evidence 的兼容边界见 [中文发布说明](docs/RELEASE_2.1.1.zh-CN.md)、[UPGRADE](UPGRADE.md)、[宿主接口](references/host-adapter.md)。
