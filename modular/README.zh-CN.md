# Reasoning Workflow 3.1.0 — Modular 版

[English](README.md) · [简体中文](README.zh-CN.md)

Modular 版把六个工作流 Family 拆成可独立安装、仅含指令的 Agent Skill。适合宿主已经能很好地发现和路由 Skill，或某项任务只需要其中一部分的情况。共享研究方法与 Portable 3.1.0 同步；Modular 不是六份可以完整取代主入口 Portable Skill 的副本。

遇到重要调研时，应根据情境推断需要考察现实结果、开发前的工程／架构证据，还是两者兼有；用户不必先给任务贴标签。默认保留宿主当前选择的模型。工作流会根据任务自动选择合适的投入深度，同时遵从用户明确指定的深度。Ultra 表示工作流投入程度，不代表切换模型。

- `reasoning-core` — 问题框定、表征、拆解、关系、假设与解释
- `deep-research` — 问题驱动调研、资料检索、证据／来源脉络、时效性、比较综合与 Ultra 调研
- `decision-analysis` — 选项完整性、权衡、偏好、稳健性与建议
- `execution-control` — 获准执行、持久状态、委派、检查点与恢复
- `audit-verification` — 验证、独立审查、评估有效性与效果
- `workflow-learning` — 维护层面的 CAPA 与证据门控学习

每个 Skill 都含有所属 Family 的指引和它需要的参考资料。独立安装的 Deep Research Skill 包含信息目标导航和研究模式参考；Reasoning Core 包含澄清关卡。共享方法会在确有需要的地方镜像；Python 路由器、Schema、运行时辅助工具和跨 Family 状态仍属于 Portable。

## 在宿主中安装

| 宿主 | 建议安装方式 |
| --- | --- |
| Codex CLI / IDE | 把选中的完整 Skill 目录放在宿主识别的 `.agents/skills/<skill-name>/` 路径下。 |
| Claude Code | 把选中的完整 Skill 目录放在 `.claude/skills/<skill-name>/` 下，并遵循该宿主当前的激活规则。 |
| ChatGPT、Claude 应用、Grok 聊天 | 只有在实际产品界面提供原生 Skill 时才使用；否则通过项目／自定义指令并按需提供参考资料。 |

关于账户和配置限制、串行 Ultra 行为及界面回退方式，请参阅规范的[宿主配置说明（英文）](../skills/reasoning-workflow/references/harness-profiles.md)。只使用当前实际开放的工具；普通聊天中也可以串行调研。[研究模式指南（英文）](../skills/reasoning-workflow/references/research-modes-and-methods.md)和[澄清关卡（英文）](../skills/reasoning-workflow/references/clarification-gate.md)也可在对应 Skill 中按需使用。不要假定某个产品开放了规范的 Python 辅助工具、代理、搜索、MCP、Research 模式、连接器或交互式 UI。

若需要完整的 Light 到 Ultra 深度关卡、确定性路由、跨 Family 状态和执行契约，请安装[Portable 版（英文入口）](../skills/reasoning-workflow/)。

使用开放的 `skills` CLI 安装一个聚焦 Skill，例如：

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill deep-research
```
