import assert from 'node:assert/strict'
import { readFile, stat } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { test } from 'node:test'
import { apply, inject, name } from '../index.js'

const root = new URL('../', import.meta.url)
const skillDir = new URL('./skills/reasoning-workflow/', root)
const sourceDir = new URL('../../../skills/reasoning-workflow/', import.meta.url)

test('registers a bundled, user- and model-invocable reasoning-workflow Skill', async () => {
  assert.equal(name, 'reasoning-workflow-deepseek-harness')
  assert.deepEqual(inject, ['skills'])
  const registrations = []
  apply({ skills: { registerProvider: (factory) => registrations.push(factory) } })
  assert.equal(registrations.length, 1)
  const provider = registrations[0]({})
  assert.equal(provider.name, 'reasoning-workflow')
  const candidates = await provider.list()
  assert.equal(candidates.length, 1)
  const [candidate] = candidates
  assert.equal(candidate.name, 'reasoning-workflow')
  assert.equal(candidate.source, 'bundled')
  assert.equal(candidate.provider, 'reasoning-workflow')
  assert.deepEqual(candidate.invocation, { modelInvocable: true, userInvocable: true })
  assert.equal(candidate.rank, 600)
  assert.equal(candidate.resourceBase.kind, 'directory')
  assert.equal(candidate.locator.href, new URL('./skills/reasoning-workflow/SKILL.md', root).href)

  const definition = await provider.get(candidate)
  const installedText = await readFile(new URL('SKILL.md', skillDir), 'utf8')
  const canonicalText = await readFile(new URL('SKILL.md', sourceDir), 'utf8')
  const canonicalBody = canonicalText.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '').trim()
  assert.equal(definition.content, canonicalBody, 'provider must return the Skill body without YAML frontmatter')
  assert.equal(installedText, canonicalText, 'packaged Skill must match the canonical Portable SKILL.md')
  assert.ok(!definition.content.startsWith('---'), 'frontmatter must not leak into loaded instructions')
  assert.equal(definition.name, candidate.name)
  assert.equal(definition.resourceBase.path, fileURLToPath(skillDir))
})

test('ships the complete relative-reference runtime tree without test fixtures', async () => {
  for (const file of ['UPGRADE.md', 'references/runtime-and-delegation.md', 'families/deep-research.md', 'schemas/dual-verification.schema.json', 'scripts/validate_runtime.py']) {
    await stat(new URL(file, skillDir))
  }
  await assert.rejects(stat(new URL('tests/', skillDir)))
  await assert.rejects(stat(new URL('evals/', skillDir)))
})
