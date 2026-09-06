Reasoning Workflow

A general-purpose governing workflow for how AI agents understand, reason, research, decide, act, and verify.

Reasoning Workflow is designed for substantive agent work: answering questions, investigating uncertain problems, analyzing systems, writing, planning, diagnosing, comparing, forecasting, recommending, designing, implementing, auditing, modifying persistent state, and verifying outcomes.

It began as an attempt to build a better Deep Research workflow.

The problem quickly turned out to be larger than research.

A capable agent should not simply receive a prompt, match keywords, call tools, and produce an output. It should first understand what problem it is solving, construct a revisable model of that problem, identify what its conclusions depend on, determine what information actually matters, route work to specialist capabilities when necessary, and know what must be true before the task can legitimately be considered complete.

That is what Reasoning Workflow is intended to govern.

Understand before acting.
Model before retrieving.
Research what can change the answer.
Preserve what conclusions depend on.
Verify before declaring completion.

⸻

What this is

Reasoning Workflow is a general-purpose orchestration and reasoning layer for AI agents.

It is meant to sit above specialist capabilities rather than replace them.

                    ┌─────────────────────┐
                    │  Reasoning Workflow │
                    └──────────┬──────────┘
                               │
             understand · model · reason
               research · decide · verify
                               │
       ┌───────────────┬───────┼────────┬───────────────┐
       │               │       │        │               │
     Coding       Product    Data      PDF          Research
                  Design    Analysis              / Retrieval
       │               │       │        │               │
       └───────────────┴───────┼────────┴───────────────┘
                               │
                         User outcome

The workflow governs questions such as:

* What is the user actually asking?
* What kind of epistemic task is this?
* What is already known?
* What is merely assumed?
* Which premises does the conclusion depend on?
* What relationships or mechanisms matter?
* What competing explanations exist?
* What uncertainty could materially change the answer?
* Is external research actually necessary?
* What evidence would distinguish between alternatives?
* Which specialist skill or tool should perform the next operation?
* What changed after execution?
* What became stale?
* What must be verified?
* Is the task truly complete?

The specialist capability performs the domain-specific operation.

Reasoning Workflow governs the reasoning around it.

⸻

Why this exists

Agent workflows often fail in two opposite directions.

1. Research without understanding

A user asks a question.

The agent extracts a few nouns and immediately searches them.

prompt
→ keywords
→ search
→ more sources
→ summary

This can look rigorous while missing the real problem.

The relevant evidence may exist several causal steps away from the words used in the prompt. Important variables may be upstream causes, common causes, mediators, constraints, feedback loops, lagging effects, substitutes, or hidden assumptions.

A large number of sources cannot repair a badly framed question.

2. Process without reasoning

The opposite failure is turning every task into:

plan
→ execute
→ verify
→ close

before sufficiently understanding the problem.

This creates procedural discipline while weakening inquiry.

A question becomes a project.

A hypothesis becomes a requirement.

A preliminary interpretation becomes a decision.

A checklist replaces thinking.

Reasoning Workflow is designed to avoid both failure modes.

⸻

One governing workflow for substantive agent work

The workflow can govern many different classes of tasks.

Questions
Analysis
Research
Explanation
Diagnosis
Comparison
Writing
Planning
Recommendation
Forecasting
Decision support
Design
Coding
Implementation
File modification
Audit
Verification
Persistent projects
Consequential change

These tasks do not all require the same amount of process.

They do, however, share a common requirement:

The agent should understand what it is doing before it commits to how it will do it.

⸻

Two first-class lanes

Reasoning Workflow has two equal lanes.

A question is not a truncated project.

Answering a question is a complete task.

