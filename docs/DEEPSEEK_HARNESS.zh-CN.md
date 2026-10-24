# DeepSeek Harness 插件：安装与使用

> 这是一个原生 Cordis 组合包，会把仓库中的 Reasoning Workflow 注册为 Harness 内置 Skill。它打包了完整 Skill 运行目录；不会新增工具、授予权限或改变宿主审批策略。

[English](DEEPSEEK_HARNESS.md) · [项目 README](../README.zh-CN.md) · [技术架构](../skills/reasoning-workflow/docs/TECHNICAL_ARCHITECTURE.zh-CN.md)

## 从本仓库安装

前置条件：已安装 DeepSeek Harness `dsh` CLI，并且 `pnpm` 在 `PATH` 中（CLI 会把插件管理命令转交给 pnpm）。在仓库根目录，把本地组合包安装到你使用的 profile：

```sh
dsh plugin --profile default add ./integrations/deepseek-harness
```

如需使用其他 profile，把 `default` 换成对应名称。该命令只会把组合包加入 profile；不会发布到 npm 或 Plugin Market。可用下面的命令检查解析后的 profile 配置：

```sh
dsh --profile default --dump-config
```

确认插件列表中出现 `reasoning-workflow-deepseek-harness`，然后按平常方式启动或重启该 Harness profile，使新组合生效。如果仓库检出在其他位置，请从仓库根目录执行安装命令，或改用相应绝对路径。

## 使用 Skill

可以直接按名称请求，也可在当前 Harness Skill 消费端提供 `/reasoning-workflow` 命令时使用它：

```text
/reasoning-workflow 使用 Ultra 深度比较这个结果最有力的几种解释。指出哪些证据能区分它们，核查最关键的来源，并说明仍有哪些不确定性。
```

插件会把 Skill 标记为可由模型和用户调用。自动匹配由 Harness 与模型决定；明确点名调用更可靠。“Ultra”指更深入、迭代式的研究工作流，不代表切换模型、要求使用全部工具，也不授予编辑文件或对外承诺的权限。Harness 的权限与确认机制仍然优先。

安装后的只读检查示例：

```text
/reasoning-workflow 阅读仓库 README，告诉我其中一条具体项目约束。不要编辑文件或运行命令。
```

如果没有出现该 Skill，先用 `--dump-config` 检查所选 profile，确认插件条目已加入，并确认 profile 包含标准 Skills 注册表和面向模型的 Skill 消费端。某些精简自定义 profile 可能没有这些宿主服务；插件本身不会代替它们。

## 组合包包含什么

`integrations/deepseek-harness/` 是真实的 `dsh.bundle` 包。其 Cordis 插件会注册原生 `SkillProvider`；提供方负责返回内置 `SKILL.md`，并通过资源目录暴露相邻的参考资料、families、schemas、scripts 和 assets。内置 Skill 是本仓库 Portable 运行文件的副本；修改规范 Skill 后请重新同步：

```sh
pnpm --dir integrations/deepseek-harness run sync-skill
pnpm --dir integrations/deepseek-harness test
```

测试会检查提供方是否注册了内置 Skill，以及打包入口文本是否与 `skills/reasoning-workflow/SKILL.md` 一致。这个组合包随本仓库提供，目前尚未上架 Harness Plugin Market，也没有发布为 npm 包。

## 官方参考资料

- [Harness：打包与安装插件组合包](https://deepseek-harness.github.io/deepseek-harness/develop/basic/publish)
- [Harness：插件市场](https://deepseek-harness.github.io/deepseek-harness/guide/plugin-market)
- [Harness Skill 提供方注册表](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/README.zh.md)
- [Harness 内置 Skill 提供方示例](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/experimental/skill-badge/src/index.ts)
- [Reasoning Workflow Portable Skill](../skills/reasoning-workflow/SKILL.md)
