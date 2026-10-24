<div align="center">
  <img src="skills/reasoning-workflow/assets/icon.svg" width="76" height="76" alt="Reasoning Workflow" />

  # Reasoning Workflow

  **一套帮助 AI 提出更好的问题、找到更可靠证据，并把事情做完的工作流。**

  [English](README.md) · [简体中文](README.zh-CN.md)

  [DeepSeek Harness 使用指南](docs/DEEPSEEK_HARNESS.zh-CN.md) · [选择安装版本](#edition) · [技术架构](skills/reasoning-workflow/docs/TECHNICAL_ARCHITECTURE.zh-CN.md) · [下载 Portable 完整包](dist/reasoning-workflow-3.1.0.zip)
</div>

---

Reasoning Workflow 是一套供 AI Agent 使用的指引，以及可选的辅助工具。它帮助 Agent 弄清答案真正取决于什么，选择与任务相称的调研方法，并检查建议或交付是否符合需求。

它适用于现实问题调研、开发前的研究、决策、写作与代码，以及需要跨会话继续推进的工作。简单问题依然可以直接回答。工作流的目的是改善解决问题的路径，不是让每件事都变复杂。

> [!NOTE]
> 本仓库不是模型、搜索服务或权限系统。宿主应用决定 Skill 是否加载、可用模型与工具，以及允许执行哪些操作。Skill 指引本身不能强制激活，也不能证明模型确实照做。

<a id="deep-research"></a>

## Deep Research：围绕“哪些证据会改变答案”展开

本项目最核心的能力，是以证据为中心组织 Deep Research，而不是把搜索词写得更长。工作流会先找出结论真正取决于什么，再寻找能够区分竞争解释的观察，阅读原始材料，核查关键主张是否得到来源支持，并综合已知、适用边界与未知。若继续调研很难改变一个简单问题的答案，它也应及时停下。

| Agent 会做什么 | 你可以从结果中检查什么 |
|---|---|
| 确定影响决策的问题与关键未知 | 聚焦于问题本身的回答，而不是泛泛介绍主题 |
| 沿因果关系和竞争解释寻找证据，而非机械重复关键词 | 分别回应效果、机制、替代解释和适用边界的材料 |
| 核对来源脉络，以及证据是否真的支持对应主张 | 清楚区分直接证据、推断、争议与未知 |
| 把发现重新连接到原始决策，并控制调研投入 | 带有适用条件和剩余限制的建议 |

```mermaid
flowchart LR
  Q[真正重要的问题] --> U[决定答案的未知项]
  U --> E[寻找能区分解释的证据]
  E --> S[阅读来源并核查主张支持度]
  S -->|仍有缺口或冲突| E
  S --> Y[综合发现、边界与未知]
  Y --> D[回答或建议]
  D --> C{更多证据会改变答案吗？}
  C -->|会，且缺口重要| E
  C -->|不会| F[按适当深度完成]
```

例如，“辅导有没有用？”会被拆成对结果、项目设计、受益人群、可能机制、自我选择偏差和研究局限的核对；不会把一次搜索或单篇研究说成因果证明。方法概览见本 README 的“工作流如何选择路径”；实现结构见[技术架构报告（简体中文）](skills/reasoning-workflow/docs/TECHNICAL_ARCHITECTURE.zh-CN.md)。

## 从这里开始

1. **选择一个版本。** 不确定时，先用 Portable。
2. **安装完整 Skill 文件夹。** 按[Claude Code、Codex 或其他 Agent 的说明](#install-portable-zh)选择宿主目录；不要只复制 `SKILL.md`，它需要同目录的支持文件。
3. **在宿主中启用或调用它。** 下方按宿主给出了具体路径和验证方法；其他适配见[宿主与 Agent 配置](skills/reasoning-workflow/references/harness-profiles.md)。
4. **像平时一样提问。** 工作流应根据情境推断调研路径和投入深度。想明确指定时，可以试试[下面的示例](#try-it)。
5. **检查结果。** 对高风险或易变问题，要求它给出决定性证据、不确定性和适用边界，而不只是一个肯定的结论。

<a id="edition"></a>

## 选择安装版本

|  | Portable | Modular |
|---|---|---|
| 适合谁 | 希望有一个统一入口和完整工作流 | 宿主已能发现并调度多个 Skill |
| 包含什么 | 入口 Skill、按需参考资料、Schema、可选 Python 工具和测试 | 六个独立的指令型 Skill，各自带参考资料 |
| 取舍 | 包更完整；仅在使用辅助工具时需要兼容的 Python 环境 | 不含 Portable 的 Python 辅助工具及跨 Family 共享运行时／状态层 |
| 从这里开始 | [`skills/reasoning-workflow/`](skills/reasoning-workflow/) | [`modular/README.zh-CN.md`（简体中文）](modular/README.zh-CN.md) |

首次安装推荐 Portable。Modular 不是六份各自包含所有 Portable 功能的完整副本；它更适合能可靠组合多个 Skill 的宿主。Modular 包含 `reasoning-core`、`deep-research`、`decision-analysis`、`execution-control`、`audit-verification` 和 `workflow-learning`。

<a id="install-portable-zh"></a>

### 安装 Portable

规范 Skill 位于 `skills/reasoning-workflow/`。请安装**整个文件夹**，不要只复制 `SKILL.md`：它依赖相对路径下的参考资料、families、schemas、scripts 和 assets。可以克隆仓库，或解压[完整 Portable 压缩包](dist/reasoning-workflow-3.1.0.zip)。下面命令假设你已克隆仓库，并在仓库根目录运行：

```sh
git clone --depth 1 https://github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills.git
cd Agent--deep-research-Workflow-Skills
```

克隆方式需要 Git，且需要先安装要使用的宿主。下面命令使用 Bash/zsh（macOS、Linux、WSL 或 Git Bash）。命令会在目标目录已存在时主动停止。请先检查或备份原有 Skill，不要把新文件直接合并覆盖自定义内容。示例安装到当前用户目录，所有项目都可用；只想给单个项目使用时，则放到对应宿主的项目目录（Claude Code 用 `.claude/skills/`；Codex 用 `.agents/skills/`）。

#### Claude Code

Claude Code 会发现用户级目录 `~/.claude/skills/` 和项目级目录 `.claude/skills/`。在仓库根目录运行下面命令，安装到当前用户：

```sh
dest="$HOME/.claude/skills/reasoning-workflow"
if [ -e "$dest" ]; then
  echo "目标已存在；替换前请先检查或备份：$dest" >&2
  exit 1
fi
mkdir -p "$(dirname "$dest")"
cp -R skills/reasoning-workflow "$dest"
test -f "$dest/SKILL.md"
```

运行 `claude`，询问 `What skills are available?`，确认列表里有 `reasoning-workflow`，再输入 `/reasoning-workflow` 或提出匹配该 Skill 描述的请求。如果列表中没有，检查目标路径并重启 Claude Code。当前发现与调用方式见 [Claude Code Skills 官方文档](https://docs.anthropic.com/en/docs/claude-code/skills)。

#### Codex

Codex 会发现用户级目录 `~/.agents/skills/`；也支持项目级 `.agents/skills/`。在仓库根目录运行下面命令，安装到当前用户：

```sh
dest="$HOME/.agents/skills/reasoning-workflow"
if [ -e "$dest" ]; then
  echo "目标已存在；替换前请先检查或备份：$dest" >&2
  exit 1
fi
mkdir -p "$(dirname "$dest")"
cp -R skills/reasoning-workflow "$dest"
test -f "$dest/SKILL.md"
```

在 Codex 中打开 `/skills`，确认列表里有 `reasoning-workflow`；再用 `$reasoning-workflow` 调用，或直接提出符合其描述的请求。Codex 通常会自动发现新 Skill；若未显示，请重启 Codex。当前目录与用法见 [Codex Skills 官方文档](https://developers.openai.com/codex/skills)。

#### 给 AI Agent 的安装指令

可以把下面这段指令复制给要配置的 Agent（已知宿主时，可在开头写明宿主名称）：

> 请从 `https://github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills` 安装 Reasoning Workflow Skill。若已有干净仓库副本则使用它；否则在父目录运行 `git clone --depth 1 https://github.com/zy839971925-zyy/Agent--deep-research-Workflow-Skills.git`，克隆到新的目录，不要覆盖已有文件。先识别当前宿主是 Claude Code、Codex，还是其他有文档说明的 Skill 宿主，并阅读该仓库 README 的安装部分。使用规范源目录 `skills/reasoning-workflow/`，完整复制这个文件夹并保留相对文件；不要只安装 `SKILL.md`。Claude Code 的用户级目标目录是 `~/.claude/skills/reasoning-workflow/`；Codex 是 `~/.agents/skills/reasoning-workflow/`。写入前先检查目标路径；如果已存在，请停止并报告路径，不要覆盖、合并、删除或改名用户文件。其他宿主只按其当前官方 Skill 安装说明操作；无法确认目标目录时，先询问再写入。完成后确认安装目录下有 `SKILL.md` 和支持目录；若当前会话能访问宿主，再验证宿主是否发现了它。报告来源、安装位置、做过的验证及无法验证的事项。除非真的运行了模型任务，不要声称已测试模型行为。这只安装 Skill；只有当当前宿主是 DeepSeek Harness 且用户要求安装其插件时，才继续安装 DeepSeek Harness 插件。

Windows PowerShell 可用下面这段等价复制流程；Claude Code 的 `$dest` 如下，Codex 请改成 `.agents/skills/reasoning-workflow`：

```powershell
$dest = Join-Path $HOME ".claude/skills/reasoning-workflow"
if (Test-Path -LiteralPath $dest) { throw "目标已存在，请先检查或备份：$dest" }
New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
Copy-Item -Recurse -LiteralPath "skills/reasoning-workflow" -Destination $dest
if (-not (Test-Path -LiteralPath (Join-Path $dest "SKILL.md"))) { throw "没有复制到 SKILL.md" }
```

这段提示说明了安全流程，不会自动授予文件修改权限。Agent 仍需实际访问宿主文件系统，并在目标已存在时停止。

#### DeepSeek Harness：安装插件，而不只是 Skill 文件夹

DeepSeek Harness 使用本仓库单独提供的原生 Cordis 组合包；把 Portable Skill 复制到其他宿主目录，**不会**安装这个插件。前置条件：已安装 `dsh` CLI，且 `pnpm` 可用。在仓库根目录把组合包加入你使用的 profile：

```sh
dsh plugin --profile default add ./integrations/deepseek-harness
dsh --profile default --dump-config
```

如果你用的不是 `default`，请替换成实际 profile 名。确认解析后的插件列表包含 `reasoning-workflow-deepseek-harness`，然后启动或重启该 profile，并向 `/reasoning-workflow` 提出一个只读问题。这个组合包随仓库分发，尚未发布到 npm 或 Plugin Market。完整步骤见 [DeepSeek Harness 插件安装与使用指南](docs/DEEPSEEK_HARNESS.zh-CN.md)。

Python 辅助工具是可选的，依赖见 [`requirements.txt`](skills/reasoning-workflow/scripts/requirements.txt)。这些工具用于准备或校验任务记录，不会运行模型、激活 Skill，也不会执行现实世界操作。

### 安装 Modular

1. 打开 [Modular 指南（简体中文）](modular/README.zh-CN.md)，按宿主需求选择要安装的 Skill。
2. 将每个所选 Skill 的**完整文件夹**放入宿主识别的目录（例如 Codex 的 `.agents/skills/<skill-name>/`，或 Claude Code 的 `.claude/skills/<skill-name>/`）。
3. 启用宿主的原生 Skill 发现。可以从 `reasoning-core` 开始；涉及证据调研时再启用 `deep-research`，其他 Skill 按任务需要加入。

如果宿主支持 `skills` CLI，仓库指南提供了一个只安装指定 Skill 的示例：

```bash
npx skills add zy839971925-zyy/Agent--deep-research-Workflow-Skills --skill deep-research
```

CLI 和宿主的安装方式可能变化；如果命令或路径不可用，请以宿主当前文档为准。

### DeepSeek Harness

本仓库除了 Portable Markdown Skill，还包含一个可安装的原生 Cordis 组合包，可将 Reasoning Workflow 注册为 DeepSeek Harness Skill。请看 [DeepSeek Harness 插件安装与使用指南](docs/DEEPSEEK_HARNESS.zh-CN.md)；该组合包目前随仓库提供，尚未发布到 npm 或 Plugin Market。

## 工作流如何选择路径

你不需要先给任务贴上“现实问题”或“工程调研”的标签。遇到需要认真调查的问题时，Agent 会根据真正影响决策的问题，推断应该寻找哪类观察：

- **现实／经验问题：** 发生了什么、规模多大、影响谁、什么导致变化，或预期结果有哪些证据？
- **开发前工程／架构：** 在真实代码库、约束和质量目标下，哪些设计可行，关键取舍是什么？
- **相互关联的混合问题：** 人们需要什么，这个系统能否实现？先区分需求证据和技术可行性证据，再在决策处把两者连接起来。

默认使用宿主已经选择的模型。工作流会根据复杂度、不确定性、时效性、后果，以及新增证据能否改变答案，自动选择合适的投入深度：从 Light、Standard、Deep、Max 到 Ultra。这是工作投入程度，不代表切换模型、固定输出篇幅，也不会增加工具权限或行动授权。用户明确指定深度时，优先按指定深度执行，但仍受宿主实际能力限制。

```mermaid
flowchart LR
  A[你的请求] --> B[推断所需证据路径与工作深度]
  B --> C[现实／经验调研]
  B --> D[开发前工程调研]
  B --> E[现实与技术相连的混合问题]
  C --> F[寻找并阅读与决策有关的证据]
  D --> G[检查真实项目并比较可行设计]
  E --> H[连接现实需求与系统可行性]
  F --> I[回答、建议，或询问必要信息]
  G --> I
  H --> I
  I --> J[核对结果并说明重要限制]
```

面对因果问题，因果链是待检验的假设，不是证明。搜索应沿着可能改变结论的环节展开，检查竞争解释和适用边界，并阅读原始材料，而不是只信摘要或重复引用。面对架构问题，应先检查实际仓库和需求，再推荐设计。更完整的 Deep Research 工作方式见本 README 的[Deep Research 介绍](#deep-research)；技术实现见[技术架构报告](skills/reasoning-workflow/docs/TECHNICAL_ARCHITECTURE.zh-CN.md)。

<a id="try-it"></a>

## 试着使用

Portable 入口的设计目标是：当宿主将它作为默认入口提供时，对每条请求静默做轻量分流。你也可以对当前请求明确调用：

> **“调用我的 workflow skills，评估这个课后辅导项目能否提高数学成绩、对哪些学生有效，以及什么证据会改变结论。”**
>
> 预期路径：现实／因果调研。工作流应区分成绩效果与可能机制、替代解释，再调查那些可能改变结论的关键缺口。

> **“开始开发前，请先检查这个代码库，为离线课表编辑和可靠恢复设计架构。使用我的 workflow skills 的 Ultra 深度。”**
>
> 预期路径：开发前工程调研，并按明确要求使用 Ultra 深度。Agent 应检查现有项目证据，按约束比较设计；Ultra 本身不代表授权改代码。

> **“使用我的 workflow skills 的 Ultra 深度，查明学生是否需要这个恢复功能，以及我们的离线 App 能否安全支持它。”**
>
> 预期路径：现实需求与技术可行性相连的混合调研。需求证据和工程证据应分别说明，再连接到建议中。

> **“简单回答即可，尽量轻量；除非有关键事实不确定，否则不用做大范围调研。”**
>
> 预期路径：Light 或同样精简的处理方式，直接回答；只有剩余不确定性会实质影响答案时，才做针对性核查。

说 **“调用我的 workflow skills”** 会为当前请求选择该工作流；它本身不等于 Ultra。想明确使用 Ultra，可以说：**“使用我的 workflow skills 的 Ultra 深度去思考调研。”** 如果希望既调用又使用 Ultra，把两项要求都说清楚。

## 没有按预期工作时

- **宿主没有识别到 Skill：** 检查完整文件夹是否放在正确的宿主目录，并确认已开启 Skill 发现。部分宿主只会尽力匹配。若要求每条请求都先经过工作流，需要在宿主中配置可信的常驻指令或前置路由；Skill 文件不能强制自己加载。
- **主动调用短语没有效果：** 把它作为你当前请求中的指令，不要只放在引文、文件或其他资料里；并确认当前宿主界面支持此 Skill。
- **简单问题收到太多流程：** 明确要求直接回答或 Light。深度影响调查投入，不应强制长报告、固定章节或增加 Agent。
- **Ultra 好像切换了模型或触发了操作：** 这不应发生。Ultra 只改变工作流投入程度，不切换模型、不增加权限，也不授权执行。
- **Agent 说搜索过，却没有可用证据：** 要求它指出实际打开的来源，并说明来源如何支持关键主张。账号已连接或产品介绍中有某功能，不代表本次运行确实使用了它。
- **Skill 只有部分内容可用：** 重新安装完整文件夹，不要只复制入口文件。使用 Modular 时，还要确认安装并启用了与当前任务有关的 Skill 及其参考资料。

如果宿主没有提供需要的搜索工具、连接器、权限或运行时辅助工具，工作流应尽可能使用受支持的替代路线，并说明剩余限制；它不能凭空创造宿主未开放的能力。

## 测试能说明什么

自动化检查覆盖 Schema、链接、辅助工具、包内容和协议场景等结构契约，可以发现这些方面的回归；但它们**不能证明模型会遵循每条指引，也不能证明调研质量提高**。要评估实际效果，需要在模型、宿主、工具和预算可比的条件下，对同一组任务进行有／无工作流的对照，并评阅答案及可观察的证据收集过程。

同样，计划、检查点或子代理报告也不能证明外部操作已经发生。宿主必须提供真实结果，并执行自身的权限和操作规则。

## 仓库导航

- [`skills/reasoning-workflow/`](skills/reasoning-workflow/)：Portable 入口、方法、Schema、可选工具和包内测试。
- [`modular/`](modular/)：供宿主原生路由使用的分体 Skill。
- [`tests/`](tests/)：仓库级宿主契约测试。
- [`dist/`](dist/)：Portable 版本包及校验和。
- [DeepSeek Harness 指南（简体中文）](docs/DEEPSEEK_HARNESS.zh-CN.md) · [DeepSeek Harness guide (English)](docs/DEEPSEEK_HARNESS.md)
- [技术架构报告（简体中文）](skills/reasoning-workflow/docs/TECHNICAL_ARCHITECTURE.zh-CN.md) · [Technical architecture (English)](skills/reasoning-workflow/docs/TECHNICAL_ARCHITECTURE.md)
- [贡献指南（英文）](CONTRIBUTING.md) · [隐私说明（英文）](PRIVACY.md) · [使用条款（英文）](TERMS.md) · [MIT 许可证原文](LICENSE)

<sub>由 <a href="https://github.com/zy839971925-zyy">折鸢 / zy839971925-zyy</a> 维护。</sub>