flowchart TD
    U[User intent] --> E[Identify epistemic task / desired outcome]
    E --> M[Build revisable problem model]
    M --> Q[Question / Reasoning Lane]
    M --> A[Action / Project Lane]
    Q --> Q1[Essence · premises · decomposition]
    Q1 --> Q2[Relationships · competing explanations]
    Q2 --> Q3[Uncertainty · reasoning · research]
    Q3 --> Q4[Challenge · recompose · answer · verify]
    A --> A1[Reasoning / decision layer first]
    A1 --> A2[Risk · change control · execute]
    A2 --> A3[Re-observe · verify · validate]
    A3 --> A4[Reconcile · effectiveness · close / reopen]
    Q4 --> O[User outcome]
    A4 --> O

Question / Reasoning Lane

understand
→ identify essence
→ model
→ premises
→ decompose / recompose
→ relationships
→ competing explanations
→ uncertainty
→ reason / research
→ challenge
→ synthesize
→ answer
→ verify

This lane is sufficient for tasks such as:

* factual questions;
* explanations;
* mechanism analysis;
* truth assessment;
* rumor verification;
* comparison;
* diagnosis;
* interpretation;
* conceptual analysis;
* technical investigation;
* forecasting;
* forming a judgment;
* decision analysis;
* open-ended research.

A difficult question can involve extensive research without becoming a project-management exercise.

Action / Project Lane

When the task requires changing persistent state, producing controlled artifacts, modifying code or files, operating tools, or implementing consequential changes, the reasoning layer extends into:

understand
→ model / research
→ decide
→ assess risk
→ govern change
→ execute
→ re-observe
→ verify
→ validate
→ reconcile
→ assess effectiveness
→ close / reopen

The Action lane extends reasoning.

It does not replace it.

⸻

The reasoning kernel

Before selecting tools, the workflow attempts to identify the real epistemic task.

The user may be asking the agent to:

establish a fact
explain a cause
judge whether something is true
compare alternatives
diagnose a failure
understand a mechanism
forecast an outcome
interpret a statement
make a recommendation
support a decision
or directly solve a problem

The first question is therefore not:

Which tool should I call?

It is:

What conclusion would actually answer the user’s question?

⸻

Build a revisable problem model

The workflow distinguishes different epistemic roles.

fact
observation
premise
assumption
hypothesis
inference
judgment
recommendation
unknown

These should not silently collapse into one another.

For example:

OBSERVATION
Sales increased after the product launch.
INFERENCE
The launch may have contributed to the increase.
HYPOTHESIS
The launch was the primary cause of the increase.
JUDGMENT
The launch was probably commercially effective.
RECOMMENDATION
Expand the campaign.

Evidence supporting the first statement does not automatically prove the last.

The problem model must remain revisable.

New evidence should be allowed to change the interpretation rather than merely accumulate support for the first plausible story.

⸻

Model-driven research

Reasoning Workflow originated from a Deep Research problem:

Agents often retrieve information before they understand what information would actually matter.

The workflow therefore prefers:

observation
→ problem model
→ premises / assumptions
→ hypotheses
→ relationships
→ material uncertainty
→ discriminating evidence
→ retrieval
→ model update

over:

prompt
→ keywords
→ more pages
→ summary

The central principle is:

Research should follow the structure of the problem, not merely the wording of the prompt.

⸻

Research starts from uncertainty

Before an important retrieval, the workflow should be able to answer:

What do I currently not know?
Why could this unknown materially change the answer?
What competing explanations are currently plausible?
What evidence would distinguish between them?
What would I do differently after learning it?

Retrieval can then serve specific purposes such as:

discover the frame
establish a premise
test a mechanism
distinguish alternatives
resolve an entity or version
estimate magnitude
check recency
falsify a conclusion

Research is therefore not measured primarily by source count.

The target is information gain.

⸻

Frame uncertainty vs answer uncertainty

Not all uncertainty is the same.

Answer uncertainty

The problem is correctly framed, but the answer is unknown.

question known
→ answer unknown

More evidence may solve the problem.

Frame uncertainty

The current understanding of the problem itself may be wrong or incomplete.

problem space uncertain
→ orient
→ expand
→ map
→ identify structure
→ then focus

When frame uncertainty is high, immediately narrowing to literal keyword search can produce a deeply researched answer to the wrong question.

