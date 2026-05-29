# evolution log

## 2026-05-25 - upgrade-skill

- evidence used: user reported that modularized MasterZhuyan still underperformed in Codex-like use and did not reliably trigger longform-composer.
- hypothesis: performance was blocked by soft routing, overlong trigger description, ambiguous artifact responsibilities, insufficient file-inspection protocol, and lack of a local longform fallback.
- files changed: SKILL.md, agents/openai.yaml, references/router.md, references/masterzhuyan-planning.md, references/masterzhuyan-output-contracts.md, references/domain-kernels.md, references/dense-topic-scaffold.md, references/teaching-advantage-overlay.md, references/quality-gates.md, references/longform-bridge.md, references/codex-execution.md, references/regression-prompts.md, scripts/mz_longform.py, tests/test_mz_longform.py.
- validation result: pending at edit time; package and tests must pass before delivery.
- regressions checked: memory mode, understanding mode, comparison mode, longform escalation, chat-only long answer, current/source-sensitive caution.
- next improvement idea: add a small behavior test harness that checks generated outputs against regression-prompts.md with model-in-the-loop evaluation.

## 2026-05-25 performance-first revision

- mode: upgrade-skill
- evidence used: user feedback that the previous revision made behavior harder/stricter but the desired goal was better model performance.
- hypothesis: answer quality should improve more from adaptive tutor judgment, explanation exemplars, misconception repair, contrastive teaching, and taste gates than from stronger routing alone.
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/teaching-performance-playbook.md, references/exemplar-patterns.md, references/masterzhuyan-planning.md, references/quality-gates.md, references/teaching-advantage-overlay.md, references/regression-prompts.md; removed obsolete hard router reference file.
- validation result: smoke_test passed; pytest passed; package validation passed.
- regressions checked: formal memory/understanding contracts preserved; longform-composer handoff preserved; bundled longform fallback preserved; anti-overrigidity behavioral prompts added.
- next improvement idea: run side-by-side answers on a fixed benchmark set and compress the best-performing patterns into exemplar-patterns.md.

## 2026-05-25 longform-first simplification

- mode: simplify-routing
- evidence used: user explicitly requested one default route: file-backed longform for all learning requests, with chat-only only after explicit user request or unavailable files.
- hypothesis: performance should improve by removing route hesitation; memory, understanding, comparison, review, and easy-error work become chapter emphases inside one durable deliverable instead of competing answer modes.
- files changed: SKILL.md, references/adaptive-router.md, references/masterzhuyan-output-contracts.md, references/quality-gates.md, references/longform-bridge.md, references/codex-execution.md, references/exemplar-patterns.md, references/masterzhuyan-planning.md, references/dense-topic-scaffold.md, references/teaching-performance-playbook.md, references/regression-prompts.md.
- validation result: smoke_test passed; unittest discovery passed (26 tests); py_compile passed; skill consistency check had 0 failures and one registry warning because MasterZhuyan is not a collaborative skill.
- regressions checked: default longform from bare material, memory signal as chapter emphasis, understanding signal as chapter emphasis, comparison signal as chapter emphasis, explicit chat-only exception, stop-file-output exception, current/source-sensitive caution, source contradiction handling.
- next improvement idea: add a behavior harness that confirms ordinary learning prompts produce a manifest, chapters, validation note, and final/final_merged.md unless explicitly chat-only.

## 2026-05-25 named prep-template overlay

- mode: upgrade-skill
- evidence used: user reported that over-branching reduced model performance, that fixed longform output now works well, and requested a local, user-named lesson-prep prompt file that can be activated later.
- hypothesis: MasterZhuyan can gain controllable teaching direction without reintroducing router bloat by treating named lesson-prep prompts as soft attention overlays before longform chapter planning.
- snapshot: .evolution/snapshots/20260525T133310_274249Z
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/codex-execution.md, references/longform-bridge.md, references/masterzhuyan-output-contracts.md, references/masterzhuyan-planning.md, references/quality-gates.md, references/regression-prompts.md, references/prep-template-workflow.md, scripts/prep_template.py, scripts/smoke_test.py, tests/test_prep_template.py.
- validation result: smoke_test passed; pytest passed with 30 tests; py_compile passed; local_validate passed; package validation passed before archive creation.
- regressions checked: longform-first default preserved, memory/understanding remain chapter emphases, chat-only remains explicit exception, no forced mode-choice question for named styles, local template creation, explicit activation behavior.
- next improvement idea: add an optional model-evaluated benchmark comparing default MasterZhuyan vs named prep-template outputs on the same medical textbook prompt to measure whether the overlay improves focus without adding rigidity.

## 2026-05-25 generic named-template cleanup

- mode: upgrade-skill
- evidence used: user clarified that the earlier named style was only an example; any arbitrary name such as 猫, 狗, 外星人, or another label should be a user-created optional style overlay.
- hypothesis: template support should remain a low-friction attention overlay by removing example-specific templates, avoiding default template scans, and activating only on explicit style phrases.
- snapshot: .evolution/snapshots/pre_generic_template_fix_20260525.zip
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/masterzhuyan-planning.md, references/prep-template-workflow.md, references/regression-prompts.md, scripts/prep_template.py, scripts/smoke_test.py, tests/test_prep_template.py; removed the example-specific bundled prep template from the active package.
- validation result: smoke_test passed; pytest passed with 31 tests; py_compile passed.
- regressions checked: default longform remains unchanged, templates are not read on default runs, arbitrary names are supported, explicit style activation works, bare ordinary words do not activate templates.
- next improvement idea: add a tiny real-output benchmark comparing default style and one user-created style without adding any new routing branch.

## 2026-05-26 deep-research learning architecture

- mode: multi-agent upgrade-skill
- evidence used: user requested a new MasterZhuyan architecture based on ChatGPT/Gemini/Perplexity/Claude-style deep research, then explicitly asked Codex and Claude to use agent teams to implement it.
- hypothesis: MasterZhuyan should keep longform-first delivery but add conditional research artifacts for source-heavy, current, high-risk, multi-file, conflicting, or evidence-critical learning tasks: source intake, research brief, evidence ledger, knowledge model, lesson plan, quality verifier, and regression prompts.
- collaboration: Codex acted as integrator; Codex subagents produced architecture/schema/quality-regression drafts; Claude reviewed and created execution/output/agent-pattern references. Claude's preserved constraints: deep research is conditional, not a new output channel; `research_plan -> evidence_ledger -> knowledge_model -> chapter_plan` must stay sequenced; high-severity precision-anchor evidence failures block merge.
- files changed: SKILL.md, agents/openai.yaml, references/masterzhuyan-planning.md, references/codex-execution.md, references/quality-gates.md, references/regression-prompts.md, references/deep-research-architecture.md, references/deep-research-execution.md, references/deep-research-output-contracts.md, references/deep-research-agent-patterns.md, references/deep-research-quality-gates.md, schemas/source_map.schema.json, schemas/research_brief.schema.json, schemas/evidence_card.schema.json, schemas/knowledge_model.schema.json, schemas/lesson_plan.schema.json, schemas/quality_report.schema.json.
- validation result: schema JSON validation passed with jq; py_compile passed for scripts; smoke_test passed; unittest discovery passed with 26 tests; skill_consistency_check passed with 0 failures and one expected registry warning because MasterZhuyan is not a collaborative skill. `python3 -m pytest` could not run because pytest is not installed in this environment.
- regressions checked: longform-first remains default, chat-only remains explicit exception, named templates remain soft overlays, topic_research and learning_artifacts are formally connected, deep-research multi-agent work remains explicit and artifact-bounded.
- next improvement idea: add model-evaluated behavior tests that score generated longform outputs against `references/regression-prompts.md`, especially claim traceability, inference labels, and precision-anchor blocking.

