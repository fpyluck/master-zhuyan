# MasterZhuyan adaptive router

Use this file only after `SKILL.md` has selected the merged deep-research plus longform route, or a delivery/limitation note because file-backed output is unavailable or intentionally stopped. `SKILL.md` `Output policy` remains authoritative.

## 1. Named prep-template overlay

Template lookup is an explicit-style signal, not topic matching. Load `.masterzhuyan/prep_templates/<name>.md` when the request names a saved style through patterns such as `X式讲解`, `X式输出`, `X教案`, `X模板`, `用X风格`, or `按X教案`.

Activation requires one of the saved template's explicit style aliases in the current request. Ordinary topic words stay source/topic intent.

The loaded template flows into the planning layer as a soft overlay: source priority, learner assumptions, explanation taste, safety posture, chapter emphasis, and anti-overconstraint notes. Research, evidence, Knowledge Model locking, and chapter planning remain the single route.

## 2. Chapter emphasis

User wording flows into chapter `purpose`, `required_anchors`, examples, and ordering inside the single route.

| Intent signal | Information flows to |
| --- | --- |
| remember, review, exam points, mnemonics, `帮我记` | memory purpose: core anchors, retrieval hooks, mnemonic or logic line, high-frequency points, 30-second recap |
| why, how, mechanism, principle, derivation, judgment logic, `讲懂` | understanding purpose: reference frame, disturbance, mechanism, consequence, recognition, handling, boundary |
| compare, distinguish, identify, `怎么区分`, A 与 B | comparison purpose: decisive criteria, mechanism differences, use cases, traps, one-sentence distinctions |
| traps, mistakes, confusing points, wrong-question review, risk boundaries | error-repair purpose: wrong pattern, correct understanding, trigger clue, repair method |

When several signals apply, `chapter_plan` includes the relevant purposes and orders them by the user's wording or by the learning flow.

## 3. Source intake

Pasted text:
Preserve the user's wording when it carries technical meaning. Recover the hierarchy before synthesizing. If the pasted material visibly contradicts itself or contains a self-evident error, flag the issue and separate source facts from corrected or uncertainty-labeled teaching.

Image/screenshot:
Use only visible information. If a label or number is unclear, mark it rather than guessing.

Uploaded/repository files:
Inspect actual files. For multiple files, write `notes/source_map.md`:
file -> main topic -> trustworthy facts -> gaps -> output chapter.

Current/source-sensitive topics:
Use retrieval when available for guidelines, laws, policies, standards, product behavior, software versions, prices, current events, and citations. If retrieval is unavailable, separate stable concepts from uncertain specifics.

## 4. Explanation spine

Choose the mechanism-first spine that best teaches the topic. A non-causal spine is valid only when it still explains how the parts relate, change, fail, or get distinguished:

Definition-heavy topic:
problem -> definition -> elements -> boundary -> examples -> confusions

Mechanism-heavy topic:
baseline -> disturbance -> mechanism -> result -> recognition -> intervention/boundary

Classification topic:
classification purpose -> branch criterion -> categories -> distinguishing anchors -> exceptions

Procedure/skill topic:
goal -> standard -> steps -> key actions -> failure modes -> practice loop

Formula/mathematics topic:
definition -> conditions -> variables -> derivation intuition -> application -> traps

Legal/policy topic:
rule purpose -> elements -> conditions -> exceptions -> consequence -> risk boundary

Business/decision topic:
context -> objective -> variables -> trade-offs -> indicators -> execution risk

Humanities/history topic:
background -> actors/ideas -> causes -> process -> consequences -> interpretations

## 5. Depth control

Add depth when it protects a mechanism, branch criterion, threshold, exception, misconception, or transfer boundary. Keep only chapters or sections that improve understanding, memory, judgment, or reuse.