⸻

Decompose — then recompose

Complex questions often need decomposition.

But decomposition is useful only if the pieces can reconstruct the original problem.

Reasoning Workflow therefore applies a recomposition test:

If every subquestion were answered perfectly, would those answers be sufficient to answer the parent question?

If not, the decomposition may be:

* incomplete;
* overlapping;
* at inconsistent analytic levels;
* missing dependencies;
* aimed at the wrong abstraction.

The objective is not checklist-style MECE compliance.

The objective is explanatory sufficiency.

⸻

Mechanism before taxonomy

Classification can be useful.

But categorization should normally follow understanding rather than replace it.

A useful progression is:

concrete observations
→ recurring patterns
→ consequential relationships
→ mechanism / essence
→ abstraction / taxonomy

A label compresses a model.

It should not become the model.

⸻

Induction, abduction, and deduction

The workflow treats several reasoning operators as complementary.

Induction

observations
→ pattern
→ tentative generalization

Abduction

observation
→ possible explanations
→ competing hypotheses

Deduction

hypothesis / mechanism
→ predicted consequence
→ testable observation

A stronger reasoning loop is therefore:

observation
→ induction / abduction
→ competing hypotheses
→ deduction
→ discriminating predictions
→ evidence
→ revision

This helps prevent:

first intuition
→ search for supporting evidence
→ confidence increases

without meaningful hypothesis competition.

⸻

Relationship reasoning

“Related to” is too weak for serious analysis.

The workflow distinguishes relationships such as:

causes
correlates_with
depends_on
enables
constrains
mediates
moderates
precedes
is_part_of
is_example_of
is_alternative_to

Depending on the problem, it may also explore:

upstream causes
common causes
downstream consequences
mediators
feedback loops
time lags
thresholds
adaptation
expectations
path dependence
confounding
selection effects
reverse causality
substitutes
complements
buffers

This is particularly important in problems where the relevant answer cannot be found by searching the literal nouns in the prompt.

Relationship exploration is also pruned.

A branch is worth pursuing when resolving it could materially change:

interpretation
explanation
prediction
judgment
decision
or action

⸻

Competing explanations

For important explanatory claims, the workflow asks:

What else could produce the same observation?
What would each explanation predict differently?
Which evidence best distinguishes them?
What evidence would make the current explanation less plausible?
Which premise, if false, would reverse the conclusion?

Research becomes stronger when it searches for discriminating evidence, not merely additional confirming material.

Ten sources repeating the same proposition may add less value than one observation capable of distinguishing two competing mechanisms.

⸻

Source quality means “position to know”

Source evaluation is not a simple prestige ranking.

The workflow asks:

Is this source actually in a position to know this specific proposition?

For example:

Source	Often strong for	Often weak for
Official institution	official rules, announcements, formal specifications	independent evaluation of itself
Company	product specifications, internal announcements	unbiased assessment of real-world product quality
Journalist	reported events, sourced investigation	unsourced claims about hidden internal mechanisms
Research paper	measured relationships under its design	conclusions outside the measured scope
User community	real experiences, edge cases, failure modes	population-wide incidence
Secondary summary	orientation and discovery	replacing the primary evidence it summarizes

The question is not merely:

Is this source authoritative?

It is:

Authoritative about what?

⸻

Structured uncertainty

Uncertainty should not collapse into words such as:

maybe
probably
unclear

Reasoning Workflow distinguishes uncertainty sources such as:

missing evidence
source conflict
measurement uncertainty
definition / scope mismatch
premise uncertainty
model uncertainty
causal uncertainty
future behavioral uncertainty
external-variable uncertainty

Different uncertainty types imply different actions.

For example:

missing evidence
→ retrieval may help
definition mismatch
→ clarify the construct
premise uncertainty
→ challenge the dependency
causal uncertainty
→ compare mechanisms
future uncertainty
→ scenarios / signposts / monitoring

Not every uncertainty must be eliminated.