## 2026-05-26 merged research-longform hardening

- mode: buddys + multi-agent upgrade-skill
- evidence used: user requested removal of "Chinese-first", elimination of chat-mode teaching, a merged deep-research + longform route, model-inferred research nodes with soft target around five, mechanism-first teaching that templates may adjust, default bounded multi-agent/multi-pass execution, and removal of mandatory owner taste review.
- collaboration: Codex integrated; Claude and Gemini reviewed the route and both returned REFINE, emphasizing mandatory synthesis responsiveness, concrete examples/hooks, bounded artifacts before multi-agent expansion, and explicit fallback boundaries. Two Codex subagents implemented disjoint script/test and documentation lanes.
- files changed: SKILL.md, agents/openai.yaml, references/adaptive-router.md, references/masterzhuyan-planning.md, references/deep-research-execution.md, references/deep-research-agent-patterns.md, references/multi-agent-patterns.md, references/codex-execution.md, references/regression-prompts.md, references/quality-gates.md, references/masterzhuyan-output-contracts.md, references/exemplar-patterns.md, references/deep-research-quality-gates.md, references/longform-bridge.md, references/dense-topic-scaffold.md, references/deep-research-architecture.md, scripts/topic_research.py, tests/test_topic_research.py.
- behavior changes: MasterZhuyan now treats research/modeling plus file-backed longform as one default learning route; chat is only for delivery, limitation, or coordination notes. Research node planning uses model-inferred nodes with a soft target around five and a compact scored-node-candidate artifact when scope is uncertain. Mechanism-first is the default spine, with operational switches for comparison, classification, procedure, formula, rule, and narrative topics. Multi-pass is default for substantive learning runs and multi-agent work is allowed when bounded artifacts and one integrator are present. Artifact validation now rejects empty examples and teaching hooks, and synthesis/coverage gates reject structurally traceable but non-responsive research.
- validation result: smoke_test passed; unittest discovery passed with 28 tests; py_compile passed; skill_consistency_check passed with 0 failures and one expected registry warning because MasterZhuyan is not a collaborative skill.
- next improvement idea: add a semantic/model-evaluated responsiveness scorer for `primary_confusion` and `success_criteria`, because the current script-level alignment check is deterministic lexical overlap by design.

## 2026-05-27 Agent-first automation run 1 - SKILL.md route rewrite

- mode: bounded automation execution
- checklist item completed: 1. SKILL.md Agent-first/Jianfa rewrite.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代方案.md` and `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` require Agent-first, Skill-as-lever, ProcessTracing-first, active acquisition, artifact-backed agents, no default budget/stop/Clarifier, and quality tracing instead of hard gates.
- conflict check: no prior mtime/sha256 state existed for this automation series; target directory is not a git repository, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/SKILL.before-agent-first-20260527T110121.md`
- files changed: `SKILL.md`, `.evolution/evolution-log.md`.
- SKILL.md before: mtime `2026-05-26 12:32:42.597717400 +0800`, sha256 `312870bf93f9d92cdcef6925cb041798a866a6298f5895e1a1f058ca4fad6309`.
- SKILL.md after: mtime `2026-05-27 11:02:56.431367800 +0800`, sha256 `05df104b5bb373edfa0d1fe903c601e238b2c5c4b9f8c86fd7ccb4a19512649e`.
- behavior changes: frontmatter now declares the Agent-first route; Operating identity now exposes the Agent-first workbench; deep-research flow now routes acquisition, evidence, modeling, teaching composition, tracing, and integration through artifacts; quality blocking language was replaced with quality tracing and continuation mapping; reference map now points to `agent-fabric.md` and `process-tracing.md`; performance guardrails now act as trace prompts instead of prohibition-only language.
- Jianfa note: kept trigger language, output policy, source handling, named template rules, and longform fallback intact; moved complexity toward references and artifacts by adding only compact top-level contracts.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning.
- Claude/Codex debug state: no Claude process launched in this run because only one file was changed and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `references/agent-fabric.md` and `references/process-tracing.md` are now referenced but not yet created; this is the next bounded item.
- next atomic action: create `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/agent-fabric.md` from the engineering manual, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 2 - Agent Fabric reference

- mode: bounded automation execution
- checklist item completed: 2. 新增 `references/agent-fabric.md`.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` section "新增 Agent Fabric 参考文件" requires a dispatch reference defining Agent types, dispatch fields, output paths, and integrator promotion.
- conflict check: `references/agent-fabric.md` did not exist before this run; target directory is not a git repository; no overwrite occurred.
- files changed: `references/agent-fabric.md`, `.evolution/evolution-log.md`.
- `references/agent-fabric.md` before: missing.
- `references/agent-fabric.md` after: mtime `2026-05-27 11:06:26.438457200 +0800`, sha256 `5c88d9b96283b9db16511bfd02511ec433056d212be778785ada9a552c9f3530`.
- behavior changes: added the Agent Fabric workbench layout, dispatch card, Source Scout, Evidence Curator, Mechanism Modeler, Concept Graph Builder, Misconception Repairer, Comparison Builder, Teaching Composer, Trace Curator, and Integrator contracts; added source-heavy, concept-heavy, and review-heavy dispatch patterns; fixed the integrator merge rule around canonical promotion.
- Jianfa note: kept this as a reference file rather than inflating `SKILL.md`; retained only contracts and artifact formats needed for downstream execution.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed `SKILL.md` references `agent-fabric.md` and the new reference contains all listed agent types.
- Claude/Codex debug state: no Claude process launched in this run because only one new reference file was created and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `references/process-tracing.md` is still referenced by `SKILL.md` but not yet created.
- next atomic action: create `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/process-tracing.md` from the engineering manual, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 3 - ProcessTracing reference

- mode: bounded automation execution
- checklist item completed: 3. 新增 `references/process-tracing.md`.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` section "新增 ProcessTracing 参考文件" requires trace templates for process trace, integrator decisions, continuation map, agent output trace updates, index integration, and final delivery notes.
- conflict check: `references/process-tracing.md` did not exist before this run; target directory is not a git repository; no overwrite occurred.
- files changed: `references/process-tracing.md`, `.evolution/evolution-log.md`.
- `references/process-tracing.md` before: missing.
- `references/process-tracing.md` after: mtime `2026-05-27 11:09:40.116472000 +0800`, sha256 `78147ceae0f3124abe93a1a4c6f4d78e199478578567599b693d8dda321010b8`.
- behavior changes: added required trace files, `process_trace.md` phase timeline, Agent Run Index, Strong Evidence Zones, Expansion Signals, `integrator_decisions.md`, `continuation_map.md`, per-agent Trace Update block, `index.md` ProcessTracing links, and final delivery reading-order note.
- Jianfa note: kept ProcessTracing as a reusable reference and did not expand the top-level `SKILL.md`; the reference is template-heavy because downstream agents need exact artifact shapes.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed `SKILL.md` references `process-tracing.md` and the new reference contains process trace, integrator decisions, continuation map, trace update, index integration, and final delivery sections.
- Claude/Codex debug state: no Claude process launched in this run because only one new reference file was created and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `deep-research-execution.md` still describes the previous durable deep-research protocol and is not yet wired to Agent Fabric / active acquisition phases.
- next atomic action: update `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/deep-research-execution.md` to the Agent-first phase sequence from the engineering manual, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 4 - Deep research execution protocol

