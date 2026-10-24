# Use Reasoning Workflow with DeepSeek Harness

> [!NOTE]
> DeepSeek Harness has two different extension paths: local **Skills** are Markdown instruction bundles; native Harness **plugins** are executable TypeScript/Cordis modules. This repository provides a portable Skill, not a native DSH plugin. Do not install its `SKILL.md` as a Cordis plugin.

[English](DEEPSEEK_HARNESS.md) · [简体中文](DEEPSEEK_HARNESS.zh-CN.md) · [Project README](../README.md)

## What you will install

The Portable edition is a directory bundle whose entry is `SKILL.md` and whose relative `references/`, `families/`, `schemas/`, and `scripts/` files support it. DeepSeek Harness's documented filesystem Skill provider accepts a top-level `<name>/SKILL.md` bundle under a scanned Skill root. The repository folder can therefore be installed as a local Skill without writing an adapter plugin.

DeepSeek Harness's native plugin mechanism is for TypeScript modules and plugin packages. Use that route only when you are building a real DSH extension; it is not needed to load this workflow.

## Install into a project workspace

These steps install the Skill for one project. They do not change Harness model settings or grant extra permissions.

1. **Get the repository.** Clone it, or download the repository's complete Portable package. Keep the `reasoning-workflow` directory intact; copying only `SKILL.md` breaks its relative references.
2. **Choose the workspace root.** Use the project directory that DeepSeek Harness will open. If this repository itself is the project, run the following commands from its root:

   ```bash
   mkdir -p .dsh/skills
   cp -R skills/reasoning-workflow .dsh/skills/reasoning-workflow
   ```

   If the Skill lives in another checkout, copy that complete directory into `<your-workspace>/.dsh/skills/reasoning-workflow/` instead. Do not copy the surrounding `skills/` parent as the bundle name.
3. **Start DeepSeek Harness.** Follow the [official quickstart](https://deepseek-harness.github.io/deepseek-harness/en/guide/quickstart) and the [official Harness repository](https://github.com/deepseek-ai/deepseek-harness) for current prerequisites and launch instructions. The current repository quickstart documents `npx @deepseek-ai/dsh web`; installation requirements may change.
4. **Select the workspace.** In the Web UI, add and select the project root that contains `.dsh/skills/reasoning-workflow/`. The `dsh` process's working directory is not automatically selected as a Web UI workspace.
5. **Check Skill support in the active profile.** DeepSeek's filesystem discovery, Skill registry, and model-facing Skill catalog/loader are separate components. The chosen Harness composition/profile must expose the filesystem provider and, for model-discovered loading, the registry and `skill` tool. A custom profile may omit them. Confirm that `reasoning-workflow` appears in the available Skill catalog or the UI's `/` suggestions before relying on automatic discovery.
6. **Set up a model if needed.** Harness's official quickstart configures a model under **Settings → Models**. This is separate from installing or invoking a Skill.

Harness's filesystem provider documents `.dsh/skills` as a project Skill root. It also recognizes `.agents/skills` and configured/user roots, but the project-local `.dsh/skills` path is the least ambiguous place to start. The provider discovers a one-level directory bundle (`<root>/<name>/SKILL.md`) or flat `<name>.md`; it does not recursively discover nested bundles.

## Use it

For deliberate invocation, enter the Skill name as a slash command in a client that supports Harness Skill invocation:

```text
/reasoning-workflow Does this after-school tutoring programme improve maths outcomes, for whom, and what evidence could change the answer?
```

For a project-design question:

```text
/reasoning-workflow Before coding, inspect this workspace and compare feasible offline-first backup and restore designs. Do not edit files yet.
```

For a bounded task:

```text
/reasoning-workflow Answer this stable question briefly. Use only the supplied facts; do not browse unless a key fact is uncertain.
```

Harness documents `/name` invocation in its model-facing Skill integration; the exact UI and availability depend on the active client/profile. If slash invocation is unavailable, ask the agent in plain language to use the `reasoning-workflow` Skill, provided the Skill catalog and loader are visible. Automatic matching is host-dependent and best-effort: the Skill text cannot force its own activation.

The workflow chooses relevant evidence methods and proportionate effort. “Ultra” is a workflow-depth request, not a model switch, an instruction to use every tool, or permission to edit/publish/execute. For example:

```text
/reasoning-workflow Use Ultra depth to investigate whether this recovery feature is needed and whether this repository can support it safely. Keep need evidence separate from engineering feasibility.
```

## Adapt it to your Harness workspace

- **Keep the entry and references together.** The main `SKILL.md` uses relative links to supporting files. If you intentionally adapt the instructions, preserve these references or update them alongside the change.
- **Prefer workspace-local customization.** Put project-specific constraints and accepted conventions in a separate local Skill or your trusted Harness instructions rather than editing shared upstream methods for one project.
- **Keep permissions outside the Skill.** Harness's active permission policy and approval UI govern file edits, commands, and external actions. The workflow's depth or wording does not grant them.
- **Use a native plugin only for actual integration code.** A native DSH plugin requires the official TypeScript/Cordis plugin contract and package/manifest shape. This repository does not ship one; no undocumented plugin API is assumed.
- **For a different Harness composition**, check the official docs for which skill packages are mounted. A folder on disk alone does not prove that the current agent can discover or load it.

## Smoke test

Use this read-only prompt after installation:

```text
/reasoning-workflow Inspect this workspace's top-level project guide. State the file you actually read and one specific constraint it gives. Do not edit files or run commands.
```

A useful smoke-test result should identify the actual project guide and a verifiable detail from it, without claiming a write or broader research. If the agent cannot see the file, first confirm the selected workspace root and that the complete Skill bundle is under `.dsh/skills/`. Then check that the active profile exposes Skill discovery/loading and that the Skill appears in its catalog or command suggestions.

This checks one installation path in one current Harness setup; it is not a cross-version host compatibility test or evidence that the model always follows the Skill.

## Compatibility at a glance

| Environment | Installation shape | Invocation / discovery | What this repository supplies |
|---|---|---|---|
| DeepSeek Harness | Full Portable directory at project `.dsh/skills/reasoning-workflow/` | Native filesystem Skill discovery; `/reasoning-workflow` where the client/profile exposes user Skill commands; model loading requires the Skill tool path | Markdown Skill bundle; not a DSH Cordis plugin |
| Codex | Full Portable directory in `.agents/skills/reasoning-workflow/` | Host-native Skill discovery/invocation | Portable bundle |
| Claude Code | Full Portable directory in `.claude/skills/reasoning-workflow/` | Host-native Skill discovery/invocation | Portable bundle |
| Other Skills-compatible hosts | Use the host's documented Skill directory and activation rules | Varies by host and client | Portable Markdown instructions; no guarantee of implicit activation |

Paths and client behavior can change. Confirm against the host's current official documentation before rollout.

## Official references

- [DeepSeek Harness repository and current quickstart](https://github.com/deepseek-ai/deepseek-harness)
- [DeepSeek Harness Web UI quickstart](https://deepseek-harness.github.io/deepseek-harness/en/guide/quickstart)
- [Official local filesystem Skill provider contract](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)
- [Official Skill registry/provider overview](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/README.md)
- [Official model-facing Skill catalog, loader, and `/name` behavior](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.md)
- [Official native plugin publishing guide](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish)
- [Official third-party plugin-market guide](https://deepseek-harness.github.io/deepseek-harness/en/guide/plugin-market)