Some should be bounded, disclosed, monitored, or explicitly retained.

⸻

Challenge is part of normal reasoning

For conclusions carrying material weight, the workflow asks proportionately:

What evidence would make me change my answer?
Which premise, if false, would break the conclusion?
Is there a counterexample?
Does another explanation fit the same evidence?
Am I treating sequence or correlation as causation?
What happens if the main assumption is wrong?

Simple questions may pass this stage almost immediately.

Consequential conclusions require deeper challenge.

⸻

Adaptive depth

Reasoning Workflow is designed to be broadly applicable without becoming a fixed procedural ceremony.

It separates five dimensions of depth.

Dimension	Core question
Reasoning breadth	How much of the problem space, mechanism, relationship structure, and alternative space must be explored?
Evidence depth	How much external observation or retrieval is necessary?
Challenge depth	How aggressively should counterevidence, alternatives, and reversal conditions be tested?
Verification depth	How much checking is needed before accepting the result?
Governance depth	How much traceability, authorization, reversibility, monitoring, and effectiveness control is required?

A simple task may remain:

understand
→ reason
→ answer
→ check

A difficult task may expand into:

orient
→ model
→ decompose
→ inspect relationships
→ form competing explanations
→ research
→ challenge
→ recompose
→ decide
→ verify

A consequential persistent task may additionally require:

change control
→ execution
→ state synchronization
→ artifact validation
→ effectiveness assessment
→ closure / reopen

The governing principle is:

Rigor is not ceremony.

Complexity comes from the problem.

Not from the framework having many modules.

⸻

Stop research by marginal information gain

Research should not stop because the agent has reached:

5 searches
10 sources
20 pages

It should stop when another feasible research action is unlikely to materially improve the answer relative to its cost.

A useful question is:

If I learned the answer to the next unresolved question, is there a meaningful chance I would change the core explanation, judgment, forecast, or decision?

If not, continued retrieval has low expected value.

⸻

Decision quality is not belief quality

Many substantive tasks eventually ask:

What should I do?

That is not the same question as:

What is true?

Reasoning Workflow separates:

evidence
→ inference
→ belief / judgment

from:

objective
→ alternatives
→ constraints
→ consequences
→ trade-offs
→ uncertainty
→ robustness / sensitivity
→ reversibility
→ opportunity cost
→ value of more information
→ recommendation

A belief can remain uncertain while a decision is robust.

A fact can be highly certain while the correct decision remains ambiguous because the user’s objectives or trade-offs are unclear.

The workflow therefore avoids silently treating value judgments as evidence-derived facts.

When important preferences are unknown, conditional recommendations may be more appropriate:

If X matters most → choose A.
If Y matters most → choose B.

⸻

Measurement validity is not decision relevance

A correctly measured quantity can still be the wrong thing to optimize.

The workflow distinguishes:

construct
→ operational measure
→ measurement validity
→ decision relevance

Examples:

large market
≠ automatically attractive market
high benchmark score
≠ automatically better real-world task performance
more engagement
≠ automatically more user value
sales growth
≠ automatically positive net value

The workflow asks both:

Does the proxy actually measure the construct?

and:

Even if it does, how much should that construct matter to the final decision?

⸻

Specialist skills remain specialist

Reasoning Workflow is not intended to replace domain-specific skills.

It should compose with them.

Reasoning Workflow + Coding
Reasoning Workflow + Product Design
Reasoning Workflow + Data Analysis
Reasoning Workflow + PDFs
Reasoning Workflow + Spreadsheets
Reasoning Workflow + Research
Reasoning Workflow + Computer Use

The governing workflow decides:

what the actual objective is
what is known vs assumed
what evidence is missing
which relationships matter
what specialist capability is needed
what changed after the operation
what became stale
what must be verified
what counts as complete

The specialist capability performs the specialized work.

This distinction is important.

A universal governing workflow does not mean one Skill should contain every domain capability.

It means the same reasoning architecture can govern many different domains.

⸻

Persistent work and canonical state

