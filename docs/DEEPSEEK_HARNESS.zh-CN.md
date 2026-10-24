# 在 DeepSeek Harness 中使用 Reasoning Workflow

> [!NOTE]
> DeepSeek Harness 有两种不同的扩展方式：本地 **Skill** 是 Markdown 指令包；Harness 原生 **plugin** 是可执行的 TypeScript/Cordis 模块。本仓库提供的是 Portable Skill，不是原生 DSH plugin。不要把它的 `SKILL.md` 当作 Cordis 插件安装。

[English](DEEPSEEK_HARNESS.md) · [简体中文](DEEPSEEK_HARNESS.zh-CN.md) · [项目 README](../README.zh-CN.md)

## 你将安装什么

Portable 版本是一个目录包，入口文件为 `SKILL.md`，并通过相对路径引用 `references/`、`families/`、`schemas/` 和 `scripts/` 中的材料。DeepSeek Harness 官方说明的文件系统 Skill 提供方支持在已扫描 Skill 根目录中放置顶层 `<name>/SKILL.md` 目录包。因此，本仓库的 Skill 可以作为本地指令包使用，不需要编写适配插件。

DeepSeek Harness 原生插件机制面向 TypeScript 模块和插件包。只有在开发真正的 DSH 扩展时才需要这条路径；加载本工作流不需要原生插件。

## 安装到项目工作区

以下步骤只为一个项目安装 Skill，不会改变 Harness 的模型设置，也不会额外授予权限。

1. **获取仓库。** 克隆仓库，或下载完整的 Portable 包。保持 `reasoning-workflow` 目录完整；只复制 `SKILL.md` 会破坏相对引用。
2. **确定工作区根目录。** 使用 DeepSeek Harness 将要打开的项目目录。如果本仓库本身就是项目，请在仓库根目录执行：

   ```bash
   mkdir -p .dsh/skills
   cp -R skills/reasoning-workflow .dsh/skills/reasoning-workflow
   ```

   如果 Skill 来自另一个检出目录，则把完整目录复制到 `<你的工作区>/.dsh/skills/reasoning-workflow/`。不要把外层 `skills/` 父目录当成 Skill 包名复制。
