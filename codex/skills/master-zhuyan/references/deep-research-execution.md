# Deep-research execution protocol

Use this protocol as the durable form of MasterZhuyan's default research/modeling layer when source material is dense, multi-source, conflicting, or evidence-critical, or when the user explicitly requests evidence-grounded learning, systematic review, or citation-backed answers.

For simple source intake, use `references/adaptive-router.md` section 3 and keep this protocol mental. Write these artifacts only when source complexity or traceability warrants it.

## 1. Trigger conditions

Write durable deep-research execution artifacts when any of the following apply:

1. The user supplies three or more distinct source files or dense note sets.
2. The material contains visible contradictions, multiple competing frameworks, or domain-sensitive precision claims (doses, legal thresholds, clinical criteria, engineering standards).
3. The user asks for 系统整理, 循证, 研究综述, 文献综述, 证据, 系统梳理, evidence-based, or systematic coverage.
4. The topic requires separating current/guideline-dependent facts from stable conceptual knowledge.
5. A chapter plan built without evidence verification would carry real risk if a precision anchor is wrong.

For single-source or low-complexity requests, still use the research/modeling logic, but keep it mental and deliver through the normal longform container.

## 2. Phase sequence

Run silently. Each phase produces a locked artifact before the next phase begins. Do not draft chapters before the Knowledge Model is locked.

### Phase 1: Research planning

Before reading sources, define what the research must answer.

Produce `notes/research_plan.md` using the contract in `references/deep-research-output-contracts.md` section 1.

Minimum contents:
1. Knowledge questions: the specific questions this research must answer.
2. Source requirements: what source types are needed (guidelines, mechanisms, classifications, examples, exceptions).
3. Uncertainty budget: how much uncertainty is acceptable given the domain and stakes.
4. Completion criteria: when the evidence is sufficient to teach from.
5. Research nodes: dynamic nodes chosen by the planner or integrator from knowledge questions, source structure, dependency order, contradiction risk, domain precision, and teaching value. Do not force fixed chunks, a fixed count, or a scored ranking gate. If a candidate map helps clarify scope, record it as optional planning context; expand, merge, or split nodes whenever the evidence or lesson plan benefits.

Do not begin source intake until the research plan is written.

### Phase 2: Source intake and Evidence Ledger

Read all supplied sources. For each source, build a source map entry (see `references/codex-execution.md` section 2). Then extract evidence claims into the Evidence Ledger.

Produce `notes/evidence_ledger.md` using the contract in `references/deep-research-output-contracts.md` section 2.

Rules:
1. Every claim that will appear in a chapter must have a ledger entry.
2. Mark confidence honestly: `high` only when the source is unambiguous; `med` when interpretation is needed; `low` when support is thin; `inferred` when no source supports it.
3. When two sources contradict, create a `contradicted` entry for both. Do not silently pick one.
4. Do not invent ledger entries. If a knowledge question cannot be answered from supplied material, record it as `missing`.

Do not lock the Knowledge Model until the Evidence Ledger is complete.

### Phase 3: Knowledge Model

Build a structured representation of what is known, uncertain, and missing.

Produce `notes/knowledge_model.md` using the contract in `references/deep-research-output-contracts.md` section 3.

Rules:
1. Every concept in the Knowledge Model must cite at least one Evidence Ledger entry.
2. Misconceptions must include a repair anchor, not just a flag.
3. Gaps must map back to their knowledge question in the Research Planner.
4. Precision anchors (thresholds, doses, criteria, formulas) must reference their source entry directly.

Do not begin chapter planning until the Knowledge Model is locked.

### Phase 4: Chapter planning

Use `references/masterzhuyan-planning.md` section 1 with the Knowledge Model as primary input. The Knowledge Model replaces generic topic brainstorming: use its concepts, relationships, misconceptions, and precision anchors to fill the canvas fields.

Record `notes/chapter_plan.md` as in the normal longform workflow (`references/codex-execution.md` section 6).

### Phase 5: Chapter drafting

Use `references/masterzhuyan-output-contracts.md` for chapter module shapes. Each chapter may cite Evidence Ledger entries when flagging precision or uncertainty. Do not introduce source claims not present in the Evidence Ledger.

### Phase 6: Verification pass

Before merge, verify that:
1. Every precision anchor in the chapters has a matching `accepted` Evidence Ledger entry.
2. Every `contradicted` or `missing` ledger entry is either flagged in the relevant chapter or intentionally excluded with a reason in `notes/review.md`.
3. No chapter contains a claim marked `inferred` without labeling it as inference in the text.
4. The chapter plan and final draft answer the research brief's `primary_confusion` and satisfy its `success_criteria`; if not, revise the Knowledge Model or Chapter Plan before polishing.

After this verification pass, rely on longform for container validation and merge discipline. Use `references/quality-gates.md` only for extra teaching/source risks that remain unresolved.

## 3. Fallback

If Phase 1 or 2 fails because sources cannot be read, retrieval is unavailable for a current/high-risk claim, filesystem output is unavailable, or context budget cannot safely hold the chapter plan, write a limitation or handoff note and continue only with the portions that can still be file-backed and source-bounded. Do not replace the full learning deliverable with chat teaching.

If Phase 3 produces a Knowledge Model with more gaps than accepted claims, tell the user what is missing before teaching from thin evidence.