Some tasks end with an answer.

Others continue across many actions, artifacts, observations, decisions, or sessions.

For persistent work, Reasoning Workflow can maintain a canonical current-state representation covering concepts such as:

objective
scope
requirements
acceptance criteria
questions
answers
observations
evidence
premises
assumptions
hypotheses
uncertainties
relationships
inferences
judgments
recommendations
decisions
risks
actions
artifacts
verification
effectiveness
stale items
blocked items
last completed action
next safe action

The distinction is:

PRESERVED HISTORY
raw inputs
observations
user steering
state-changing events
        │
        ▼
CANONICAL CURRENT STATE
        │
        ▼
DERIVED REPRESENTATIONS
reports
code
documents
slides
UI
other artifacts

The canonical state answers:

What should the agent currently believe and act from?

Preserved history answers:

How did the work arrive here?

⸻

Machine-enforceable semantics

Reasoning principles become more useful when important structural invariants can also be checked by machines.

Two principles guide the semantic layer:

Declared state is input. Effective state is computed.

Validators certify structural admissibility, not epistemic truth.

For example, a record may still declare:

status = current

while an upstream premise has already been invalidated.

The effective state can therefore become:

Premise invalidated
        ↓
Inference stale
        ↓
Judgment stale
        ↓
Recommendation recompute
        ↓
Artifact stale
        ↓
Verification rerun

The purpose is not to let a formal validator decide what is true in the real world.

The purpose is to make it harder for an obviously stale, incomplete, contradictory, or structurally unsupported reasoning state to masquerade as current and complete.

⸻

Typed semantic records

Persistent state can use typed records including:

Epistemic

Question
Answer
Observation
Evidence
Premise
Assumption
Hypothesis
Uncertainty
Relationship
Inference
Judgment

Decision

Objective
Constraint
Alternative
Consequence
Measurement
Recommendation
Decision

Runtime

Requirement
Risk
Action
Artifact
Verification
Effectiveness
Raw / Derived Record
Event

Typed references make relationships between these records explicit.

This enables structural checks such as:

premise_refs
must resolve to Premise records
question_refs
must resolve to Question records
verification_refs
must resolve to Verification records

rather than treating every ID as an arbitrary string.

⸻

Closure is different from stopping

An agent stopping work does not prove that a task is complete.

For the Question / Reasoning Lane, closure can depend on conditions such as:

root question answered or bounded
material child questions dispositioned
recomposition complete
question drift checked
material uncertainty resolved / bounded / irreducible
decisive dependencies current
current answer available

For persistent Action / Project work, closure may additionally require:

material requirements satisfied
blocking risks dispositioned
required artifacts current
verification passed
delivery state reconciled
effectiveness checked where required

The intended distinction is:

agent stopped

versus:

task is admissible for closure

⸻

System invariants

For substantive persistent work, Reasoning Workflow aims to preserve eight system properties.

Invariant	Meaning
Traceable	Important conclusions and outputs can be traced to their basis
Readable	A human or successor agent can understand the current state
Synchronized	Upstream changes update or invalidate dependent state
Original-preserving	Raw evidence remains distinguishable from transformations and inference
Complete	Closure checks the original question, requirements, blockers, artifacts, and verification
Consistent	Canonical state and derived representations can be reconciled
Durable / recoverable	Persistent work can checkpoint, resume, and hand off where supported
Fast / proportionate	Heavy formal machinery activates only when it adds material value

These are system properties.

They are not instructions to create a large state file for every simple question.

⸻

Semantic validation stack

The machine layer is organized conceptually into several validation layers.

1. Type validity
2. Graph validity
3. Effective-state computation
4. Closure semantics
5. Runtime integrity
6. Decision-quality structure
7. Behavioral evaluation

Type validity

Checks:

record shape
enums
typed references
local invariants

Graph validity

Checks:

dependency relationships
cycle policies
lineage
reference integrity

Effective-state computation

Handles:

stale propagation
invalidation
supersession
recomputation

Closure semantics