- mode: bounded automation execution
- checklist item completed: 4. 更新 `references/deep-research-execution.md`.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` section "改写 Deep Research 执行协议" requires replacing the old phase sequence with Agent-first contract/workbench, active source acquisition, evidence curation, knowledge modeling, chapter composition, and integration/tracing phases.
- conflict check: previous file state matched the recorded local state at run start; target directory is not a git repository, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/deep-research-execution.before-agent-first-20260527T111232.md`
- files changed: `references/deep-research-execution.md`, `.evolution/evolution-log.md`.
- `references/deep-research-execution.md` before: mtime `2026-05-26 12:32:52.835506400 +0800`, sha256 `f16a63e0897e93edf8a76206c8e7cd3493d8791d2f3f9b61f52db7090fde1bcd`.
- `references/deep-research-execution.md` after: mtime `2026-05-27 11:13:09.674251800 +0800`, sha256 `0354100621adf4186f8eda09df12ed2b16eeb9d447679f409d7df72242fbd0d3`.
- behavior changes: replaced the old linear research plan / source intake / knowledge model / chapter draft / verification pass with Agent-first phases; added active acquisition triggers; routed Source Scout, Evidence Curator, modeling agents, Teaching Composer, Trace Curator, and Integrator through file-backed artifacts; changed fallback into continuation handling that records missing artifacts and next handoff cards instead of stopping or switching to chat teaching.
- Jianfa note: preserved trigger conditions and file-backed delivery boundary while moving execution complexity into Agent Fabric and ProcessTracing artifacts.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed the protocol now contains Agent-first, active acquisition, Source Scout, Evidence Curator, modeling agents, Teaching Composer, Trace Curator, process trace, integrator decisions, continuation map, and final merge references.
- Claude/Codex debug state: no Claude process launched in this run because only one reference file was edited and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `codex-execution.md`, `multi-agent-patterns.md`, and `deep-research-agent-patterns.md` still need Agent-first wiring.
- next atomic action: update `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/codex-execution.md`, `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/multi-agent-patterns.md`, and `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/deep-research-agent-patterns.md` as the next coordinated reference-wiring item, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 5 - Codex execution wiring

- mode: bounded automation execution
- checklist item completed: 5a. 更新 `references/codex-execution.md`.
- split decision: the previous next action named three reference files; this run intentionally split the coordinated reference-wiring item to keep write scope bounded and avoid changing more than three files in one invocation.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` section "更新 codex-execution.md" requires adding the Agent-first workbench, real agent artifact paths, and canonical promotion recording.
- conflict check: previous file state matched the recorded local state at run start; target directory is not a git repository, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/codex-execution.before-agent-first-20260527T111624.md`
- files changed: `references/codex-execution.md`, `.evolution/evolution-log.md`.
- `references/codex-execution.md` before: mtime `2026-05-26 12:37:34.128347600 +0800`, sha256 `ddc9b1a9f356fbc327399f286cf8f0b8782533657799af4bbdb6585bb8935164`.
- `references/codex-execution.md` after: mtime `2026-05-27 11:16:46.378856700 +0800`, sha256 `7bee431e803275a534e5ad0d76b390b0f945a16129aec62bdd0d618af285392c`.
- behavior changes: added Agent-first workbench creation under longform root; linked `agent-fabric.md` dispatch cards and `process-tracing.md` trace templates; defined when role names become real via `notes/agent_outputs/<agent_type>/<agent_id>.md` or canonical notes; required dispatch cards and canonical promotion records in `notes/process_trace.md` and `notes/integrator_decisions.md`.
- Jianfa note: kept the file-system protocol concise and avoided duplicating the full Agent Fabric contract already stored in `agent-fabric.md`.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed Agent-first workbench, agent outputs, dispatch references, trace templates, and promotion records are present.
- Claude/Codex debug state: no Claude process launched in this run because only one reference file was edited and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `multi-agent-patterns.md` and `deep-research-agent-patterns.md` still need Agent-first wiring.
- next atomic action: update `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/multi-agent-patterns.md` to map split types onto Agent Fabric artifact roles, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 6 - Multi-agent split mapping

- mode: bounded automation execution
- checklist item completed: 5b. 更新 `references/multi-agent-patterns.md`.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` section "更新 multi-agent-patterns.md" requires preferring `agent-fabric.md`, mapping split types to Agent Fabric roles, writing outputs under `notes/agent_outputs/<agent_type>/...`, and recording canonical promotion in `notes/integrator_decisions.md`.
- conflict check: previous file state matched the recorded local state at run start; target directory is not a git repository, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/multi-agent-patterns.before-agent-first-20260527T111940.md`
- files changed: `references/multi-agent-patterns.md`, `.evolution/evolution-log.md`.
- `references/multi-agent-patterns.md` before: mtime `2026-05-26 12:33:29.053268200 +0800`, sha256 `ccf8ab9619a3b5ad8b1bcf3efab47cb4cccc3846469f579d4d76dadb9d41dc29`.
- `references/multi-agent-patterns.md` after: mtime `2026-05-27 11:20:24.382127300 +0800`, sha256 `54417dba00c6d108db752b71d0406100ef4d23f463b48c0814e187c06763c4ee`.
- behavior changes: mapped `section`, `source`, `lens`, and `check` splits to `teaching_composer`, `source_scout` / `evidence_curator`, `comparison_builder` / `misconception_repairer` / `concept_graph_builder`, and `trace_curator` / integrator review; replaced old worker/source/lens/check draft paths with Agent Fabric output paths; moved finding resolution from `notes/review.md` to `notes/integrator_decisions.md` / `notes/continuation_map.md`.
- Jianfa note: preserved split-type selection guidance while moving path ownership and promotion records into the shared Agent Fabric artifact model.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed Agent Fabric role mappings, agent output paths, integrator decisions, and absence of old draft/check paths.
- Claude/Codex debug state: no Claude process launched in this run because only one reference file was edited and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `deep-research-agent-patterns.md` still needs Agent-first wiring.
- next atomic action: update `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/deep-research-agent-patterns.md` to use `agent-fabric.md` as the primary dispatch contract and map evidence/model/verification splits to Agent Fabric roles, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 7 - Deep research agent adapter

