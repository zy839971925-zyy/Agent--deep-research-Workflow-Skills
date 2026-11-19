import { cp, mkdir, readdir, rm } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const packageDir = fileURLToPath(new URL('../', import.meta.url))
const repoDir = path.resolve(packageDir, '../..')
const sourceDir = path.join(repoDir, 'skills/reasoning-workflow')
const targetDir = path.join(packageDir, 'skills/reasoning-workflow')
const includedDirs = ['references', 'families', 'schemas', 'scripts', 'assets']

const includedFiles = ['SKILL.md', 'UPGRADE.md', 'routing-index.json', 'RELEASE.json']

await mkdir(targetDir, { recursive: true })
for (const entry of [...includedFiles, ...includedDirs]) {
  await rm(path.join(targetDir, entry), { recursive: true, force: true })
}
for (const file of includedFiles) {
  await cp(path.join(sourceDir, file), path.join(targetDir, file))
}
for (const dir of includedDirs) {
  await cp(path.join(sourceDir, dir), path.join(targetDir, dir), {
    recursive: true,
    filter: (source) => !source.split(path.sep).includes('__pycache__'),
  })
}

const actual = (await readdir(targetDir)).sort()
console.log(`Synced ${actual.join(', ')} from ${path.relative(repoDir, sourceDir)}`)