Handles:

epistemic closure
runtime closure
delivery reconciliation

Runtime integrity

Can check structures such as:

event continuity
raw lineage
artifact references
hashes / fingerprints where available

Decision structure

Makes explicit structures such as:

objectives
alternatives
constraints
consequences
trade-offs
uncertainty
value of information

Behavioral evaluation

Can evaluate public observables such as:

expected events
forbidden events
expected final state
expected findings

without requiring private chain-of-thought.

⸻

Raw evidence and lineage

Where the environment supports durable artifacts, original inputs should remain distinguishable from transformations.

RAW-001 original image
│
├── DER-001 crop
├── DER-002 enhancement
│      └── OCR-001
│
└── OBS-004 visual observation
       └── INF-003 inference

The intended principle is:

Transformations create descendants, not silent replacements.

The same applies to:

original document
→ working copy
→ revised artifact
→ delivered artifact

and:

retrieved page
→ extracted passage
→ observation
→ inference
→ judgment

⸻

Behavioral regression

The repository includes behavioral specifications designed to test workflow behavior across different task classes.

Examples include:

trivial questions
ambiguous questions
deep open inquiry
needle search
rumor verification
human-statement interpretation
conflicting evidence
stale sources
premise invalidation
question drift
decomposition / recomposition
interrupted work
user steering
partial failure
persistent change
ineffective change
requirement omission
multi-artifact drift
specialist-skill handoff

These are intentionally treated as:

regression specifications, not proof of model intelligence.

A run can expose observable events and final state without recording hidden chain-of-thought.

⸻

Repository structure

.
├── .codex-plugin/
│   └── plugin.json
│
├── .github/
│   └── workflows/
│       └── validate.yml
│
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── PRIVACY.md
├── TERMS.md
│
└── skills/
    └── reasoning-workflow/
        ├── SKILL.md
        ├── README.md
        │
        ├── agents/
        │   └── openai.yaml
        │
        ├── assets/
        │
        ├── references/
        │   ├── problem-framing-and-effort.md
        │   ├── inquiry-and-research.md
        │   ├── reasoning-structure-and-decomposition.md
        │   ├── relationships-and-systems.md
        │   ├── evidence-and-provenance.md
        │   ├── hypotheses-and-bias-control.md
        │   ├── decision-and-recommendation.md
        │   ├── measurement-and-operationalization.md
        │   ├── semantic-state-contract.md
        │   ├── synchronization-and-recovery.md
        │   ├── synthesis-execution-and-verification.md
        │   └── ...
        │
        ├── schemas/
        │
        ├── scripts/
        │
        └── tests/

The public repository README explains the project.

The runtime entry point is:

skills/reasoning-workflow/SKILL.md

Detailed modules are loaded progressively from references/.

Machine-readable contracts live under schemas/.

Deterministic semantic checks live under scripts/.

Behavioral and validator regression material lives under tests/.

⸻

Quick start

Use as a Skill

The Skill root is:

skills/reasoning-workflow/

A compatible agent environment can install or load that directory as a Skill.

The root SKILL.md acts as the governing router.

Detailed references should be loaded progressively rather than injecting the entire package into context at once.

⸻

Use in a normal chat

When the Skill is attached as a file rather than formally installed, a suitable bootstrap instruction is:

Read reasoning-workflow/SKILL.md and use it as the governing workflow for subsequent substantive tasks in this conversation.
Apply the core reasoning process to substantive questions, but only activate heavy research, persistent state, change governance, semantic validation, or specialist references when the task actually warrants them.
Load references, schemas, and scripts progressively rather than all at once.

⸻

Use as a skill-only Codex plugin

The repository also contains:

.codex-plugin/plugin.json

with the Skill directory exposed through:

./skills/

The Skill itself remains:

reasoning-workflow

The plugin wrapper is a distribution mechanism.

It does not change the internal reasoning architecture.

⸻

Validation

Python 3.10+ is recommended.

Semantic validators use jsonschema.