- mode: bounded automation execution
- checklist item completed: 5c. 更新 `references/deep-research-agent-patterns.md`.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` section "更新 deep-research-agent-patterns.md" requires using `agent-fabric.md` as the primary dispatch contract and mapping evidence/model/verification splits to Agent Fabric roles.
- conflict check: previous file state matched the recorded local state at run start; target directory is not a git repository, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/deep-research-agent-patterns.before-agent-first-20260527T112325.md`
- files changed: `references/deep-research-agent-patterns.md`, `.evolution/evolution-log.md`.
- `references/deep-research-agent-patterns.md` before: mtime `2026-05-26 12:37:34.152144500 +0800`, sha256 `2aaeac73943811dd78d1e73c108a278f9d7d6ddb9f250e4eda0e09bd0e4f770c`.
- `references/deep-research-agent-patterns.md` after: mtime `2026-05-27 11:23:58.394810500 +0800`, sha256 `23a625152de044605808338fd02c3e55c09a8ed3bbed79f4bac78672e007aa6d`.
- behavior changes: added the Agent Fabric adapter note; mapped `evidence` to `evidence_curator`, `model` to `mechanism_modeler` / `concept_graph_builder` / `misconception_repairer` / `comparison_builder`, and verification to `trace_curator` plus integrator decision record; replaced `evidence-drafts` and `model-drafts` paths with `notes/agent_outputs/...`; moved phase resolution and fallback records from `notes/review.md` to `notes/process_trace.md`, `notes/integrator_decisions.md`, and `notes/continuation_map.md`.
- Jianfa note: preserved deep-research sequencing constraints while removing duplicate path conventions now owned by Agent Fabric.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed Agent Fabric split mappings, new output paths, integrator decision/continuation records, and absence of old hard-gate wording.
- Claude/Codex debug state: no Claude process launched in this run because only one reference file was edited and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `deep-research-output-contracts.md` still needs agent output, process trace, and continuation map field contracts.
- next atomic action: update `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/deep-research-output-contracts.md` to add Agent-first output, process trace, and continuation map fields, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 8 - Deep research output contracts

- mode: bounded automation execution
- checklist item completed: 6a. 更新 `references/deep-research-output-contracts.md`.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` requires adding agent output, process trace, and continuation map field contracts; current file still used old `research_plan`, `uncertainty_budget`, and threshold-style uncertainty language.
- conflict check: previous file state matched the recorded local state at run start; target directory is not a git repository, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/deep-research-output-contracts.before-agent-first-20260527T112716.md`
- files changed: `references/deep-research-output-contracts.md`, `.evolution/evolution-log.md`.
- `references/deep-research-output-contracts.md` before: mtime `2026-05-26 09:06:42.128326400 +0800`, sha256 `6fa5b89ffa77bf4c556093750fb16901c7e1b5c3e66ab57f2757c20d24d42745`.
- `references/deep-research-output-contracts.md` after: mtime `2026-05-27 11:28:04.299138900 +0800`, sha256 `c0a6b62d3db06f9bd057171e101475eb21dd3f3141230be194944fc28ad0c837`.
- behavior changes: replaced `notes/research_plan.md` with `notes/research_brief.md`; added Source Map contract; expanded Evidence Ledger and Knowledge Model fields for Agent-first use; added Agent Output, Process Trace, Integrator Decisions, and Continuation Map contracts; removed fixed percentage uncertainty threshold and `verify-before-teach` stop-style action language.
- Jianfa note: this reference now carries field contracts while `agent-fabric.md` carries role contracts and `process-tracing.md` carries templates, keeping top-level `SKILL.md` light.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed research brief, source map, evidence ledger, knowledge model, agent output, process trace, integrator decisions, continuation map fields, and absence of old threshold/stop fields.
- Claude/Codex debug state: no Claude process launched in this run because only one reference file was edited and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `quality-gates.md` still needs to be converted into quality tracing / enhancement map semantics.
- next atomic action: update `/mnt/c/Users/83233/.codex/skills/master-zhuyan/references/quality-gates.md` so checks record evidence/support/continuation state instead of acting as hard gates, then run smoke, pytest-if-available, consistency check, and update this log with mtime/sha256.

## 2026-05-27 Agent-first automation run 9 - Quality tracing map

- mode: bounded automation execution
- checklist item completed: 6b. 更新 `references/quality-gates.md`.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代方案.md` and `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` require changing quality gates into quality tracing / enhancement map semantics: checks should record evidence, support state, integrator action, and continuation candidates rather than acting as hard pass/fail gates.
- conflict check: previous file state matched the recorded local state at run start; target directory is not a git repository, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/quality-gates.before-agent-first-20260527T113140.md`
- files changed: `references/quality-gates.md`, `.evolution/evolution-log.md`.
- `references/quality-gates.md` before: mtime `2026-05-26 12:40:45.769724500 +0800`, sha256 `dee90d254dde8a5673d2801234ef094a0a633cf8d7b46a568955e8a9592011d7`.
- `references/quality-gates.md` after: mtime `2026-05-27 11:32:42.837638600 +0800`, sha256 `dfc3a11f693aec8cbea1b7ddf5bb18cbf26fe0faae4af5e95d1f94e309ea1148`.
- behavior changes: renamed the semantic contract to quality tracing while preserving the legacy filename; added an Enhancement Map record shape with `support_state`, evidence refs, teaching effect, integrator action, next agent, output path, and user-visible note; converted longform, chapter value, coverage, source/uncertainty, teaching value, responsiveness, multi-agent, prep-template, and final review checks into trace/enhancement actions; routed resolved findings to `notes/integrator_decisions.md`, open branches to `notes/continuation_map.md`, phase state to `notes/process_trace.md`, and delegated review to `notes/agent_outputs/trace_curator/<agent_id>.md`; replaced old `notes/review.md` and "blocks final merge" style with acquisition, softening, omission, revision, or continuation choices.
- Jianfa note: kept the existing review categories because they are behavior-bearing, but changed their carrier from hard gate prose to artifact records and integrator actions. This preserves quality pressure without adding a new blocker framework.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed enhancement map, support state, `integrator_decisions`, `continuation_map`, and absence of old `blocks final merge`, `return to the research planner`, and `notes/review.md` wording in `quality-gates.md`.
- Claude/Codex debug state: no Claude process launched in this run because only one reference file was edited and validation did not fail. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: Agent-first artifact validation is not yet implemented in scripts/tests, so the new workbench contract is documented but not mechanically checked.
- next atomic action: add `/mnt/c/Users/83233/.codex/skills/master-zhuyan/scripts/validate_agent_first_artifacts.py` with CLI checks for the Agent-first longform workbench, then add a small fixture and tests in the following bounded runs.

## 2026-05-27 Agent-first automation run 10 - Artifact validator and tests