3. **启动 DeepSeek Harness。** 按照[官方快速开始](https://deepseek-harness.github.io/deepseek-harness/guide/quickstart)和[官方 Harness 仓库](https://github.com/deepseek-ai/deepseek-harness)确认当前前置条件与启动方式。当前仓库快速开始文档给出的命令是 `npx @deepseek-ai/dsh web`；安装要求可能变化。
4. **选择工作区。** 在 Web UI 中添加并选择包含 `.dsh/skills/reasoning-workflow/` 的项目根目录。`dsh` 进程的工作目录不会自动成为 Web UI 已选择的工作区。
5. **检查当前配置是否支持 Skill。** DeepSeek 的文件系统发现、Skill 注册表和面向模型的 Skill 目录／加载器是不同组件。所选 Harness 组合／配置必须提供文件系统提供方；若要让模型自行发现并加载 Skill，还需要注册表和 `skill` 工具。自定义配置可能没有这些组件。依赖自动发现前，先确认 `reasoning-workflow` 出现在可用 Skill 目录或界面的 `/` 命令建议中。
6. **需要时配置模型。** Harness 官方快速开始在 **Settings → Models** 中配置模型。这与安装或调用 Skill 是两件事。

Harness 的文件系统提供方把 `.dsh/skills` 列为项目 Skill 根目录。它也识别 `.agents/skills` 和已配置／用户级目录，但项目级 `.dsh/skills` 最适合新手先用。该提供方只发现一层目录包（`<root>/<name>/SKILL.md`）或平铺的 `<name>.md` 文件；不会递归发现更深层的 Skill。

## 使用方式

如果希望明确调用，可在支持 Harness Skill 命令的客户端中输入斜杠命令：

```text
/reasoning-workflow 这个课后辅导项目能否提高数学成绩、对哪些人有效，以及什么证据会改变结论？
```

开发前架构问题示例：

```text
/reasoning-workflow 开始写代码前，先检查这个工作区，比较可行的离线优先备份与恢复设计。暂时不要编辑文件。
```

限定范围的任务示例：

```text
/reasoning-workflow 简短回答这个稳定事实问题。只用给定信息；除非关键事实不确定，否则不要联网搜索。
```

Harness 的模型侧 Skill 集成文档说明了 `/name` 调用方式；具体 UI 和是否可用，取决于当前客户端与配置。如果斜杠调用不可用，只要 Skill 目录和加载器对模型可见，也可以用普通语言要求 Agent 使用 `reasoning-workflow` Skill。自动匹配取决于宿主，且属于尽力而为：Skill 文本无法强迫自己被激活。

工作流负责选择相关证据方法和适度投入。“Ultra”表示工作流推理深度，不是切换模型、使用所有工具或允许编辑／发布／执行。例如：

```text
/reasoning-workflow 使用 Ultra 深度调研这个恢复功能是否有实际需求，以及当前仓库能否安全支持。需求证据与工程可行性请分开论证。
```

## 如何适配当前 Harness 工作区

- **保持入口和参考资料在一起。** 主 `SKILL.md` 使用相对链接指向支持文件。如果要调整指引，保留这些引用，或同步更新它们。
- **优先使用工作区级定制。** 项目的专属约束和约定，建议写在独立的本地 Skill 或可信的 Harness 指令中，不要为了单个项目去改写共享的上游方法。
- **权限由 Skill 之外的机制控制。** Harness 当前权限策略和审批界面决定文件修改、命令及外部操作权限。工作流深度或措辞不会授予这些权限。
- **只有编写真实集成代码时才用原生插件。** 原生 DSH 插件必须符合官方 TypeScript/Cordis 插件契约及包／manifest 结构。本仓库不包含这类插件，也不假定存在未公开的插件 API。
- **其他 Harness 配置要另行确认。** 如果使用不同组合，请查阅官方文档确认挂载了哪些 Skill 包。文件已放在磁盘上，不代表当前 Agent 一定能发现或加载。

## 安装冒烟测试

安装后，使用以下只读提示词测试：

```text
/reasoning-workflow 检查此工作区的顶层项目说明。指出你实际读取的文件名和其中一条具体约束。不要编辑文件或运行命令。
```

有用的冒烟测试结果应指出实际读取的项目说明及可核对的内容，且不声称执行了写入或更广泛的调研。如果 Agent 看不到文件，先确认选中的工作区根目录，以及完整 Skill 包是否位于 `.dsh/skills/` 下；再确认当前配置是否开放 Skill 发现／加载，并检查目录或命令建议中是否出现该 Skill。

这只能验证当前某一种 Harness 配置中的一条安装路径，不是跨版本宿主兼容性测试，也不能证明模型总会遵循 Skill。

## 兼容性速览

| 环境 | 安装形式 | 调用／发现方式 | 本仓库提供什么 |
|---|---|---|---|
| DeepSeek Harness | 完整 Portable 目录放在项目 `.dsh/skills/reasoning-workflow/` | 原生文件系统 Skill 发现；客户端／配置提供用户 Skill 命令时可用 `/reasoning-workflow`；模型加载需要可见的 Skill 工具路径 | Markdown Skill 目录包；不是 DSH Cordis 插件 |
| Codex | 完整 Portable 目录放在 `.agents/skills/reasoning-workflow/` | 宿主原生 Skill 发现／调用 | Portable 目录包 |
| Claude Code | 完整 Portable 目录放在 `.claude/skills/reasoning-workflow/` | 宿主原生 Skill 发现／调用 | Portable 目录包 |
| 其他兼容 Skills 的宿主 | 按该宿主文档使用其 Skill 目录和激活规则 | 由宿主与客户端决定 | Portable Markdown 指令；不保证隐式自动激活 |

路径和客户端行为可能变化。正式部署前请以宿主最新官方文档为准。

## 官方参考资料

- [DeepSeek Harness 仓库与当前快速开始](https://github.com/deepseek-ai/deepseek-harness)
- [DeepSeek Harness Web UI 快速开始](https://deepseek-harness.github.io/deepseek-harness/guide/quickstart)
- [官方本地文件系统 Skill 提供方契约](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.zh.md)
- [官方 Skill 注册表／提供方概览](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/README.zh.md)
- [官方面向模型的 Skill 目录、加载器与 `/name` 行为](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.zh.md)
- [官方原生插件发布指南](https://deepseek-harness.github.io/deepseek-harness/develop/basic/publish)
- [官方第三方插件市场指南](https://deepseek-harness.github.io/deepseek-harness/guide/plugin-market)