From the Skill directory:

cd skills/reasoning-workflow
python -m pip install -r scripts/requirements.txt
python scripts/validate_skill.py .
python scripts/validate_links.py .
python -m unittest tests.test_validators -v

The validation suite is intended to check structural properties such as:

Skill/package integrity
reference navigation
JSON Schema validity
typed-reference compatibility
dependency semantics
cycle policy
transitive invalidation
closure blockers
state ↔ delivery reconciliation
event continuity
raw lineage
artifact and verification references

Passing these checks does not prove that the real-world answer is true.

It means that the represented reasoning or work state satisfies the structural rules the workflow claims to enforce.

⸻

What Reasoning Workflow does not claim

Reasoning Workflow does not claim that:

* every question requires research;
* every task requires persistent state;
* more sources automatically produce a better answer;
* more process automatically produces better reasoning;
* every relationship is causal;
* every uncertainty can or should be eliminated;
* validators can prove epistemic truth;
* a generic governing workflow can replace domain expertise;
* specialist skills should be absorbed into one giant universal tool;
* private chain-of-thought should be recorded for auditability.

The objective is not maximal process.

The objective is better problem understanding and stronger structural integrity at the level appropriate to the task.

⸻

Design philosophy

Several principles recur throughout the project.

Understand before acting

Do not let tool availability decide what the problem is.

Model before retrieving

Search because something important is unknown.

Not because “research” sounds rigorous.

Research the problem, not the keywords

The important evidence may lie in mechanisms, dependencies, and adjacent variables not explicitly named by the user.

Mechanism before taxonomy

Understand the phenomenon before compressing it into a category.

Relationships before isolated facts

Real systems are often explained by interactions, not individual variables.

Competing explanations before confidence

A conclusion becomes stronger when plausible alternatives fail, not merely when confirming evidence accumulates.

Information gain over source count

Prefer evidence capable of changing the model.

Recomposition after decomposition

Solving subquestions is useful only if they reconstruct the parent problem.

Belief quality is not decision quality

Knowing what is true and deciding what to do are related but different semantic layers.

Measurement validity is not decision relevance

A metric may measure something correctly without measuring what matters.

Effective state over declared state

A conclusion does not remain current merely because its own record says current.

Closure over stopping

The agent stopping is not proof that the task is complete.

Specialist skills remain specialist

A universal workflow should orchestrate domain capabilities, not erase their boundaries.

Proportional rigor

The workflow should become more rigorous because the problem demands it.

Not because the framework contains many components.

⸻

Project direction

The main reasoning architecture is intentionally becoming more stable.

Future development should favor stronger implementation of the ideas already present rather than continuously adding more methodology prose.

High-value areas include:

semantic contracts
typed state
dependency semantics
question / answer binding
recursive closure
temporal validity
artifact / state synchronization
verification provenance
event integrity
raw lineage
decision-quality enforcement
behavioral evaluation
runtime integrations

The long-term objective is not to formalize truth.

It is to make it harder for an agent to:

answer the wrong question
research irrelevant evidence
hide important assumptions
ignore competing explanations
use stale premises as current
let artifacts drift from decisions
claim verification without coverage
or declare incomplete work finished

⸻

Contributing

See CONTRIBUTING.md.

Useful contributions include:

* real failure cases;
* semantic-contract improvements;
* validator correctness;
* dependency and invalidation semantics;
* reasoning and research edge cases;
* behavioral regression scenarios;
* specialist-skill interoperability;
* runtime integrations;
* documentation improvements.

When proposing a new principle, prefer identifying a concrete failure mode that the existing workflow cannot adequately:

represent
detect
reason about
recover from
or prevent

rather than adding methodology for its own sake.

⸻

中文简介

Reasoning Workflow 是一个面向 AI Agent 的通用 governing workflow。

它最初来自一个 Deep Research 问题：

为什么 Agent 明明搜索了很多资料，最后还是可能没有真正理解问题？

后来我们发现，这个问题并不属于 Research 本身。