- mode: bounded automation execution with subagent review
- checklist items completed: 7. 新增 `scripts/validate_agent_first_artifacts.py`; 8. 新增 `tests/fixtures/agent_first_sample/`; 9. 新增 `tests/test_agent_first_artifacts.py`; 10. 更新 `scripts/smoke_test.py` 覆盖 validator help / JSON success path.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` section "回归验证和实施命令" requires a CLI validator for the Agent-first workbench, a minimal fixture, pytest-style tests, and smoke coverage.
- conflict check: validator script, test file, and fixture did not exist before this run; target directory is not a git repository. `scripts/smoke_test.py` existed, so a timestamp backup was created before editing.
- snapshot: `.evolution/snapshots/smoke_test.before-agent-first-validator-20260527T113539.py`
- files changed: `scripts/validate_agent_first_artifacts.py`, `scripts/smoke_test.py`, `tests/test_agent_first_artifacts.py`, `tests/fixtures/agent_first_sample/**`, `.evolution/evolution-log.md`.
- `scripts/validate_agent_first_artifacts.py` before: missing.
- `scripts/validate_agent_first_artifacts.py` after: mtime `2026-05-27 11:42:32.069542900 +0800`, sha256 `d61d491d857bdd5f795e83c5bb5ad01f747b3dc5bd7e0e430824f3fe7f2ed424`.
- `scripts/smoke_test.py` before: mtime `2026-05-25 22:23:11.000000000 +0800`, sha256 `d4a0f4d3770fdfaa9ca41cbf9782f8689f93b88fc4c7d48467611750b40e084b`.
- `scripts/smoke_test.py` after: mtime `2026-05-27 11:42:32.090369100 +0800`, sha256 `188aa40cacf19163558d357f8c5f6243977e46df697bd0ffbb9dfb133bf6bdb8`.
- `tests/test_agent_first_artifacts.py` before: missing.
- `tests/test_agent_first_artifacts.py` after: mtime `2026-05-27 11:42:32.105680600 +0800`, sha256 `43c56e6ab6cf8442a354a0f7586488f15e5156490e680ac4525deea015828a0b`.
- `tests/fixtures/agent_first_sample/` before: missing.
- `tests/fixtures/agent_first_sample/` after: 13 files, aggregate sha256 of sorted file hashes `8badf1435b80fb076e85ad3789d8ff988708e282d3be9aafce35ca93f99f5a2a`.
- behavior changes: added a standalone validator with `--root` and `--json`; checks required files, required directories, empty required files, non-empty chapter set, and non-empty markdown agent outputs; reports `missing`, `present`, `empty_files`, chapter count, agent output count, warnings, and summary; smoke test now imports the validator, verifies CLI help mentions `--root` and `--json`, creates a temporary Agent-first sample, and validates JSON success; tests cover text success, JSON success, missing artifact failure, empty required file failure, and empty agent output failure.
- subagent review: Tesla reviewed the slice read-only and found no blockers. Its main nice-to-fix item was that empty `notes/agent_outputs/` should fail rather than warn; Codex accepted and implemented that tightening before final validation.
- validation result: `python3 scripts/validate_agent_first_artifacts.py --root tests/fixtures/agent_first_sample` passed; `python3 scripts/validate_agent_first_artifacts.py --root tests/fixtures/agent_first_sample --json` returned `"ok": true`, 1 chapter, and 1 agent output; `python3 scripts/smoke_test.py` passed; `python3 -m unittest tests.test_agent_first_artifacts` passed with 5 tests; `python3 -m unittest discover -s tests` passed with 33 tests; `python3 -m py_compile` passed for all scripts; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning.
- Claude/Codex debug state: no Claude process launched in this run because validation passed and the independent subagent review found no blocker. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: the validator checks structural Agent-first artifact presence and non-empty core files, but not full semantic schemas for every artifact. The next debug pass should decide whether semantic validation belongs in this script, a separate validator, or future model-evaluated checks.
- next atomic action: perform a Codex debug/audit pass over the full Agent-first MasterZhuyan iteration against the plan/manual, looking for stale route names, old hard-gate language, inconsistent artifact paths, and validation gaps before handing a bounded debug request to ClaudeCode.

## 2026-05-27 Agent-first automation run 11 - Codex debug pass

- mode: Codex debug/audit pass
- checklist item completed: 11a. Codex 对 Agent-first 改造做一次系统 debug。
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代方案.md` and `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` require Agent-first, ProcessTracing, active acquisition, no completion budget / stop policy / Clarifier / hard gate defaults, unified `notes/agent_outputs`, `notes/integrator_decisions.md`, and `notes/continuation_map.md`.
- audit method: searched current `SKILL.md`, references, and schemas for stale `research_plan`, `notes/review.md`, worker draft directories, hard-gate language, pass/fail quality report semantics, Clarifier language, budget fields, and `blocked` states; then patched confirmed conflicts and reran validation.
- conflict check: target directory is not a git repository; backups were created before editing reusable instruction/reference/schema files.
- snapshots: `.evolution/snapshots/SKILL.before-codex-debug-20260527T114635.md`, `codex-execution.before-codex-debug-20260527T114635.md`, `deep-research-agent-patterns.before-codex-debug-20260527T114635.md`, `deep-research-architecture.before-codex-debug-20260527T114635.md`, `longform-bridge.before-codex-debug-20260527T114635.md`, `quality_report.schema.before-codex-debug-20260527T114635.json`, `research_brief.schema.before-codex-debug-20260527T114635.json`, `multi-agent-patterns.before-codex-debug-20260527T114635.md`, `deep-research-output-contracts.before-codex-debug-20260527T114635.md`, `adaptive-router.before-codex-debug-20260527T114635.md`, `masterzhuyan-output-contracts.before-codex-debug-20260527T114635.md`.
- files changed: `SKILL.md`, `references/codex-execution.md`, `references/deep-research-agent-patterns.md`, `references/deep-research-architecture.md`, `references/longform-bridge.md`, `references/multi-agent-patterns.md`, `references/deep-research-output-contracts.md`, `references/adaptive-router.md`, `references/masterzhuyan-output-contracts.md`, `schemas/quality_report.schema.json`, `schemas/research_brief.schema.json`, `.evolution/evolution-log.md`.
- selected before -> after sha256:
  - `SKILL.md`: `05df104b5bb373edfa0d1fe903c601e238b2c5c4b9f8c86fd7ccb4a19512649e` -> `840f909d0ee2e894db6eac883631764a8ca824464847133d058dffb2f1d81982`
  - `references/codex-execution.md`: `7bee431e803275a534e5ad0d76b390b0f945a16129aec62bdd0d618af285392c` -> `28b16b363bd57f1d56246dc6038dd7a953c8f58b9523890fe5ffeec0c77d91c0`
  - `references/deep-research-architecture.md`: `ba7496d2af07358daf43d2a5d1b4581dabeb262136de7b39bb17e9e1908a6dde` -> `4858fc652f5a699588d06ac33f09d3aa5d5ab895ba971fdcd855cf84584ba02b`
  - `schemas/quality_report.schema.json`: `2b7d0cc9191b799c1a7dd87a72c7f75f44d162c754dcb49cd33a51486e6131e4` -> `5ff89135f20ecd7792089e00e972aa33425cd50ab197f175c825c8d59e024263`
  - `schemas/research_brief.schema.json`: `afab9d2816506c6e18ec8062d135e2d07888f4f8fc0728ba8fea719e84fdc8d9` -> `e1b0d05dcaf1be3787a6b8dafe2803cd615fbe7ccd90a11b6649c179a0fb1734`
- behavior changes: added `notes/research_brief.md` to top-level workbench listings; replaced the stale `research_plan -> evidence_ledger -> knowledge_model -> chapter_plan` chain with `research_brief + source_map -> evidence_ledger -> knowledge_model -> chapter_plan`; changed `codex-execution.md` and `longform-bridge.md` from `notes/review.md` / worker-draft paths to `notes/agent_outputs`, `notes/integrator_decisions.md`, `notes/process_trace.md`, and `notes/continuation_map.md`; reframed `deep-research-architecture.md` from Quality Report pass/revise/blocked to Quality Trace support state / integrator action / continuation candidates; changed `quality_report.schema.json` into a legacy-named quality trace schema; changed `research_brief.schema.json` question status from `blocked` to `needs_acquisition` / `recorded_for_continuation`; removed remaining Clarifier-gate and quality-gate wording from the audited references.
- debug note: during validation, Codex caught that `python3 -m json.tool file1 file2` treats the second argument as an output path and had temporarily overwritten `schemas/quality_report.schema.json` with formatted research-brief JSON. Codex restored the quality trace schema and reran per-file JSON validation.
- validation result: per-file `python3 -m json.tool` passed for `schemas/research_brief.schema.json` and `schemas/quality_report.schema.json`; targeted stale-language `rg` over `SKILL.md`, references, and schemas returned no matches for the audited old terms; `python3 scripts/smoke_test.py` passed; `python3 -m unittest discover -s tests` passed with 33 tests; `python3 scripts/validate_agent_first_artifacts.py --root tests/fixtures/agent_first_sample --json` returned `"ok": true`; `python3 -m py_compile` passed for all scripts; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning.
- Claude/Codex debug state: Codex debug pass completed. ClaudeCode debug pass was launched after this run as a read-only bounded audit. Preserve rule: do not kill slow Claude processes unless they report an error.
- known temporary gap: `scripts/topic_research.py` still has a legacy standalone `research_plan` field and `agent_outputs/*.md` paths by design; `codex-execution.md` now labels it a standalone legacy trace package and tells Agent-first runs to promote useful findings into the canonical workbench.
- next atomic action: wait for ClaudeCode debug findings; if it reports blockers, patch them and rerun validation, otherwise log the ClaudeCode pass and proceed to final Jianfa redundancy/completion audit.

## 2026-05-27 Agent-first automation run 12 - ClaudeCode debug pass

- mode: ClaudeCode bounded debug audit plus Codex integration
- checklist item completed: 11b. ClaudeCode 对 Agent-first 改造做一次 debug 复核。
- execution notes: first ClaudeCode attempt ran read-only against the full current package and failed with server-side API 524 timeout; Codex did not kill the process. Second attempt used `--bare`, read-only tools, and a smaller scope, but hit the explicit `--max-budget-usd 0.25` limit before returning findings. Third attempt used no tools and a current-state audit summary; it returned successfully.
- ClaudeCode result: no blockers. It accepted the legacy standalone `scripts/topic_research.py` boundary, accepted pytest unavailability as non-blocking because unittest/py_compile/json validation passed, and accepted the quality trace schema semantics. Its only `should_fix_before_complete` item was that `schemas/quality_report.schema.json` should declare a canonical quality-trace alias so future agents do not infer old pass/fail semantics from the legacy filename.
- files changed: `schemas/quality_report.schema.json`, `.evolution/evolution-log.md`.
- `schemas/quality_report.schema.json` before Claude integration: mtime `2026-05-27 11:51:33.379296100 +0800`, sha256 `5ff89135f20ecd7792089e00e972aa33425cd50ab197f175c825c8d59e024263`.
- `schemas/quality_report.schema.json` after Claude integration: mtime `2026-05-27 12:06:53.406038700 +0800`, sha256 `da7c3bba49ddb0c34ab0b71974b872c4bee85870b830948a3ea83060769eae30`.
- behavior changes: added root-level `"x-canonical-name": "quality_trace_report"` to the legacy-named quality schema. This is non-breaking JSON Schema metadata and keeps the file path stable while making the intended semantic name explicit.
- validation result after Claude integration: `python3 -m json.tool schemas/quality_report.schema.json` passed; `python3 scripts/smoke_test.py` passed; `python3 -m unittest discover -s tests` passed with 33 tests; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning; `rg` confirmed `x-canonical-name` and no `overall_status`, `pass_with_notes`, or `blocked` remained in `quality_report.schema.json`.
- Claude/Codex debug state: Codex debug pass and ClaudeCode debug pass are both complete. Preserve rule was followed: Claude was never killed; only errored attempts were retried with smaller scopes.
- known temporary gap: no live end-to-end generation run has yet been performed for the broad/manual acceptance examples; current validation proves structural contracts, scripts, schemas, and stale-language cleanup, not full teaching output quality.
- next atomic action: run final Jianfa redundancy pass and completion audit against the plan/manual; if no missing requirements remain, mark the goal complete, otherwise patch the identified gap.

## 2026-05-27 Agent-first automation run 13 - Final Jianfa and completion audit

- mode: final Jianfa redundancy pass plus plan/manual acceptance audit.
- checklist item completed: 11. 最终 Jianfa 冗余整理和验收.
- evidence used: `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代方案.md` and `/mnt/c/Users/83233/Desktop/MasterZhuyan迭代工程手册.md` lines 53-63, 67-76, 1740-1750, and 1812-1832.
- snapshots: `.evolution/snapshots/learning_artifacts.before-final-jianfa-20260527T121019.py`, `.evolution/snapshots/topic_research.before-final-jianfa-20260527T121019.py`, `.evolution/snapshots/test_learning_artifacts.before-final-jianfa-20260527T121019.py`, `.evolution/snapshots/smoke_test.before-final-jianfa-20260527T121019.py`, `.evolution/snapshots/openai.before-final-jianfa-20260527T121019.yaml`, `.evolution/snapshots/lesson_plan.schema.before-final-jianfa-20260527T121019.json`, `.evolution/snapshots/deep-research-quality-gates.before-final-jianfa-20260527T121019.md`, `.evolution/snapshots/20260527-121505-final-jianfa/`.
- files changed in final pass: `scripts/learning_artifacts.py`, `scripts/topic_research.py`, `scripts/smoke_test.py`, `tests/test_learning_artifacts.py`, `agents/openai.yaml`, `schemas/lesson_plan.schema.json`, `references/deep-research-quality-gates.md`, `references/regression-prompts.md`, `.evolution/evolution-log.md`.
- selected final sha256:
  - `scripts/learning_artifacts.py`: `c68f2655438d0060c2fd95af0122c76d6d7e0304633e74105e6a04168bebf71e`
  - `scripts/topic_research.py`: `c79369c16d4f9c335be100088112b668df92cd7c07615214213ff9c121a462b2`
  - `references/regression-prompts.md`: `1a01f666e6f52bb23a93e3cf1ad13bb182477356d01e320a2ffe9ed02e219c31`
  - `schemas/lesson_plan.schema.json`: `64ca7519caa8f28ef2a5c07c4266864a1375af98de2818d7b985ccd0b69ec3b1`
  - `references/deep-research-quality-gates.md`: `7a7bc58e6e32021af5ff1ec23dc7e6698a18fca57cb0af24e9f55670d8cc08c4`
- behavior changes: renamed legacy `*_GATE` learning-artifact output constants to `*_CHECK`; changed internal validation error/log vocabulary from `gate` to `check`; changed lesson-plan review task field from `gate` to `dimension`; changed the OpenAI agent prompt from `scoring as a gate` to `scoring as a limiter`; rewrote `deep-research-quality-gates.md` and `regression-prompts.md` language toward quality tracing / enhancement rather than hard gates.
- compatibility note: `scripts/topic_research.py` keeps `research_plan` inside the standalone legacy trace package by design. `references/codex-execution.md` labels this helper legacy and requires promotion into canonical Agent-first artifacts: `notes/research_brief.md`, `notes/source_map.md`, `notes/evidence_ledger.md`, `notes/knowledge_model.md`, and `notes/agent_outputs/<agent_type>/<agent_id>.md`.
- validation result: `python3 -m py_compile scripts/prep_template.py scripts/mz_longform.py scripts/learning_artifacts.py scripts/topic_research.py scripts/smoke_test.py scripts/validate_agent_first_artifacts.py` passed; `python3 -m json.tool` passed for `schemas/lesson_plan.schema.json`, `schemas/quality_report.schema.json`, and `schemas/research_brief.schema.json`; `python3 scripts/smoke_test.py` passed; `python3 scripts/validate_agent_first_artifacts.py --root tests/fixtures/agent_first_sample --json` returned `"ok": true`; `python3 -m unittest discover -s tests` passed with 33 tests; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning.
- stale-language audit: `rg -n "\bgate\b|quality gate|质量门"` over `SKILL.md`, `references`, `scripts`, `tests`, `schemas`, and `agents` now only finds the intentional legacy-filename note in `references/quality-gates.md` explaining that it is not a pass/fail gate.
- completion audit: manual file-change table lines 53-63 are present; implementation order lines 67-76 is complete; engineering acceptance commands lines 1740-1750 were run where the environment allowed them, with pytest explicitly recorded as unavailable; completion coverage command lines 1812-1832 covers `SKILL.md`, `references/agent-fabric.md`, `references/process-tracing.md`, `references/deep-research-execution.md`, `references/codex-execution.md`, `references/multi-agent-patterns.md`, `references/deep-research-agent-patterns.md`, `tests/test_agent_first_artifacts.py`, and `scripts/validate_agent_first_artifacts.py`.
- Claude/Codex debug state: Codex debug pass and ClaudeCode debug pass are complete; the final pass did not launch or kill Claude. The user rule to not kill slow Claude processes was followed.
- known limitation after completion: no live full teaching-generation acceptance run was executed; the completed work validates the skill contracts, scripts, schemas, Agent-first artifact fixture, automation record, and stale-language cleanup.
- automation state: updated active automation `masterzhuyan-agent-first` from implementation checklist mode to steady-state monitoring mode. Future runs should report status by default and patch only newly discovered regressions, handoff conflicts, validation failures, or user-requested changes.

## 2026-05-27 Jianfa release pass - Loosen chat and sequencing gates

- mode: user-directed Jianfa release pass.
- intent: reduce unnecessary triggers and extra gating while preserving source discipline, high-risk boundaries, Agent-first artifacts, and Integrator stability.
- snapshots: `.evolution/snapshots/20260527-152158-jianfa-release/`, `.evolution/snapshots/20260527-152432-chat-release-followup/`, `.evolution/snapshots/20260527-152525-deep-research-chat-release/`.
- files changed: `SKILL.md`, `agents/openai.yaml`, `references/deep-research-agent-patterns.md`, `references/codex-execution.md`, `references/quality-gates.md`, `references/regression-prompts.md`, `references/deep-research-execution.md`, `.evolution/evolution-log.md`.
- selected after sha256:
  - `SKILL.md`: `3bbbf867ff5ae7ce9579d66965822190953d87dfbf785f76eaa0630713329189`
  - `agents/openai.yaml`: `047755041aed2502771f4cc71d20d8a2b28dde61f7c18cc3e07ae49cc4f6d963`
  - `references/deep-research-agent-patterns.md`: `18d8fb5d3b694e0a5c45fe6c5326b1fde2b7386f1d4f2d2ed66e1103e73967b0`
  - `references/codex-execution.md`: `078ff3da35868eab3596da8ff9535846702b5d441662d5de84de08fe7cafbf22`
  - `references/quality-gates.md`: `c08ef200bd9be6821601d9b13f6d8af1c41ba5f4a4b12a985d3d82d1fcfe248e`
  - `references/regression-prompts.md`: `c744bebe74ddfc90ef10db2212cddc34e61d3d9037fa6fb8767b9806d0167f74`
  - `references/deep-research-execution.md`: `817559bf1ed88742f23cc8b8a1c5342ad3ec16dc1ef3879af8b1c1df15a1aa2c`
- behavior changes: compressed the frontmatter trigger list into broad learning/explanation/study/template activation; changed brief/no-files behavior from limitation-only to concise high-quality teaching with the same source and uncertainty discipline; collapsed repeated template activation rules in `SKILL.md` into one soft-overlay contract and left details to `references/prep-template-workflow.md`; changed deep-research sequencing from hard evidence/model serialization to canonical artifact stabilization with parallel exploratory sidecars; simplified synthesis responsiveness from `must answer/satisfy then revise before polishing` into direct revision cues or continuation notes.
- follow-up cleanup: aligned `quality-gates.md`, `regression-prompts.md`, and `deep-research-execution.md` so no-files/brief chat no longer acts as a no-teaching gate.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 scripts/validate_agent_first_artifacts.py --root tests/fixtures/agent_first_sample --json` returned `"ok": true`; `python3 -m unittest discover -s tests` passed with 33 tests; `python3 -m py_compile` passed for all scripts; `python3 -m json.tool` passed for changed/critical schemas; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning.
- stale-language audit: targeted `rg` found no remaining matches for the old chat ban, hard evidence/model parallel ban, hard draft-before-research ban, or hard responsiveness wording.
- Claude/Codex debug state: no Claude process was launched or killed for this small user-directed release pass.

## 2026-05-27 Jianfa release pass - Remove short-answer cue

- mode: user-directed Jianfa follow-up.
- intent: remove accidental short/brief cues from the chat-only/no-files route so explicit chat teaching can still be high-quality and not implicitly throttled.
- snapshot: `.evolution/snapshots/20260527-152845-remove-short-chat-cue/`.
- files changed: `SKILL.md`, `agents/openai.yaml`, `references/quality-gates.md`, `references/codex-execution.md`, `references/deep-research-execution.md`, `references/regression-prompts.md`, `.evolution/evolution-log.md`.
- selected after sha256:
  - `SKILL.md`: `23420ef996f908f232e8cd607fb88b02da4b18b5c8bf55f95bd98ee3ef1753fd`
  - `agents/openai.yaml`: `8dcc73f613787d2677c4e2002a0ed77e1adf5e469ccb93a094b4cb2e276e3cd4`
  - `references/quality-gates.md`: `4179915d48136dea0e6e5e674d2215bb4b95fa7da0bd34ec0a77f4ba470f7c5c`
  - `references/codex-execution.md`: `c5316b63fb8e823f1991fa0a3dcb5b8b89bdf0557a0e539a96fc0b89c996d94f`
  - `references/deep-research-execution.md`: `ded5390ecf2fe141853918ce7f94c28811cd34a2aeb35c297d16330f13e239cf`
  - `references/regression-prompts.md`: `b88d948196fa1dad34268d73fd694595be040387bcc9d0abe65e90ec865ebaab`
- behavior changes: replaced `brief chat`, `short answer`, `concise teaching answer`, `高质量短讲解`, and `简洁聊天回答` in the chat-only/no-files route with `chat-only output` / `high-quality teaching answer`; preserved limitation notes only for missing file-backed capability and delivery-focused post-longform summaries.
- validation result: `python3 scripts/smoke_test.py` passed; `python3 scripts/validate_agent_first_artifacts.py --root tests/fixtures/agent_first_sample --json` returned `"ok": true`; `python3 -m unittest discover -s tests` passed with 33 tests; `python3 -m py_compile` passed for all scripts; `python3 -m json.tool` passed for critical schemas; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning.
- remaining short/brief terms: most are artifact names (`research_brief`, `framing_brief`, `worker_briefs`), UI metadata (`short_description`), or delivery-summary guidance after a file-backed deliverable. Review candidates remain in `references/exemplar-patterns.md`, `references/deep-research-quality-gates.md`, `references/masterzhuyan-output-contracts.md`, `references/quality-gates.md`, `references/deep-research-architecture.md`, and `references/prep-template-workflow.md`.

## 2026-05-27 Jianfa release pass - Remove chat-mode traces in references

- mode: user-directed Jianfa follow-up.
- intent: remove stale "chat mode" / "short answer" / limitation-only wording from the remaining references while keeping a lightweight boundary that does not pretend file-backed longform was completed.
- snapshot: `.evolution/snapshots/20260527-153412-remove-chat-mode-traces/`.
- files changed: `references/exemplar-patterns.md`, `references/deep-research-quality-gates.md`, `references/masterzhuyan-output-contracts.md`, `.evolution/evolution-log.md`.
- selected after sha256:
  - `references/exemplar-patterns.md`: `7bb3549914b21a0f9c3e21cba514d358729773f359aca19b778e67387744ae5b`
  - `references/deep-research-quality-gates.md`: `f5f900e90af0712928be6fa1b5ecf612f00ab2e560f2d067e2bfe46712cdbc2e`
  - `references/masterzhuyan-output-contracts.md`: `fb17019c78c0d0235ece2c0bf95d024d891715f76ee225422f98821e84a5be9c`
- behavior changes: replaced the exemplar's "只在聊天里简短回答" pattern with "current conversation delivery"; replaced no-files/brief limitation-only wording with current available delivery surface plus high-quality teaching; replaced `brief reason` / `smallest useful next step` with a boundary note plus useful teaching content.
- product judgment: no-files/chat-only/file-unavailable is not the dominant route, but it is common enough to keep a small boundary rule. The boundary should prevent false claims that files were created, not throttle the teaching answer or create a separate chat mode.
- validation result: targeted stale-language `rg` over the three edited references returned no matches; `python3 scripts/smoke_test.py` passed; `python3 scripts/validate_agent_first_artifacts.py --root tests/fixtures/agent_first_sample --json` returned `"ok": true`; `python3 -m unittest discover -s tests` passed with 33 tests; `python3 -m py_compile` and critical schema `json.tool` checks passed; `python3 -m pytest tests` skipped because `/usr/bin/python3: No module named pytest`; `skill_consistency_check.py --side codex --skill master-zhuyan` passed with 0 failures and one expected registry warning.

## 2026-05-29 Jianfa slice - Quality action boundary

- mode: Jianfa + ClaudeCode + Codex explorer review of Quality Trace versus Citation Audit action surfaces.
- snapshot: `.evolution/snapshots/quality-action-boundary-20260529T090000/`.
- files changed: `schemas/quality_report.schema.json`, `references/quality-gates.md`, `references/deep-research-quality-gates.md`, `references/deep-research-output-contracts.md`, `references/deep-research-execution.md`, `references/codex-execution.md`, `tests/test_schema_contracts.py`, `.evolution/evolution-log.md`, `reports/jianfa-audit-20260528.md`.
- decision: keep Citation Audit claim-level actions exactly `accept`, `revise`, `soften_claim`, `omit_claim`, `mark_unavailable`, `dispatch_agent`, and `record_continuation`. Keep `create_missing_artifact` only in Quality Trace for container or required-file repair; remove `not_applicable` from the Quality Trace action enum because it is a support/status value, not an action.
- behavior changes: `quality-gates.md` now names the Quality Trace-only boundary and includes `mark_unavailable`; DeepResearch quality/output/execution contracts now use canonical action values near `integrator_action` instead of natural-language aliases such as `verify, soften, omit, scope out, dispatch evidence work`.
- tests added: `tests/test_schema_contracts.py` pins Citation Audit actions exactly, pins Quality Trace actions to Citation Audit plus `create_missing_artifact`, rejects duplicate action enum values, and checks that docs name the Quality Trace-only boundary.
- selected after sha256:
  - `schemas/quality_report.schema.json`: `45a16495102ea9b0c52ef64952b67bb78ff1581381c5dd89bd15f5f300e3c19d`
  - `references/quality-gates.md`: `984f06ca99bfed0230baec0fe873668a1439bcb3a5784a096546d5fcd92e6c27`
  - `references/deep-research-quality-gates.md`: `a83cef953d62592904c860c078eafedb9b2a88d8bbfaac27cc097aa396239420`
  - `references/deep-research-output-contracts.md`: `321ac9c377a1711e37645ccc8d9127d3be14976641e7529c39a742285dd9c8f7`
  - `references/deep-research-execution.md`: `c9480fde8899aab49f5b89c8574f025893b9145822dd43674a5eec655f214fd7`
  - `references/codex-execution.md`: `5641df07373f992ad3c3225773ef8e91e869804116ba0acf722c7949a8300fec`
  - `tests/test_schema_contracts.py`: `1e0e047c8b4d9501ede280cef903384aefb0e9913a846ededa246f4a5f481651`
- validation result: focused suite `tests/test_schema_contracts.py tests/test_deep_research_artifacts.py` passed with `62 passed`; broader suite `tests/test_mz_longform.py tests/test_deep_research_artifacts.py tests/test_schema_contracts.py tests/test_prep_template.py tests/test_legacy_topic_research.py tests/test_legacy_learning_artifacts.py` passed with `97 passed, 2 subtests passed`; `python3 scripts/smoke_test.py` passed; `python3 scripts/validate_deep_research_artifacts.py --root tests/fixtures/deep_research_sample --json` returned `"ok": true`; `python3 -m py_compile` passed for runtime scripts; `python3 -m json.tool` passed for all schemas.
- CodeGraph note: CLI status failed with `disk I/O error` during this slice, so direct file reads, ClaudeCode, subagent review, and tests were used as the authoritative evidence.
