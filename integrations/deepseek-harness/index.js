import { readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'

const PLUGIN_NAME = 'reasoning-workflow-deepseek-harness'
const PROVIDER_NAME = 'reasoning-workflow'
const SKILL_NAME = 'reasoning-workflow'
const SKILL_URL = new URL('./skills/reasoning-workflow/SKILL.md', import.meta.url)
const RESOURCE_BASE = {
  kind: 'directory',
  path: fileURLToPath(new URL('./skills/reasoning-workflow/', import.meta.url)),
}
const DESCRIPTION = 'Default silent entry for questions, research, artifacts, code, coordination and persistent projects. When available to the host, infer the relevant evidence path from each direct request, including real-world, pre-build engineering, or linked hybrid research; choose proportionate Light-to-Ultra workflow depth and load only relevant guidance. Keep the host-selected default model unless the user or host explicitly changes it. The direct user phrase “调用我的 workflow skills” explicitly selects this workflow.'
const INVOCATION = { modelInvocable: true, userInvocable: true }

// DeepSeek Harness @deepseek-ai/dsh-skill currently defines BUNDLED_SKILL_RANK as 600.
// Keep this aligned with that bundled-provider contract; engines.dsh pins the API line.
const BUNDLED_SKILL_RANK = 600

const candidate = {
  name: SKILL_NAME,
  description: DESCRIPTION,
  invocation: INVOCATION,
  provider: PROVIDER_NAME,
  source: 'bundled',
  resourceBase: RESOURCE_BASE,
  rank: BUNDLED_SKILL_RANK,
  locator: SKILL_URL,
}

async function loadSkillBody() {
  const raw = await readFile(SKILL_URL, 'utf8')
  const match = raw.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n([\s\S]*)$/)
  if (!match) throw new Error('Bundled Reasoning Workflow SKILL.md is missing valid YAML frontmatter')
  return match[1].trim()
}

const provider = {
  name: PROVIDER_NAME,
  list: () => Promise.resolve([candidate]),
  async get() {
    return {
      name: candidate.name,
      description: candidate.description,
      invocation: candidate.invocation,
      provider: candidate.provider,
      source: candidate.source,
      resourceBase: RESOURCE_BASE,
      content: await loadSkillBody(),
    }
  },
}

export const name = PLUGIN_NAME
export const inject = ['skills']

export function apply(ctx) {
  ctx.skills.registerProvider(() => provider)
}