几乎所有严肃的 Agent 任务都会面对类似的问题：

用户真正想解决什么？
当前问题是怎么被定义的？
哪些是事实，哪些只是前提或假设？
事物之间有哪些真正重要的关系？
还有哪些竞争解释？
什么未知信息真的会改变结论？
现在应该继续推理、搜索，还是调用专业 Skill？
执行以后什么状态发生了变化？
哪些旧结论因此失效？
什么东西必须重新验证？
什么时候才算真正完成？

于是这个项目逐渐从 Deep Research workflow 演化成了一个可以治理：

问答
分析
研究
写作
规划
诊断
比较
推荐
预测
决策
设计
编码
实施
审计
验证
以及复杂长期任务

的通用工作流。

它有两条平级 Lane。

Question / Reasoning Lane

understand
→ identify essence
→ model
→ premises
→ decompose / recompose
→ relationships
→ competing explanations
→ uncertainty
→ reason / research
→ challenge
→ synthesize
→ answer
→ verify

这里非常重要的一条原则是：

回答一个问题本身就是一个完整任务。

并不是所有问题都应该被强行变成项目管理。

Action / Project Lane

当任务需要真正改变 persistent state，例如：

写代码
修改文件
生成 artifact
执行操作
实施方案
完成项目

Reasoning Lane 才继续扩展为：

risk
→ change control
→ execute
→ re-observe
→ verify
→ validate
→ reconcile
→ effectiveness
→ close / reopen

Reasoning Workflow 也不是为了替代 Coding、Product Design、PDF、Spreadsheet、Data Analysis 等专业 Skill。

它位于更上层：

负责理解问题、组织推理、决定研究方向、选择专业能力、整合结果、管理状态并判断任务是否真正完成。

另一个核心思想是：

Research should follow the structure of the problem, not merely the wording of the prompt.

也就是说：

用户问 A
≠
立刻搜索 A

更合理的过程可能是：

理解问题
→ 建立模型
→ 找前提
→ 找关系
→ 提出竞争解释
→ 找 material uncertainty
→ 判断什么证据能区分这些解释
→ 再去检索
→ 更新模型

这也是为什么 Reasoning Workflow 特别强调：

因果关系
依赖关系
中介变量
反馈
时间滞后
阈值
适应
路径依赖
反向因果
替代关系
共同原因

等系统结构。

同时它又是自适应的。

简单问题可以只有：

理解 → 推理 → 回答 → 检查

复杂问题才逐渐增加：

Reasoning breadth
Evidence depth
Challenge depth
Verification depth
Governance depth

因此：

Rigor is not ceremony.

严谨并不意味着所有任务都必须跑完整流程。

当任务进入持久化或复杂执行阶段，项目还可以进一步使用 typed state、dependency graph、stale propagation、closure gate、delivery reconciliation 等机器语义。

其中一个核心原则是：

Declared state is input. Effective state is computed.

例如一个 premise 已经失效，那么依赖它的：

Inference
Judgment
Recommendation
Artifact
Verification

都可能需要重新计算、失效或重新验证。

但这里有一个明确边界：

Validators certify structural admissibility, not epistemic truth.

机器 validator 可以检查：

类型是否正确
引用是否合法
依赖是否自洽
旧前提是否继续被当作 current
任务是否还有 material blocker
delivery 是否与 canonical state 一致

但它不能代替现实世界证据，也不能证明一个结论一定是真的。

Reasoning Workflow 最终想解决的不是：

“如何让 Agent 跑更多流程？”

而是：

如何让 Agent 在各种严肃任务中，更清楚地知道自己正在解决什么、结论依赖什么、还缺什么、什么时候应该继续调查、什么时候应该调用专业能力，以及什么时候才真的可以说：完成。

⸻

License

No open-source license has been declared yet.

Public availability of this repository should not be interpreted as an automatic grant of permission to reuse, redistribute, repackage, or create derivative distributions.

Add an explicit license only when the intended reuse policy has been decided.
