# DeepSeek Harness Plugin — Install & Use

> A native Cordis bundle that registers the repository’s Reasoning Workflow as a bundled Harness Skill. It packages the complete Skill runtime tree; it does not add tools, grant permissions, or change the host’s approval policy.

[简体中文](DEEPSEEK_HARNESS.zh-CN.md) · [Project README](../README.md) · [Architecture](../skills/reasoning-workflow/docs/TECHNICAL_ARCHITECTURE.md)

## Install from this repository

Prerequisites: an installed DeepSeek Harness `dsh` CLI and `pnpm` available on `PATH` (the CLI forwards plugin management to pnpm). From the repository root, install the local bundle into the profile you use:

```sh
dsh plugin --profile default add ./integrations/deepseek-harness
```

Replace `default` with your profile name if needed. The command adds the bundle to that profile; it does not publish anything to npm or the Plugin Market. To inspect the resolved profile configuration:

```sh
dsh --profile default --dump-config
```

Look for `reasoning-workflow-deepseek-harness` in the plugin list. Then start or restart that profile in your normal Harness client so the updated composition is active. If the checkout is elsewhere, run the install command from the repository root or use the corresponding absolute path.

## Use the Skill

Ask for it by name, or use the client’s `/reasoning-workflow` command when exposed by the active Harness Skill consumer:

```text
/reasoning-workflow Use Ultra depth to compare the strongest explanations for this result. Identify what evidence would distinguish them, check the most decisive sources, and state what remains uncertain.
```

The provider advertises the Skill for both model and user invocation. Automatic matching is decided by Harness and the model; explicit invocation is more reliable. “Ultra” means a deeper, iterative research workflow—not a model switch, a request to use every available tool, or permission to make edits or external commitments. Harness permissions and confirmation controls remain authoritative.

A read-only first check after installation:

```text
/reasoning-workflow Read the repository README and tell me one concrete project constraint it states. Do not edit files or run commands.
```

If it is not offered, inspect the selected profile with `--dump-config`, confirm the bundle row is present, and ensure the profile includes the standard Skills registry and model-facing Skill consumer. A custom minimal profile may omit those host services; the plugin cannot provide them by itself.

## What is in the bundle

`integrations/deepseek-harness/` is a real `dsh.bundle` package. Its Cordis plugin registers a native `SkillProvider`; the provider serves the bundled `SKILL.md` and exposes the adjacent references, families, schemas, scripts and assets through the Skill resource base. The embedded Skill is a copy of this repository’s Portable runtime files, so resync it after changing the canonical Skill:

```sh
pnpm --dir integrations/deepseek-harness run sync-skill
pnpm --dir integrations/deepseek-harness test
```

The test checks that the provider registers the bundled Skill and that its entry text matches `skills/reasoning-workflow/SKILL.md`. The bundle is distributed in this repository; it is not yet listed in the Harness Plugin Market or published as an npm package.

## Official references

- [Harness: package and install a plugin bundle](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish)
- [Harness: Plugin Market](https://deepseek-harness.github.io/deepseek-harness/en/guide/plugin-market)
- [Harness Skill provider registry](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/README.md)
- [Harness bundled Skill provider example](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/experimental/skill-badge/src/index.ts)
- [Reasoning Workflow Portable Skill](../skills/reasoning-workflow/SKILL.md)
