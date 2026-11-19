# Reasoning Workflow 3.2.0

Built as a Portable distribution on 2026-11-19. Keep the complete folder when installing. A host that supports trusted standing instructions can use the following short instruction alongside its native Skill discovery.

> For each direct request, silently use the installed reasoning-workflow entry when available. Honor explicit depth and the user's scope. Give simple tasks a direct answer. Consult specialist skills only when they change the result.

Native discovery alone cannot establish every-turn activation. To check an update, inspect the actual loaded entry or version and a real run in your host. Replacing a repository checkout does not update an already-loaded chat.

## 日常行为

- 复杂但明确的任务直接开工。遇到需要用户决定且会造成大规模返工的分歧，先查已有材料，再问决定下一步的一个问题。
- 对设计、动效和陌生工程栈，优先找已安装的专业 Skill、项目内实现或维护中的原始示例，检查版本、依赖和实际表现。
- 工程从用户入口、小范围回归、安装成品验收。研究按主张核对证据，标出同源转载、反证、适用范围和未解条件。
- 按读者和文体组织语言：可直接发送的微信、正式报告和保留作者口吻的修改稿采用不同写法。

## Evidence check

Save source text in the packet directory. For example, place the text `Eight sites reported an improvement.` in `trial.txt`, then save this JSON as `packet.json`.

```json
{
  "sources": [{"id":"trial","file":"trial.txt","origin":"register-A"}],
  "claims": [
    {"id":"C1","text":"Eight sites reported improvement.","status":"observed",
     "evidence":[{"source":"trial","quote":"Eight sites reported an improvement.","role":"support"}]},
    {"id":"C2","text":"The treatment caused the improvement.","status":"unknown","evidence":[]}
  ]
}
```

From the installed Skill folder run `python scripts/check_report_evidence.py /path/to/packet.json`. Inspect the exit code and reported origins. The checker is optional, offline and limited to the supplied UTF-8 files. A human or model still needs to judge relevance, provenance and whether the passage entails the claim. The Modular edition uses the method without this helper.

## Compatibility and reproducibility

Existing task profiles, depth signals and state formats are supported. Both routing entry points now reject unknown signals. DeepSeek Harness ships its routing index. Independent Portable installation tests no longer require the Modular tree. Cross-edition checks stay in repository-level tests. Run `python tests/run_all.py` and `python tests/check_package.py` from the extracted Portable directory after installing `scripts/requirements.txt`. Dependency-free evidence checks need only Python. See [the test report](../TEST_REPORT.md).

Design references: [Matt Pocock's requirements interview](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md), [Anthropic Skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [OpenAI Skill evaluation](https://developers.openai.com/blog/eval-skills), [GOV.UK writing guidance](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/tone-of-voice/).
